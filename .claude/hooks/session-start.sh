#!/bin/bash
# SessionStart hook for EXSTO-ERGO-SUM.
#
# This is a LaTeX manuscript repo, not a software project — there is no
# package.json / requirements.txt to install. The "build" is a LaTeX compile,
# used by /submission-check. Web sessions are ephemeral, so anything needed must
# be (re)established here.
#
# Design: stay fast. A full TeX Live install is hundreds of MB and is pointless
# when there are no .tex sources to compile (the repo currently ships PDFs only).
# So we install LaTeX ONLY when .tex sources are actually present, and otherwise
# just print a readiness banner. Idempotent and non-interactive.
set -euo pipefail

# Only do work in the remote (Claude Code on the web) environment.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$ROOT"

echo "── EXSTO-ERGO-SUM session readiness ─────────────────────────"

# Research verification workflow (/verify-claims) runs on MCP tools + these.
command -v node    >/dev/null 2>&1 && echo "  ✓ node    $(node --version)"   || echo "  • node    not present"
command -v python3 >/dev/null 2>&1 && echo "  ✓ python3 $(python3 --version 2>&1)" || echo "  • python3 not present"

# Pandoc — universal document converter. Used for format conversions between the
# repo's prose artifacts: Markdown ⇄ LaTeX ⇄ HTML/DOCX/PDF, and cleaner text
# extraction than pdftotext for any future .tex/.md sources. It is a small
# package (unlike TeX Live), so install it unconditionally when missing.
# Idempotent and non-interactive; an install hiccup must not abort session start.
if command -v pandoc >/dev/null 2>&1; then
  echo "  ✓ pandoc  $(pandoc --version 2>/dev/null | head -1 | awk '{print $2}')"
else
  echo "  … pandoc  not present — installing…"
  export DEBIAN_FRONTEND=noninteractive
  if apt-get update -qq && apt-get install -y -qq --no-install-recommends pandoc >/dev/null 2>&1; then
    echo "  ✓ pandoc  installed ($(pandoc --version 2>/dev/null | head -1 | awk '{print $2}'))"
  else
    echo "  ‼ pandoc  install failed — install by hand with: apt-get install -y pandoc"
  fi
fi

# Are there LaTeX sources to build?
TEX_COUNT=$(git ls-files '*.tex' 2>/dev/null | wc -l | tr -d ' ')

if command -v latexmk >/dev/null 2>&1 || command -v pdflatex >/dev/null 2>&1; then
  echo "  ✓ LaTeX   toolchain present"
elif [ "$TEX_COUNT" -gt 0 ]; then
  echo "  … LaTeX   $TEX_COUNT .tex source(s) found, no toolchain — installing TeX Live (recommended set)…"
  export DEBIAN_FRONTEND=noninteractive
  # Don't let an install hiccup abort the whole session start.
  if apt-get update -qq && apt-get install -y -qq --no-install-recommends \
       latexmk texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended >/dev/null 2>&1; then
    echo "  ✓ LaTeX   installed ($(pdflatex --version 2>/dev/null | head -1))"
  else
    echo "  ‼ LaTeX   install failed — run /submission-check manually or install texlive by hand"
  fi
else
  echo "  • LaTeX   skipped — no .tex sources tracked yet (repo ships PDFs only)."
  echo "             Add .tex sources and the next session will install the toolchain automatically."
fi

echo "  Commands: /verify-claims  /consistency  /submission-check   ·   subagent: reviewer"
echo "─────────────────────────────────────────────────────────────"
