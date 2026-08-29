#!/usr/bin/env python3
"""Capture a cited web source as durable, greppable text in this repository.

Why this exists
---------------
``/verify-claims`` is the highest-stakes workflow in this project, and it ends
with an instruction that has never been executable here:

    Append verified sources (URL, retrieval date, key quote) to ``SOURCES.md``
    so a later session can retrace the reasoning.

A search snippet is a lead, not proof. To honour that rule a session has to
actually retrieve the source, and — because every session runs in an ephemeral
container — write what it retrieved somewhere that survives. This tool does
exactly that: it fetches a URL, extracts the readable text, and lands it in

* ``derived/sources/<slug>.md`` — the full capture, the same "plain-text mirror
  for reading and grepping" role that ``derived/*.txt`` plays for the PDFs; and
* ``SOURCES.md`` — one indexed entry per source: title, URL, retrieval date,
  word count, and an excerpt.

Re-capturing a URL rewrites its entry in place rather than appending a
duplicate, so the index stays deterministic across sessions.

Provenance
----------
The fetching core — the SSRF address policy, per-redirect re-validation, the
redirect and byte caps, the accumulate-warnings-never-raise contract, and the
metadata/body extraction shape — is adapted from ``backend/app/url_scrape.py``
in ``professorpalmer/portable-llm-wiki`` (MIT, Copyright (c) 2026 Cary Palmer).
See ``tools/README.md`` for the licence notice and a list of what was changed
and why.

Usage
-----
    python3 tools/source_capture.py <url> [<url> ...]
    python3 tools/source_capture.py <url> --stdout        # print, write nothing
    python3 tools/source_capture.py <url> --json          # machine-readable
    python3 tools/source_capture.py --self-test           # offline checks

No third-party dependencies beyond ``requests``, which is already present; HTML
is parsed with the standard library. Nothing here imports the manuscript or
touches the PDFs.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import html.parser
import ipaddress
import json
import os
import re
import socket
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from requests.adapters import HTTPAdapter

MAX_BYTES = 1_000_000  # ~1 MB cap on what we will download
REQUEST_TIMEOUT = 20.0
MAX_REDIRECTS = 5
USER_AGENT = (
    "ExstoErgoSum-SourceCapture/1.0 "
    "(+https://github.com/SanjaySrivatsa5172/EXSTO-ERGO-SUM; citation verification)"
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CAPTURE_DIR = REPO_ROOT / "derived" / "sources"
DEFAULT_INDEX = REPO_ROOT / "SOURCES.md"

EXCERPT_CHARS = 600

# Elements whose text is chrome, not content.
_DROP_TAGS = frozenset(
    {"script", "style", "nav", "footer", "aside", "header", "noscript", "form", "svg", "template"}
)
# Elements whose text we keep, and how each is rendered into markdown.
_BLOCK_TAGS = frozenset({"h1", "h2", "h3", "p", "li", "blockquote"})
# Elements that never nest and so never need an implicit close.
_VOID_TAGS = frozenset(
    {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }
)


# --------------------------------------------------------------------------- #
# Address policy (SSRF)
# --------------------------------------------------------------------------- #

def _allow_private_targets() -> bool:
    """Escape hatch for deliberately capturing an internal host (an intranet
    mirror of a paper, say). OFF by default: a URL handed to this tool comes out
    of a manuscript's bibliography, and a bibliography must never be able to
    steer a fetch at local infrastructure. Set ``SOURCE_CAPTURE_ALLOW_PRIVATE=1``
    to relax."""
    return os.getenv("SOURCE_CAPTURE_ALLOW_PRIVATE", "0").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _unwrap(ip: ipaddress._BaseAddress) -> ipaddress._BaseAddress:
    """Reduce a tunnelled or mapped IPv6 address to the IPv4 address it carries.

    ``::ffff:127.0.0.1``, 6to4 and Teredo all reach an IPv4 destination while
    presenting as IPv6. Python 3.11.10+ folds ``ipv4_mapped`` into ``is_private``
    on its own, but not 6to4 or Teredo, and the exact version is not something
    this repository pins — so unwrap explicitly and judge the address that will
    actually be dialled.
    """
    for attr in ("ipv4_mapped", "sixtofour", "teredo"):
        inner = getattr(ip, attr, None)
        if inner is not None:
            # ``teredo`` yields a (server, client) pair; the client is the peer.
            return inner[1] if isinstance(inner, tuple) else inner
    return ip


def _ip_is_blocked(ip_text: str) -> bool:
    """True for any address we must never connect to: loopback, RFC1918
    private, link-local (which covers the 169.254.169.254 cloud metadata
    endpoint), unique-local IPv6, reserved, multicast, unspecified — and,
    as a catch-all, anything not globally routable."""
    try:
        ip = ipaddress.ip_address(ip_text)
    except ValueError:
        return True  # un-parseable -> treat as unsafe
    ip = _unwrap(ip)
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_reserved
        or ip.is_multicast
        or ip.is_unspecified
        or not ip.is_global
    )


def _public_ips_for_host(host: str) -> tuple[list[str], str]:
    """Resolve ``host`` (A and AAAA) and return its addresses, or ``([], reason)``
    if any one of them is blocked. Fails closed: a hostname that resolves to one
    public and one private address is refused outright, since we cannot control
    which the connection would pick."""
    if not host:
        return [], "missing host"
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except (socket.gaierror, UnicodeError) as exc:
        return [], f"DNS resolution failed: {exc}"
    if not infos:
        return [], "host did not resolve"
    ips: list[str] = []
    for info in infos:
        ip_text = info[4][0]
        if _ip_is_blocked(ip_text):
            return [], f"blocked address {ip_text} (private/loopback/link-local/non-global)"
        if ip_text not in ips:
            ips.append(ip_text)
    return ips, ""


def _proxy_for(scheme: str) -> str:
    """The configured forward proxy for ``scheme``, or ``""``."""
    for var in (f"{scheme}_proxy", f"{scheme.upper()}_PROXY"):
        value = os.getenv(var, "").strip()
        if value:
            return value
    return ""


def _explain_request_error(exc: Exception, hostname: Optional[str]) -> str:
    """Turn a transport exception into a finding a reviewer can act on.

    The distinction that matters for ``/verify-claims`` is *policy* versus
    *source*: a 403 from the forward proxy means this container may not reach
    the host at all, which says nothing about whether the citation is good. That
    must never be recorded as a failed verification, and per the command's own
    rule it must not be retried or routed around.
    """
    text = str(exc)
    proxy_denied = "Tunnel connection failed: 403" in text or (
        "403 Forbidden" in text and "proxy" in text.lower()
    )
    if proxy_denied:
        return (
            f"egress blocked by network policy: the agent proxy refused a tunnel to "
            f"{hostname or 'this host'} (403). This is an environment restriction, not "
            f"evidence about the source — do not retry or route around it. Capture this "
            f"URL from an unrestricted network, or verify via the MCP scholarly tools."
        )
    if isinstance(exc, requests.exceptions.SSLError):
        return f"TLS verification failed for {hostname or 'host'}: {exc}"
    if isinstance(exc, requests.exceptions.ConnectTimeout):
        return f"connection to {hostname or 'host'} timed out after {REQUEST_TIMEOUT:g}s"
    if isinstance(exc, requests.exceptions.ReadTimeout):
        return f"{hostname or 'host'} accepted the connection but stopped responding"
    return f"http error: {exc}"


class _PinnedHostAdapter(HTTPAdapter):
    """Verify the certificate against the real hostname while the URL carries a
    literal IP, so the connection lands on the address we already validated."""

    def __init__(self, hostname: str, **kwargs) -> None:
        self._hostname = hostname
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):  # type: ignore[override]
        kwargs["server_hostname"] = self._hostname
        kwargs["assert_hostname"] = self._hostname
        return super().init_poolmanager(*args, **kwargs)


def _url_on_ip(url: str, ip: str) -> str:
    """Rewrite ``url`` so the connect target is ``ip``; caller sets Host/SNI."""
    parsed = urlparse(url)
    try:
        version = ipaddress.ip_address(ip).version
    except ValueError:
        version = 4
    host = f"[{ip}]" if version == 6 else ip
    netloc = f"{host}:{parsed.port}" if parsed.port is not None else host
    return urlunparse(parsed._replace(netloc=netloc))


def _host_header(parsed) -> str:
    hostname = parsed.hostname or ""
    return f"{hostname}:{parsed.port}" if parsed.port is not None else hostname


# --------------------------------------------------------------------------- #
# HTML extraction
# --------------------------------------------------------------------------- #

class _Extractor(html.parser.HTMLParser):
    """Pull title, metadata, and body prose out of HTML using only the standard
    library. Streaming rather than tree-based: real pages leave ``<p>`` and
    ``<li>`` unclosed constantly, and a stack that flushes on the next block
    start survives that better than a tree walk does.

    Blocks found inside ``<article>``/``<main>`` are tracked separately so the
    caller can prefer them — on a news or journal page that is the difference
    between the paper and the sidebar.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta: dict[str, str] = {}
        self.blocks: list[str] = []
        self.article_blocks: list[str] = []
        self._stack: list[str] = []
        self._drop_depth = 0
        self._article_depth = 0
        self._in_title = False
        self._block_tag = ""
        self._buf: list[str] = []

    # -- helpers ---------------------------------------------------------- #

    def _flush(self) -> None:
        if not self._block_tag:
            return
        text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
        tag, self._block_tag, self._buf = self._block_tag, "", []
        if not text:
            return
        if tag in ("h1", "h2", "h3"):
            rendered = f"{'#' * int(tag[1])} {text}"
        elif tag == "li":
            rendered = f"- {text}"
        elif tag == "blockquote":
            rendered = f"> {text}"
        else:
            rendered = text
        self.blocks.append(rendered)
        if self._article_depth:
            self.article_blocks.append(rendered)

    # -- HTMLParser hooks ------------------------------------------------- #

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        if tag in _VOID_TAGS:
            if tag == "meta" and not self._drop_depth:
                self._record_meta(dict(attrs))
            elif tag == "br" and self._block_tag:
                self._buf.append(" ")
            return

        self._stack.append(tag)
        if tag in _DROP_TAGS:
            self._drop_depth += 1
            self._flush()
            return
        if self._drop_depth:
            return
        if tag in ("article", "main"):
            self._article_depth += 1
        if tag == "title":
            self._in_title = True
        elif tag in _BLOCK_TAGS:
            self._flush()  # implicit close of an unclosed predecessor
            self._block_tag = tag

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in _VOID_TAGS or tag not in self._stack:
            return
        # Unwind to the matching open tag, so stray </div> cannot desynchronise us.
        while self._stack:
            open_tag = self._stack.pop()
            if open_tag in _DROP_TAGS:
                self._drop_depth = max(0, self._drop_depth - 1)
            elif not self._drop_depth:
                if open_tag in ("article", "main"):
                    self._article_depth = max(0, self._article_depth - 1)
                if open_tag == "title":
                    self._in_title = False
                elif open_tag == self._block_tag:
                    self._flush()
            if open_tag == tag:
                break

    def handle_data(self, data: str) -> None:
        if self._drop_depth:
            return
        if self._in_title:
            self.title += data
        elif self._block_tag:
            self._buf.append(data)

    def close(self) -> None:  # type: ignore[override]
        super().close()
        self._flush()

    def _record_meta(self, attrs: dict) -> None:
        content = (attrs.get("content") or "").strip()
        if not content:
            return
        key = (attrs.get("property") or attrs.get("name") or "").strip().lower()
        # First value wins: pages repeat these, and the <head> copy is the real one.
        if key and key not in self.meta:
            self.meta[key] = content


