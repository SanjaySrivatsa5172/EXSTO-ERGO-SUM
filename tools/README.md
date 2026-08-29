# tools/

Small, dependency-light utilities that support the manuscript workflow. This is
not application code — the repository is an academic submission (see
`CLAUDE.md`), and nothing here is part of the paper.

## `source_capture.py` — capture a cited source as durable text

`/verify-claims` ends with an instruction that, until now, no session could
actually carry out:

> Append verified sources (URL, retrieval date, key quote) to `SOURCES.md` so a
> later session can retrace the reasoning.

Sessions run in ephemeral containers, so a page read in one session is gone by
the next. This tool closes that gap: it retrieves a URL, extracts the readable
text, and writes it where git will keep it.

```bash
python3 tools/source_capture.py https://example.org/paper     # capture + index
python3 tools/source_capture.py <url> --stdout                # print, write nothing
python3 tools/source_capture.py <url> --json                  # machine-readable
python3 tools/source_capture.py --self-test                   # offline checks
```

Each capture produces two artefacts:

| Artefact | Role |
|---|---|
| `derived/sources/<slug>.md` | The full extracted page text |
| `SOURCES.md` | One indexed entry: title, URL, retrieval date, word count, excerpt |

Re-capturing a URL **replaces** its index entry rather than appending a second
one, so the index stays deterministic and a refresh produces a clean diff.

### These captures are reference, not source

Exactly as with `derived/*.txt`, a capture is machine-extracted text and a lossy
view of the real page. It is evidence that a URL was retrieved on a given date
and what it said at that moment — **not** a substitute for reading the
publisher's version before quoting it. JavaScript-rendered content will be
missing; the tool warns when it extracts almost nothing.

Captures are committed deliberately. That is the point: a claim verified in
July should still be checkable in October, from a container that has never seen
the open web.

### Requirements

`requests` (already present) and the Python standard library. Deliberately no
`httpx`, no `beautifulsoup4`, no `lxml`: this repository has no package manager
and no dependency file, and a verification tool that must be `pip install`-ed
before it runs is a tool that will not be run. HTML is parsed with
`html.parser`.

### Network policy in this environment

General HTTPS egress is blocked here — the agent proxy refuses a tunnel with a
`403` for most hosts, which is why `/verify-claims` steers primary reads to the
MCP scholarly tools (Scite, PubMed, bioRxiv). The tool reports that case as an
explicit *environment restriction*, distinct from any failure of the source:

```
egress blocked by network policy: the agent proxy refused a tunnel to
arxiv.org (403). This is an environment restriction, not evidence about the
source — do not retry or route around it.
```

Record that verbatim rather than logging a failed verification, and do not try
to route around it. Capture the URL from an unrestricted network instead.

### Safety: what the tool refuses to fetch

URLs handed to this tool come out of a bibliography, so the fetcher treats them
as untrusted input:

- **Address policy.** Every hostname is resolved before connecting, and the
  request is refused if *any* returned address is loopback, RFC1918 private,
  link-local (which covers the `169.254.169.254` cloud metadata endpoint),
  unique-local, reserved, multicast, unspecified, or otherwise not globally
  routable. It fails closed: one bad address in a set refuses the whole host.
  IPv4-mapped, 6to4, and Teredo IPv6 addresses are unwrapped first, so
  `::ffff:127.0.0.1` cannot slip past as "an IPv6 address".
- **Every redirect hop is re-validated.** A permitted host that `302`s to the
  metadata endpoint is refused mid-chain (verified by test).
- **Caps.** At most 5 redirects; at most 1 MB downloaded.
- **Schemes.** `http` and `https` only — `file://`, `ftp://` and friends are
  rejected before any I/O.
- **Never raises.** Every failure is accumulated as a warning on the result, so
  one dead link cannot abort a pass over a whole bibliography.

`SOURCE_CAPTURE_ALLOW_PRIVATE=1` disables the address policy for deliberately
capturing an internal host. Leave it unset in normal use.

**One honest limitation.** The strongest form of this defence pins the
already-validated IP for the connection, closing the window in which DNS could
be re-pointed between the check and the connect (DNS rebinding). Behind a
forward proxy that is not possible — the proxy resolves the hostname itself —
and this environment sets both `HTTPS_PROXY` and
`CLAUDE_CODE_PROXY_RESOLVES_HOSTS`. The tool therefore pins when connecting
directly and falls back to pre-flight validation when a proxy is configured,
rather than implying a guarantee it cannot make. Egress control in that case
rests with the proxy.

### Provenance and licence

The fetching core is adapted from
[`backend/app/url_scrape.py`](https://github.com/professorpalmer/portable-llm-wiki/blob/main/backend/app/url_scrape.py)
in `professorpalmer/portable-llm-wiki` — specifically the SSRF address policy,
per-hop redirect re-validation, the redirect and byte caps, the
accumulate-warnings-never-raise contract, and the shape of the metadata and
body-text extraction.

What changed, and why:

| Change | Reason |
|---|---|
| `httpx` + `BeautifulSoup` → `requests` + `html.parser` | Neither dependency is installed here and there is no package manager to add them |
| `async` → synchronous CLI | Nothing in this repository runs an event loop |
| Output: wiki onboarding markdown → capture file + `SOURCES.md` index | The purpose is citation provenance, not profile import |
| Added: plain-text handling | RFCs and arXiv text mirrors are `text/plain`; the original reduced every one of them to zero words |
| Added: charset sniffing, UTF-8 preferred over the ISO-8859-1 fallback | `requests` mangles unlabelled UTF-8, which would corrupt Sanskrit diacritics |
| Added: IPv4-mapped / 6to4 / Teredo unwrapping, `is_global` catch-all | Closes bypasses the original's flag checks left open |
| Added: proxy detection with documented pinning fallback | Pinning is structurally impossible through this environment's proxy |
| Added: egress-403 translated into an actionable finding | `/verify-claims` must distinguish policy denial from a bad citation |
| Added: `--self-test` | The repository has no test suite; the address policy and extractor need a gate |

Upstream licence, reproduced as MIT requires:

```
MIT License

Copyright (c) 2026 Cary Palmer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

The repository's own content is CC BY-NC-SA 4.0; this MIT notice covers the
derived code in `source_capture.py` only.

### Verification

`--self-test` runs offline and gates the two things most worth getting right —
the address policy and the extractor:

- 17 addresses that must be blocked (including `::ffff:127.0.0.1`, a 6to4
  address wrapping `127.0.0.1`, and unparseable input) and 5 that must be
  allowed;
- extraction: title normalisation, `description`/`og:*` metadata with
  first-value-wins, `nav`/`script`/`header`/`footer` stripped, `<article>`
  preferred, unclosed `<p>` and `<li>` handled, entities decoded;
- plain text kept verbatim, HTML mislabelled as `text/plain` still parsed as
  HTML, and binary payloads refused honestly rather than captured empty;
- UTF-8 decoded without a header charset, with **Ahiṃsā** surviving extraction;
- index round-trip: a re-capture updates in place and never duplicates.

Beyond the self-test, the live paths were exercised against a local server:
HTML extraction over real HTTP (diacritics intact with no charset header),
redirect following, the redirect cap, the 1 MB cap, a permitted host redirecting
to `169.254.169.254` being refused mid-chain, and the default policy refusing
`localhost` until `SOURCE_CAPTURE_ALLOW_PRIVATE=1` is set.

Not verified: capture of a real publisher or arXiv page, which this
environment's egress policy blocks. That path is exercised only against the
local server and the few hosts the proxy permits.
