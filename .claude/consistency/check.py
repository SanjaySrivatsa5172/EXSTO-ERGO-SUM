#!/usr/bin/env python3
"""Deterministic consistency signal for the EXSTO ERGO SUM document set.

This is the mechanical half of the `/consistency` skill. It does NOT decide
what is correct — it computes the *distribution* of version strings, counts,
Sanskrit transliterations, and cross-references across `derived/*.txt` and
`README.md`, and flags the anomalies a human or Claude should then judge.

Design (ported from the CUDA Agent paper's "reliable signal, agent judges"
split): a changelog legitimately names old versions and a proposal names a
future one, so the script never demands uniformity. It reports where each value
appears and highlights the minority / out-of-range / folded cases as review
candidates. The `/consistency` skill reads this output and reasons about it;
the author sets the canonical value.

Report-only. Never edits. Exit code 0 = no anomalies, 1 = anomalies to review
(so it can gate CI later), 2 = could not run (missing inputs).

Usage:
    python3 .claude/consistency/check.py            # scan the standard set
    python3 .claude/consistency/check.py <files...> # scan specific files
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# The standard submission set: plain-text mirrors plus the primary editable.
DEFAULT_TARGETS = [
    REPO / "README.md",
    *sorted((REPO / "derived").glob("*.txt")),
]

# ── Canonical facts (single source of truth for the checks) ──────────────────
# Sanskrit terms that carry a *required* diacritic form. Base words that are
# correct in bare ASCII (Dharma, Karma, Viveka, Yoga …) are deliberately absent
# — flagging them would be noise. Map: canonical form -> folded regex to catch.
SANSKRIT = {
    "Ahiṃsā": r"\bAhimsa\b",
    "Saṃskāra": r"\bSamskara\b",
    "Vyākaraṇa": r"\bVyakarana\b",
    "Ānanda": r"\bAnanda\b",
    "Māyā": r"\bMaya\b",
    "Sākṣin": r"\bSaksin\b",
    "Pañca": r"\bPanca\b",
    "kṣetra": r"\bksetra\b",
}

# Cross-reference bands documented in CLAUDE.md: Online Resources run OR01–OR49.
OR_MIN, OR_MAX = 1, 49

WORD_NUMBERS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "forty-three": 43,
}

# Nouns whose preceding count we track, with the value expected to dominate.
# (expected is a hint for the report, not an assertion of correctness.)
COUNT_NOUNS = {
    "articles": 43,
    "Parts": 17,
    "pillars": 5,
    "wisdom traditions": 7,
}


def load(targets):
    docs = {}
    for p in targets:
        try:
            # split("\n"), not splitlines(): pdfminer leaves form-feed (\x0c)
            # page breaks in the text, and splitlines() would split on those too,
            # throwing every reported line number out of sync with sed/editors.
            docs[p] = p.read_text(encoding="utf-8", errors="replace").split("\n")
        except OSError as e:
            print(f"  ! could not read {p}: {e}", file=sys.stderr)
    return docs


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO))
    except ValueError:
        return str(p)


# ── Checks ───────────────────────────────────────────────────────────────────

def check_version(docs) -> list[str]:
    """Every vN.NN occurrence, with the declared current version highlighted."""
    findings = []
    current = None
    for lines in docs.values():
        for ln in lines:
            m = re.search(r"[Cc]urrent version:?\s*v?(\d+\.\d+)", ln)
            if m:
                current = m.group(1)
                break
        if current:
            break

    # Collect all version-like tokens, excluding license/badge noise.
    hits = defaultdict(list)  # version -> [(file, lineno)]
    ver_re = re.compile(r"\bv(\d+\.\d+)\b")
    for p, lines in docs.items():
        for i, ln in enumerate(lines, 1):
            low = ln.lower()
            if "cc by" in low or "by-nc" in low or "shields.io" in low or "badge" in low:
                continue
            for m in ver_re.finditer(ln):
                hits[m.group(1)].append((rel(p), i))

    if not hits:
        return findings

    findings.append(f"Declared current version: v{current}" if current
                    else "No 'Current version:' declaration found — cannot anchor drift check.")

    def vkey(v):  # numeric sort, e.g. 3.9 < 3.67 handled as tuple
        return tuple(int(x) for x in v.split("."))

    for v in sorted(hits, key=vkey):
        locs = hits[v]
        tag = ""
        if current and v == current:
            tag = "  ← current"
        elif current and vkey(v) > vkey(current):
            tag = "  ⚠ HIGHER than current — future/proposal or drift?"
        sample = ", ".join(f"{f}:{n}" for f, n in locs[:4])
        more = f" (+{len(locs) - 4} more)" if len(locs) > 4 else ""
        findings.append(f"  v{v}  ×{len(locs)}{tag}\n      {sample}{more}")
    return findings


def check_counts(docs) -> list[str]:
    """Distribution of the number preceding each tracked noun."""
    findings = []
    for noun, expected in COUNT_NOUNS.items():
        # \b before the alternation stops word-numbers matching inside longer
        # words (e.g. "eight" inside "weight pillars").
        pat = re.compile(
            r"\b([0-9]+|" + "|".join(WORD_NUMBERS) + r")[\s-]+" + re.escape(noun),
            re.IGNORECASE,
        )
        dist = defaultdict(list)  # value -> [(file,lineno,raw)]
        for p, lines in docs.items():
            for i, ln in enumerate(lines, 1):
                for m in pat.finditer(ln):
                    raw = m.group(1).lower()
                    val = int(raw) if raw.isdigit() else WORD_NUMBERS.get(raw)
                    # Guard against 4-digit years ("2026 ... articles") — no count
                    # noun here is anywhere near the hundreds, so drop >= 1000.
                    if val is not None and val < 1000:
                        dist[val].append((rel(p), i))
        if not dist:
            continue
        values = sorted(dist)
        if len(values) == 1 and values[0] == expected:
            findings.append(f"  '{noun}': all {len(dist[values[0]])} mention(s) = {values[0]} ✓")
        else:
            findings.append(f"  '{noun}': expected {expected}, found {len(values)} distinct value(s):")
            for v in values:
                locs = dist[v]
                flag = "" if v == expected else "  ⚠ differs from expected"
                sample = ", ".join(f"{f}:{n}" for f, n in locs[:3])
                more = f" (+{len(locs) - 3})" if len(locs) > 3 else ""
                findings.append(f"      {v}: ×{len(locs)}{flag}  [{sample}{more}]")
    return findings


def check_sanskrit(docs) -> list[str]:
    """ASCII-folded forms of terms that require diacritics — review candidates."""
    findings = []
    for canon, folded_re in SANSKRIT.items():
        pat = re.compile(folded_re)
        locs = []
        for p, lines in docs.items():
            for i, ln in enumerate(lines, 1):
                if pat.search(ln):
                    locs.append((rel(p), i))
        if locs:
            sample = ", ".join(f"{f}:{n}" for f, n in locs[:5])
            more = f" (+{len(locs) - 5} more)" if len(locs) > 5 else ""
            findings.append(
                f"  '{canon}' appears ASCII-folded ×{len(locs)} — verify each is a "
                f"code/URL identifier, else restore diacritics\n      {sample}{more}"
            )
    return findings


def check_crossrefs(docs) -> list[str]:
    """Online Resource numbers outside the documented OR01–OR49 band."""
    findings = []
    pat = re.compile(r"Online Resource\s+(\d+)")
    bad = []
    for p, lines in docs.items():
        for i, ln in enumerate(lines, 1):
            for m in pat.finditer(ln):
                n = int(m.group(1))
                if not (OR_MIN <= n <= OR_MAX):
                    bad.append((n, rel(p), i))
    if bad:
        for n, f, i in bad[:20]:
            findings.append(f"  Online Resource {n} out of band {OR_MIN}–{OR_MAX}  [{f}:{i}]")
        if len(bad) > 20:
            findings.append(f"  (+{len(bad) - 20} more out-of-band references)")
    return findings


def main(argv) -> int:
    targets = [Path(a) for a in argv] if argv else DEFAULT_TARGETS
    targets = [t for t in targets if t.exists()]
    if not targets:
        print("No target files found. Run from the repo, or pass files explicitly.", file=sys.stderr)
        return 2

    docs = load(targets)
    if not docs:
        return 2

    print("EXSTO ERGO SUM — consistency signal (report-only)")
    print(f"Scanned {len(docs)} file(s): {', '.join(rel(p) for p in docs)}")
    print("=" * 70)

    sections = [
        ("VERSION STRINGS", check_version),
        ("COUNTS (articles / Parts / pillars / traditions)", check_counts),
        ("SANSKRIT TRANSLITERATION", check_sanskrit),
        ("CROSS-REFERENCES (Online Resource band)", check_crossrefs),
    ]

    anomalies = 0
    for title, fn in sections:
        findings = fn(docs)
        print(f"\n## {title}")
        if not findings:
            print("  (nothing to report)")
            continue
        # A finding line containing a warning/mismatch marker counts as anomaly.
        for line in findings:
            print(line)
        if any(("⚠" in ln or "out of band" in ln or "ASCII-folded" in ln
                or "expected" in ln or "HIGHER" in ln) for ln in findings):
            anomalies += 1

    print("\n" + "=" * 70)
    if anomalies:
        print(f"RESULT: {anomalies} category(ies) have items to review. "
              "These are candidates, not verdicts — judge each in context.")
        return 1
    print("RESULT: no anomalies surfaced by the mechanical checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