def _decode(raw: bytes, header_encoding: Optional[str]) -> str:
    """Decode page bytes. ``requests`` falls back to ISO-8859-1 for any
    ``text/*`` response without an explicit charset, which mangles the accented
    characters and diacritics this project cares about — so sniff the document's
    own declaration first and prefer UTF-8 over that guess."""
    sniffed = None
    head = raw[:4096]
    match = re.search(rb"""<meta[^>]+charset=["']?\s*([\w.:-]+)""", head, re.I)
    if match:
        sniffed = match.group(1).decode("ascii", "ignore")
    for candidate in (sniffed, header_encoding, "utf-8"):
        if not candidate or candidate.lower() in ("iso-8859-1", "ascii"):
            continue
        try:
            return raw.decode(candidate)
        except (LookupError, UnicodeDecodeError):
            continue
    return raw.decode("utf-8", errors="replace")


# --------------------------------------------------------------------------- #
# Result type
# --------------------------------------------------------------------------- #

@dataclass
class ScrapedPage:
    url: str
    final_url: str = ""
    status_code: int = 0
    retrieved_utc: str = ""
    title: str = ""
    description: str = ""
    og_title: str = ""
    og_description: str = ""
    og_image: str = ""
    site_name: str = ""
    content: str = ""  # extracted body text, blank-line-separated blocks
    word_count: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def heading(self) -> str:
        host = urlparse(self.final_url or self.url).hostname or "source"
        return self.title or self.og_title or host

    @property
    def excerpt(self) -> str:
        """A prose excerpt for the index. The block markers that make the full
        capture readable ("## ", "- ", "> ") become noise once flattened into a
        single quoted line, so strip them here."""
        stripped = [
            re.sub(r"^\s*(?:#{1,3}\s+|[-*]\s+|>\s+)", "", block)
            for block in self.content.split("\n\n")
        ]
        flat = re.sub(r"\s+", " ", " ".join(stripped)).strip()
        if len(flat) <= EXCERPT_CHARS:
            return flat
        return flat[:EXCERPT_CHARS].rsplit(" ", 1)[0] + "…"

    def slug(self) -> str:
        """A stable, readable filename for this URL. The hash suffix keeps two
        different URLs on one host from colliding after sanitisation."""
        parsed = urlparse(self.final_url or self.url)
        stem = f"{parsed.hostname or 'source'}{parsed.path}"
        stem = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-").lower()[:60] or "source"
        digest = hashlib.sha256((self.final_url or self.url).encode()).hexdigest()[:8]
        return f"{stem}-{digest}"

    def to_markdown(self) -> str:
        """The full capture, as written to ``derived/sources/``."""
        out: list[str] = [f"# {self.heading}", ""]
        out.append("| Field | Value |")
        out.append("|---|---|")
        out.append(f"| Requested URL | <{self.url}> |")
        if self.final_url and self.final_url != self.url:
            out.append(f"| Final URL | <{self.final_url}> |")
        out.append(f"| Retrieved (UTC) | {self.retrieved_utc} |")
        if self.status_code:
            out.append(f"| HTTP status | {self.status_code} |")
        if self.site_name:
            out.append(f"| Site | {self.site_name} |")
        out.append(f"| Words extracted | {self.word_count} |")
        out.append("")
        out.append(
            "> Machine-extracted page text, captured for citation verification. "
            "Reference, **not** source: the publisher's page is authoritative, and "
            "JavaScript-rendered content will be missing. Quote from the original "
            "before relying on anything below."
        )
        out.append("")
        if self.description:
            out += ["## Summary", "", self.description, ""]
        if self.og_description and self.og_description != self.description:
            out += ["## Open Graph description", "", self.og_description, ""]
        if self.content:
            out += ["## Page content", "", self.content, ""]
        if self.errors:
            out += ["## Capture warnings", ""] + [f"- {e}" for e in self.errors]
        return "\n".join(out).rstrip() + "\n"

    def to_index_entry(self, capture_path: Optional[str]) -> str:
        """One ``SOURCES.md`` record, delimited so a re-capture can replace it."""
        out = [f"<!-- source: {self.url} -->", f"### {self.heading}", ""]
        out.append(f"- **URL:** <{self.url}>")
        if self.final_url and self.final_url != self.url:
            out.append(f"- **Resolved to:** <{self.final_url}>")
        out.append(f"- **Retrieved:** {self.retrieved_utc}")
        if capture_path:
            out.append(f"- **Capture:** [`{capture_path}`]({capture_path}) ({self.word_count} words)")
        else:
            out.append(f"- **Words extracted:** {self.word_count}")
        if self.errors:
            out.append(f"- **Warnings:** {'; '.join(self.errors)}")
        excerpt = self.excerpt
        if excerpt:
            out += ["", "> " + excerpt]
        out += ["", "<!-- /source -->"]
        return "\n".join(out)

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "final_url": self.final_url,
            "status_code": self.status_code,
            "retrieved_utc": self.retrieved_utc,
            "title": self.title,
            "description": self.description,
            "og_title": self.og_title,
            "og_description": self.og_description,
            "og_image": self.og_image,
            "site_name": self.site_name,
            "word_count": self.word_count,
            "errors": list(self.errors),
            "content_excerpt": self.excerpt,
        }


