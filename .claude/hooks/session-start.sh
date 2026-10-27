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

# The readiness banner and PM pulse print in EVERY session (local and remote);
# only the LaTeX auto-install below is limited to the remote environment.
REMOTE="${CLAUDE_CODE_REMOTE:-}"

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$ROOT"

echo "── EXSTO-ERGO-SUM session readiness ─────────────────────────"

# Research verification workflow (/verify-claims) runs on MCP tools + these.
command -v node    >/dev/null 2>&1 && echo "  ✓ node    $(node --version)"   || echo "  • node    not present"
command -v python3 >/dev/null 2>&1 && echo "  ✓ python3 $(python3 --version 2>&1)" || echo "  • python3 not present"

# Are there LaTeX sources to build?
TEX_COUNT=$(git ls-files '*.tex' 2>/dev/null | wc -l | tr -d ' ')

if command -v latexmk >/dev/null 2>&1 || command -v pdflatex >/dev/null 2>&1; then
  echo "  ✓ LaTeX   toolchain present"
elif [ "$TEX_COUNT" -gt 0 ] && [ "$REMOTE" != "true" ]; then
  echo "  • LaTeX   $TEX_COUNT .tex source(s), no toolchain — local session, skipping auto-install"
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

# Grok CLI — xAI's terminal agent (`grok`), requested as a standing part of the
# environment. Upstream ships it as `curl -fsSL https://x.ai/cli/install.sh | bash`,
# which is what we try first. In this remote container the egress proxy denies
# x.ai at CONNECT (organization network policy), so we fall back to the same
# binary on npm — @xai-official/grok, published by xai-security <security@x.ai>,
# whose postinstall drops it in ~/.grok/bin exactly as the installer does.
# Both paths are idempotent; the container is ephemeral, so this reruns each session.
GROK_BIN_DIR="${GROK_HOME:-$HOME/.grok}/bin"
case ":$PATH:" in *":$GROK_BIN_DIR:"*) ;; *) PATH="$PATH:$GROK_BIN_DIR" ;; esac
export PATH

if command -v grok >/dev/null 2>&1; then
  echo "  ✓ Grok    $(grok --version 2>/dev/null | head -1)"
elif [ "$REMOTE" != "true" ]; then
  echo "  • Grok    not installed — local session, skipping auto-install"
  echo "             Install with: curl -fsSL https://x.ai/cli/install.sh | bash"
else
  echo "  … Grok    not present — installing the xAI CLI…"
  GROK_VIA=""
  if curl -fsSL --max-time 60 https://x.ai/cli/install.sh 2>/dev/null | bash >/dev/null 2>&1; then
    hash -r 2>/dev/null || true
    command -v grok >/dev/null 2>&1 && GROK_VIA="x.ai installer" || true
  fi
  if [ -z "$GROK_VIA" ] && command -v npm >/dev/null 2>&1; then
    if npm install -g @xai-official/grok >/dev/null 2>&1; then
      hash -r 2>/dev/null || true
      command -v grok >/dev/null 2>&1 && GROK_VIA="npm @xai-official/grok" || true
    fi
  fi
  if [ -n "$GROK_VIA" ]; then
    echo "  ✓ Grok    $(grok --version 2>/dev/null | head -1) (via $GROK_VIA)"
  else
    echo "  ‼ Grok    install failed — x.ai unreachable and the npm fallback did not land"
  fi
fi
if command -v grok >/dev/null 2>&1 && [ -z "${XAI_API_KEY:-}" ] && [ ! -f "${GROK_HOME:-$HOME/.grok}/auth.json" ]; then
  echo "             (unauthenticated — set XAI_API_KEY, or run \`grok\` once to sign in)"
fi

# OptMem — the agent's memory across sessions. The store is in the repo
# (.optmem/memory), so it survives this container; the tool is not, so fetch it
# now rather than paying the latency on the session's first memo call.
if [ -d .optmem/memory ]; then
  if .claude/optmem/memo config >/dev/null 2>&1; then
    MEM_N=$(( $(wc -c < .optmem/memory/LOG.txt 2>/dev/null || echo 0) / 320 ))
    if [ "$MEM_N" -eq 0 ]; then
      echo "  ✓ OptMem  ready, no memories yet — run .claude/optmem/memo wake, then note what matters"
    else
      echo "  ✓ OptMem  $MEM_N memories — run .claude/optmem/memo wake FIRST, before any other tool call"
    fi
  else
    echo "  ‼ OptMem  store present but the tool would not start (no python3, or no network to fetch it)"
  fi
else
  echo "  • OptMem  no store — reinstall with: MEMORY_DIR=\$PWD/.optmem/memory sh -c 'curl -fsSL https://raw.githubusercontent.com/VictorTaelin/OptMem/main/install.sh | sh'"
fi

# PM pulse — surface the latest pm-status graph report (PM-STATUS.md) so every
# session opens knowing the project state, without spawning the fleet.
if [ -f PM-STATUS.md ]; then
  PM_STATE=$(grep -m1 '\*\*Overall state:' PM-STATUS.md 2>/dev/null | sed -e 's/\*//g' -e 's/ — .*//' -e 's/^ *//' || true)
  PM_DATE=$(sed -n 's/.*\*\*Run date:\*\* *\([0-9][0-9-]*\).*/\1/p' PM-STATUS.md 2>/dev/null | head -1 || true)
  PM_WHEN=""
  if [ -n "$PM_DATE" ] && command -v python3 >/dev/null 2>&1; then
    PM_WHEN=$(python3 -c "
import datetime
try:
    d = datetime.date.fromisoformat('$PM_DATE')
    n = (datetime.date.today() - d).days
    print('report from today' if n == 0 else ('report 1 day old' if n == 1 else f'report {n} days old'))
except Exception:
    pass" 2>/dev/null || true)
  fi
  [ -z "$PM_WHEN" ] && PM_WHEN="report dated ${PM_DATE:-unknown}"
  PM_ICON="•"
  case "$PM_STATE" in
    *"needs attention"*) PM_ICON="⚠" ;;
    *"on track"*)        PM_ICON="✓" ;;
  esac
  echo "  $PM_ICON PM      ${PM_STATE:-report present} · $PM_WHEN — run /pm to refresh"
else
  echo "  • PM      no PM-STATUS.md yet — run /pm for the first project pulse"
fi

echo "  Commands: /pm  /verify-claims  /consistency  /submission-check   ·   subagent: reviewer"
echo "─────────────────────────────────────────────────────────────"