# --------------------------------------------------------------------------- #
# Fetch
# --------------------------------------------------------------------------- #

def scrape(url: str, *, timeout: float = REQUEST_TIMEOUT) -> ScrapedPage:
    """Fetch and parse ``url``. Never raises: every failure is accumulated onto
    the returned :class:`ScrapedPage`, because a broken citation is a finding to
    report, not an exception that aborts a verification pass mid-bibliography."""
    page = ScrapedPage(
        url=url,
        retrieved_utc=_dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        page.errors.append(f"unsupported scheme {parsed.scheme!r}; expected http or https")
        return page
    if not parsed.hostname:
        page.errors.append("URL missing a hostname")
        return page

    # Redirects are followed by hand so the address policy is re-applied on every
    # hop; a 302 into 169.254.169.254 must be refused as firmly as a direct
    # request for it.
    response: Optional[requests.Response] = None
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
    )
    try:
        current = url
        for _ in range(MAX_REDIRECTS + 1):
            hop = urlparse(current)
            if hop.scheme not in ("http", "https") or not hop.hostname:
                page.errors.append(f"unsupported redirect target {current!r}")
                return page

            request_url, headers = current, {}
            if _allow_private_targets():
                pass  # operator has explicitly opted out of the policy
            else:
                ips, why = _public_ips_for_host(hop.hostname)
                if not ips:
                    label = "refusing to fetch" if current == url else "refusing redirect to"
                    page.errors.append(f"{label} {hop.hostname!r}: {why}")
                    return page
                # Pinning the validated IP is what closes the window between the
                # DNS check and the connection's own lookup. Through a forward
                # proxy it is not available at all — the proxy resolves the name
                # itself — so we fall back to pre-flight validation and say so
                # rather than implying a guarantee we cannot make.
                if _proxy_for(hop.scheme):
                    pass
                else:
                    request_url = _url_on_ip(current, ips[0])
                    headers["Host"] = _host_header(hop)
                    if hop.scheme == "https":
                        session.mount(f"https://{ips[0]}", _PinnedHostAdapter(hop.hostname))

            response = session.get(
                request_url,
                headers=headers,
                timeout=timeout,
                allow_redirects=False,
                stream=True,
            )
            if response.status_code not in (301, 302, 303, 307, 308):
                break
            location = response.headers.get("location")
            response.close()
            if not location:
                page.errors.append(f"http {response.status_code} with no Location header")
                break
            current = urljoin(current, location)
        else:
            page.errors.append("too many redirects; aborting")
            return page

        if response is None:  # defensive: unreachable in practice
            page.errors.append("no response received")
            return page

        page.final_url = current
        page.status_code = response.status_code
        if response.status_code != 200:
            # Don't bail: many publishers 403 a bot but still serve usable
            # <head> metadata, which is enough to confirm a citation exists.
            page.errors.append(f"http {response.status_code} {response.reason}".rstrip())

        content_type = response.headers.get("content-type", "")

        chunks, total = [], 0
        for chunk in response.iter_content(65_536):
            chunks.append(chunk)
            total += len(chunk)
            if total >= MAX_BYTES:
                page.errors.append(f"response exceeded {MAX_BYTES:,} bytes; truncated")
                break
        response.close()
        body = _decode(b"".join(chunks)[:MAX_BYTES], response.encoding)
    except requests.RequestException as exc:
        page.errors.append(_explain_request_error(exc, parsed.hostname))
        return page
    finally:
        session.close()

    _parse_body(page, body, content_type)
    return page


def _looks_like_html(text: str) -> bool:
    head = text[:4096].lstrip().lower()
    return head.startswith(("<!doctype html", "<html", "<?xml")) or "<body" in head or "<meta" in head


def _parse_body(page: ScrapedPage, body: str, content_type: str) -> None:
    """Route the payload to the right extractor.

    Plain text is kept verbatim rather than run through the HTML extractor. A
    good share of the primary sources this project needs — RFCs, arXiv text
    mirrors, author-posted transcripts — are served as ``text/plain``, and the
    upstream module, written for scraping profile pages, would silently reduce
    every one of them to zero words.
    """
    ctype = content_type.lower()
    is_markup = any(t in ctype for t in ("html", "xml")) or _looks_like_html(body)
    is_plain = not is_markup and ("text/" in ctype or (not ctype and bool(body.strip())))

    if is_markup:
        _parse_html(page, body)
    elif is_plain:
        _keep_plain_text(page, body)
    else:
        # A PDF or other binary: say so plainly instead of writing an empty
        # capture that looks like a source was checked when none was.
        page.errors.append(
            f"unsupported content-type {content_type or 'unset'}; no text extracted "
            f"(a PDF or other binary must be captured by hand)"
        )
        return

    if page.word_count >= 30:
        return
    page.errors.append(
        "very little text extracted; treat the metadata as a lead, not as a primary read"
        + (" (page is likely JavaScript-rendered or bot-walled)" if is_markup else "")
    )


def _keep_plain_text(page: ScrapedPage, body: str) -> None:
    paragraphs = [
        re.sub(r"[ \t]+", " ", block).strip()
        for block in re.split(r"\n\s*\n", body.replace("\r\n", "\n"))
    ]
    page.content = "\n\n".join(p for p in paragraphs if p)
    page.word_count = len(re.findall(r"\S+", page.content))
    if not page.title:
        # Plain text carries no <title>; the filename is the best label we have.
        stem = (urlparse(page.final_url or page.url).path or "").rstrip("/").rsplit("/", 1)[-1]
        page.title = stem or ""


def _parse_html(page: ScrapedPage, markup: str) -> None:
    parser = _Extractor()
    try:
        parser.feed(markup)
        parser.close()
    except Exception as exc:  # noqa: BLE001 - malformed markup must not abort a pass
        page.errors.append(f"parse error: {exc}")

    page.title = re.sub(r"\s+", " ", parser.title).strip()
    page.description = parser.meta.get("description", "")
    page.og_title = parser.meta.get("og:title", "")
    page.og_description = parser.meta.get("og:description", "")
    page.og_image = parser.meta.get("og:image", "")
    page.site_name = parser.meta.get("og:site_name", "")
    # Academic pages often carry citation_* metadata and nothing else useful.
    if not page.title:
        page.title = parser.meta.get("citation_title", "")

    blocks = parser.article_blocks or parser.blocks
    deduped: list[str] = []
    for line in blocks:
        if not deduped or line != deduped[-1]:
            deduped.append(line)

    page.content = "\n\n".join(deduped)
    page.word_count = len(re.findall(r"\S+", page.content))


# --------------------------------------------------------------------------- #
# Writing captures and the index
# --------------------------------------------------------------------------- #

_INDEX_HEADER = """# Sources

Primary sources retrieved for claim and citation verification, newest capture
last. Generated and maintained by `tools/source_capture.py`; see
`tools/README.md`.

Each entry records the URL, the retrieval date, and an excerpt. The full
captured text lives in `derived/sources/`. Both are **reference, not source** —
machine-extracted page text, subject to the same fidelity caveats as
`derived/README.md`. A capture is evidence that a page was retrieved and what it
said at that moment; it is not a substitute for reading the publisher's version
before quoting it.

Nothing here is added by hand. To record a source:

    python3 tools/source_capture.py <url>
"""

_INDEX_PLACEHOLDER = "_No sources captured yet._"


def _entry_bounds(text: str, url: str) -> Optional[tuple[int, int]]:
    """Locate an existing entry for ``url``, as ``(start, end)`` offsets."""
    marker = f"<!-- source: {url} -->"
    start = text.find(marker)
    if start == -1:
        return None
    closer = "<!-- /source -->"
    end = text.find(closer, start)
    return (start, len(text) if end == -1 else end + len(closer))


def update_index(index_path: Path, page: ScrapedPage, capture_path: Optional[str]) -> str:
    """Insert or replace ``page``'s entry in the index. Returns "added" or
    "updated" so the caller can report honestly."""
    text = index_path.read_text(encoding="utf-8") if index_path.exists() else _INDEX_HEADER
    text = text.replace(_INDEX_PLACEHOLDER, "")  # drop it once a real entry lands
    entry = page.to_index_entry(capture_path)
    bounds = _entry_bounds(text, page.url)
    if bounds:
        start, end = bounds
        text = text[:start] + entry + text[end:]
        action = "updated"
    else:
        text = text.rstrip() + "\n\n" + entry + "\n"
        action = "added"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return action


def capture(
    url: str,
    *,
    capture_dir: Path = DEFAULT_CAPTURE_DIR,
    index_path: Path = DEFAULT_INDEX,
    write: bool = True,
) -> tuple[ScrapedPage, Optional[Path]]:
    """Fetch ``url`` and, unless ``write`` is false, persist the capture and index."""
    page = scrape(url)
    if not write:
        return page, None
    capture_dir.mkdir(parents=True, exist_ok=True)
    path = capture_dir / f"{page.slug()}.md"
    path.write_text(page.to_markdown(), encoding="utf-8")
    rel = os.path.relpath(path, index_path.parent)
    update_index(index_path, page, rel)
    return page, path


# --------------------------------------------------------------------------- #
# Self-test (offline)
# --------------------------------------------------------------------------- #

def _self_test() -> int:
    """Offline checks of the two things most worth getting right: the address
    policy and the extractor. No network, so this is safe to run anywhere."""
    failures: list[str] = []

    def check(label: str, got, want) -> None:
        if got != want:
            failures.append(f"{label}: expected {want!r}, got {got!r}")

    blocked = [
        "127.0.0.1", "10.0.0.1", "192.168.1.1", "172.16.0.1", "169.254.169.254",
        "0.0.0.0", "224.0.0.1", "::1", "fe80::1", "fc00::1", "::",
        "::ffff:127.0.0.1", "::ffff:169.254.169.254", "::ffff:10.0.0.1",
        "2002:7f00:0001::",              # 6to4 wrapping 127.0.0.1
        "not-an-ip", "",
    ]
    for ip in blocked:
        check(f"blocked {ip!r}", _ip_is_blocked(ip), True)
    for ip in ["8.8.8.8", "1.1.1.1", "93.184.216.34", "2606:4700:4700::1111", "::ffff:8.8.8.8"]:
        check(f"allowed {ip!r}", _ip_is_blocked(ip), False)

    markup = """
    <html><head>
      <title>  A   Paper   Title </title>
      <meta name="description" content="The abstract.">
      <meta property="og:site_name" content="Journal">
      <meta name="description" content="A later duplicate that must lose.">
    </head><body>
      <nav><p>Home</p><p>About</p></nav>
      <script>var x = "<p>not content</p>";</script>
      <header><p>Site banner</p></header>
      <main>
        <h2>Findings</h2>
        <p>First paragraph &amp; an entity.
        <p>Second paragraph, unclosed predecessor.</p>
        <ul><li>Point one<li>Point two</ul>
        <blockquote>A quoted line.</blockquote>
      </main>
      <footer><p>Copyright</p></footer>
    </body></html>
    """
    page = ScrapedPage(url="https://example.org/paper")
    _parse_html(page, markup)
    check("title", page.title, "A Paper Title")
    check("description", page.description, "The abstract.")
    check("site_name", page.site_name, "Journal")
    lines = page.content.split("\n\n")
    check(
        "content blocks",
        lines,
        [
            "## Findings",
            "First paragraph & an entity.",
            "Second paragraph, unclosed predecessor.",
            "- Point one",
            "- Point two",
            "> A quoted line.",
        ],
    )
    for chrome in ("Home", "About", "not content", "Site banner", "Copyright"):
        if chrome in page.content:
            failures.append(f"chrome leaked into content: {chrome!r}")

    # Plain text is kept verbatim, not run through the HTML extractor: RFCs and
    # arXiv text mirrors are primary sources and must not reduce to zero words.
    plain = ScrapedPage(url="https://www.rfc-editor.org/rfc/rfc8890.txt")
    _parse_body(plain, "Line one.\n\n  Line   two.\r\n\r\nLine three.\n", "text/plain; charset=utf-8")
    check("plain text blocks", plain.content, "Line one.\n\nLine two.\n\nLine three.")
    check("plain text words", plain.word_count, 6)
    check("plain text title from path", plain.title, "rfc8890.txt")

    # A server that mislabels HTML as text/plain must still be parsed as HTML.
    mislabelled = ScrapedPage(url="https://example.org/x")
    _parse_body(mislabelled, "<html><head><title>T</title></head><body><p>Body.</p></body></html>", "text/plain")
    check("sniffs mislabelled HTML", mislabelled.title, "T")

    # A binary payload yields an honest refusal, not a silent empty capture.
    binary = ScrapedPage(url="https://example.org/paper.pdf")
    _parse_body(binary, "%PDF-1.7 ...", "application/pdf")
    check("binary refused", any("unsupported content-type" in e for e in binary.errors), True)
    check("binary has no bogus JS warning", any("JavaScript-rendered" in e for e in binary.errors), False)

    # Encoding: a UTF-8 page with no charset header must not be mangled. The
    # manuscript's Sanskrit diacritics are the reason this matters.
    decoded = _decode("<html><body><p>Ahiṃsā</p></body></html>".encode("utf-8"), None)
    check("utf-8 decode without header charset", "Ahiṃsā" in decoded, True)
    diacritic_page = ScrapedPage(url="https://example.org/s")
    _parse_html(diacritic_page, decoded)
    check("diacritics survive extraction", "Ahiṃsā" in diacritic_page.content, True)

    # Index round-trip: a re-capture replaces, never duplicates.
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        index = Path(tmp) / "SOURCES.md"
        first = ScrapedPage(url="https://example.org/a", title="First", retrieved_utc="2026-01-01")
        check("first write", update_index(index, first, "derived/sources/a.md"), "added")
        second = ScrapedPage(url="https://example.org/a", title="Revised", retrieved_utc="2026-02-02")
        check("second write", update_index(index, second, "derived/sources/a.md"), "updated")
        body = index.read_text(encoding="utf-8")
        check("no duplicate entry", body.count("<!-- source: https://example.org/a -->"), 1)
        check("entry replaced", "Revised" in body and "First" not in body, True)

        # The "no sources yet" placeholder must not survive the first capture.
        seeded = Path(tmp) / "SEEDED.md"
        seeded.write_text(_INDEX_HEADER.rstrip() + "\n\n" + _INDEX_PLACEHOLDER + "\n", encoding="utf-8")
        update_index(seeded, first, "derived/sources/a.md")
        check("placeholder cleared", _INDEX_PLACEHOLDER in seeded.read_text(encoding="utf-8"), False)

    slug = ScrapedPage(url="https://arxiv.org/abs/2501.00001").slug()
    check("slug shape", bool(re.fullmatch(r"arxiv-org-abs-2501-00001-[0-9a-f]{8}", slug)), True)

    if failures:
        print("SELF-TEST FAILED", file=sys.stderr)
        for line in failures:
            print(f"  - {line}", file=sys.stderr)
        return 1
    print("self-test passed")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _display_path(path: Path) -> str:
    """Repo-relative when the capture lands inside the repo, absolute otherwise
    — a custom --capture-dir must not crash the report."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _report(page: ScrapedPage, path: Optional[Path]) -> None:
    ok = page.status_code == 200 and page.word_count >= 30
    print(f"{'ok  ' if ok else 'warn'} {page.url}")
    print(f"      title: {page.heading}")
    print(f"      words: {page.word_count}   retrieved: {page.retrieved_utc}")
    if path:
        print(f"      capture: {_display_path(path)}")
    for err in page.errors:
        print(f"      ! {err}")


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="source_capture.py",
        description="Capture a cited web source into derived/sources/ and SOURCES.md.",
    )
    parser.add_argument("urls", nargs="*", help="one or more http(s) URLs to capture")
    parser.add_argument("--stdout", action="store_true", help="print the capture; write nothing")
    parser.add_argument("--json", action="store_true", help="emit JSON; write nothing")
    parser.add_argument("--capture-dir", type=Path, default=DEFAULT_CAPTURE_DIR)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--timeout", type=float, default=REQUEST_TIMEOUT)
    parser.add_argument("--self-test", action="store_true", help="run offline checks and exit")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.self_test:
        return _self_test()
    if not args.urls:
        parser.error("give at least one URL, or --self-test")

    write = not (args.stdout or args.json)
    results = []
    for url in args.urls:
        # One unusable URL must not abandon the rest of a bibliography.
        try:
            if write:
                page, path = capture(url, capture_dir=args.capture_dir, index_path=args.index)
                results.append(page)
                _report(page, path)
            else:
                page = scrape(url, timeout=args.timeout)
                results.append(page)
                if args.stdout:
                    print(page.to_markdown())
        except OSError as exc:
            print(f"fail {url}\n      ! could not write capture: {exc}", file=sys.stderr)

    if args.json:
        print(json.dumps([p.to_dict() for p in results], indent=2, ensure_ascii=False))

    # Exit non-zero if nothing usable came back, so a caller can branch on it.
    if results and all(p.word_count < 30 for p in results):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
