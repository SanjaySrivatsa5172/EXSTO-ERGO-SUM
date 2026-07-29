#!/usr/bin/env bash
# Make OptMem the memory of EVERY Claude Code session on this machine, in any
# project — not just this repository.
#
# What it sets up:
#
#   <store>/                      a git repo of its own, the one memory
#     .claude/optmem/memo         the wrapper (same layout as this repo, so
#                                 the canonical wrapper works unmodified)
#     .claude/hooks/              pull-at-start, commit-and-push-at-stop
#     .optmem/memory/             LOG.txt, TREE/, config
#   ~/.claude/CLAUDE.md           the block that makes Claude use it, in every
#                                 project, before any other tool call
#   ~/.claude/settings.json       registers the two hooks globally
#
# Idempotent: safe to re-run to upgrade the wrapper, hooks, or prompt block.
# It never deletes memories, and never overwrites a non-empty store.
#
# Usage:
#   .claude/optmem/global/install.sh [--dir PATH] [--remote URL]
#                                    [--seed-from PATH] [--dry-run]
#
#   --dir PATH        where the memory repo lives (default ~/claude-memory)
#   --remote URL      the private git remote to sync through; cloned if the
#                     store does not exist yet, otherwise set as origin
#   --seed-from PATH  copy an existing .optmem/memory into a NEW store, e.g.
#                     --seed-from /path/to/EXSTO-ERGO-SUM
#   --dry-run         print what would happen; touch nothing
set -euo pipefail

HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
WRAPPER="$HERE/../memo"
BLOCK="$HERE/CLAUDE.md"

MEM="${HOME}/claude-memory"
REMOTE=""
SEED=""
DRY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --dir)       MEM="${2:?--dir needs a path}"; shift 2 ;;
    --remote)    REMOTE="${2:?--remote needs a URL}"; shift 2 ;;
    --seed-from) SEED="${2:?--seed-from needs a path}"; shift 2 ;;
    --dry-run)   DRY=1; shift ;;
    -h|--help)   sed -n '2,30p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "install: unknown argument: $1" >&2; exit 2 ;;
  esac
done

say()  { echo "  $*"; }
run()  { if [ "$DRY" = 1 ]; then echo "  would: $*"; else "$@"; fi; }

command -v git     >/dev/null 2>&1 || { echo "install: needs git" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "install: needs python3" >&2; exit 1; }
[ -f "$WRAPPER" ] || { echo "install: cannot find the wrapper at $WRAPPER" >&2; exit 1; }
[ -f "$BLOCK" ]   || { echo "install: cannot find the prompt block at $BLOCK" >&2; exit 1; }

MEM="$(python3 -c 'import os,sys; print(os.path.abspath(os.path.expanduser(sys.argv[1])))' "$MEM")"
MEMO="$MEM/.claude/optmem/memo"
STORE="$MEM/.optmem/memory"

echo "OptMem — global install"
say "store repo: $MEM"
[ "$DRY" = 1 ] && say "(dry run — nothing will be written)"

# ---------------------------------------------------------------- store repo
if [ ! -d "$MEM/.git" ]; then
  if [ -n "$REMOTE" ] && [ ! -e "$MEM" ]; then
    say "cloning $REMOTE"
    run git clone --quiet -- "$REMOTE" "$MEM" || {
      echo "install: clone failed. If the remote is empty, create it without a" >&2
      echo "install: README and re-run — an empty remote cannot be cloned." >&2
      exit 1
    }
  else
    say "creating a new memory repo"
    run mkdir -p -- "$MEM"
    run git -C "$MEM" init --quiet
    [ -n "$REMOTE" ] && run git -C "$MEM" remote add origin "$REMOTE"
  fi
elif [ -n "$REMOTE" ]; then
  if git -C "$MEM" remote get-url origin >/dev/null 2>&1; then
    run git -C "$MEM" remote set-url origin "$REMOTE"
  else
    run git -C "$MEM" remote add origin "$REMOTE"
  fi
  say "origin set to $REMOTE"
fi

run mkdir -p -- "$MEM/.claude/optmem" "$MEM/.claude/hooks" "$STORE"

# ------------------------------------------------------------------- wrapper
say "installing the wrapper"
run cp -- "$WRAPPER" "$MEMO"
run chmod +x -- "$MEMO"

# Records are fixed width — position is identity, so EOL normalization would
# corrupt every lookup. This must exist in the store repo, not just this one.
if [ "$DRY" = 0 ]; then
  cat > "$MEM/.gitattributes" <<'EOF'
# OptMem records are fixed width — position is identity, so a single byte of
# EOL normalization would corrupt every lookup. Keep them exactly as written.
.optmem/memory/LOG.txt   -text
.optmem/memory/TREE/**   -text
EOF
  printf '%s\n' '.optmem/memory/.lock' > "$MEM/.gitignore"
else
  say "would: write .gitattributes and .gitignore"
fi

# --------------------------------------------------------------------- seed
if [ -n "$SEED" ]; then
  SRC="$SEED"
  [ -d "$SRC/.optmem/memory" ] && SRC="$SRC/.optmem/memory"
  if [ ! -f "$SRC/LOG.txt" ]; then
    echo "install: no LOG.txt under $SEED — nothing to seed from" >&2
    exit 1
  fi
  if [ -s "$STORE/LOG.txt" ]; then
    say "store already holds memories — NOT seeding (nothing overwritten)"
  else
    say "seeding from $SRC"
    run cp -- "$SRC/LOG.txt" "$STORE/LOG.txt"
    [ -f "$SRC/config" ] && run cp -- "$SRC/config" "$STORE/config"
    [ -d "$SRC/TREE" ] && run cp -R -- "$SRC/TREE" "$STORE/TREE"
  fi
fi

# --------------------------------------------------------------------- hooks
say "installing hooks"
for h in memory-pull memory-push; do
  if [ "$DRY" = 0 ]; then
    sed -e "s|@@MEMREPO@@|$MEM|g" "$HERE/hooks/$h.sh" > "$MEM/.claude/hooks/$h.sh"
    chmod +x "$MEM/.claude/hooks/$h.sh"
  else
    say "would: install $h.sh"
  fi
done

# ------------------------------------------------------------ ~/.claude/CLAUDE.md
say "writing the prompt block into ~/.claude/CLAUDE.md"
if [ "$DRY" = 0 ]; then
  mkdir -p "$HOME/.claude"
  MEMO="$MEMO" STORE="$STORE" BLOCK="$BLOCK" TARGET="$HOME/.claude/CLAUDE.md" python3 - <<'PY'
import os, re, pathlib
memo, store = os.environ["MEMO"], os.environ["STORE"]
block = pathlib.Path(os.environ["BLOCK"]).read_text(encoding="utf-8")
block = block.replace("@@MEMO@@", memo).replace("@@STORE@@", store)
target = pathlib.Path(os.environ["TARGET"])
old = target.read_text(encoding="utf-8") if target.exists() else ""
pat = re.compile(r"<!-- BEGIN OPTMEM GLOBAL -->.*?<!-- END OPTMEM GLOBAL -->\n?",
                 re.DOTALL)
new = pat.sub(block, old) if pat.search(old) else (
    (old.rstrip("\n") + "\n\n" if old.strip() else "") + block)
target.write_text(new, encoding="utf-8")
PY
fi

# ----------------------------------------------------- ~/.claude/settings.json
say "registering the hooks in ~/.claude/settings.json"
if [ "$DRY" = 0 ]; then
  MEM="$MEM" TARGET="$HOME/.claude/settings.json" python3 - <<'PY'
import json, os, pathlib
mem = os.environ["MEM"]
target = pathlib.Path(os.environ["TARGET"])
try:
    cfg = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
    if not isinstance(cfg, dict):
        raise ValueError("settings.json is not a JSON object")
except Exception as e:
    raise SystemExit(f"install: refusing to touch {target}: {e}")

wanted = {"SessionStart": f"{mem}/.claude/hooks/memory-pull.sh",
          "Stop":         f"{mem}/.claude/hooks/memory-push.sh"}
hooks = cfg.setdefault("hooks", {})
for event, cmd in wanted.items():
    groups = hooks.setdefault(event, [])
    if any(h.get("command") == cmd
           for g in groups if isinstance(g, dict)
           for h in g.get("hooks", []) if isinstance(h, dict)):
        continue                      # already registered — re-run is a no-op
    groups.append({"hooks": [{"type": "command", "command": cmd}]})

target.parent.mkdir(parents=True, exist_ok=True)
tmp = target.with_suffix(".json.optmem-tmp")
tmp.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
tmp.replace(target)                   # atomic: never a half-written settings file
PY
fi

# --------------------------------------------------------------------- commit
if [ "$DRY" = 0 ] && [ -d "$MEM/.git" ]; then
  git -C "$MEM" add -A >/dev/null 2>&1 || true
  git -C "$MEM" diff --cached --quiet 2>/dev/null ||
    git -C "$MEM" commit --quiet --no-verify -m "Set up OptMem as the global memory store" >/dev/null 2>&1 || true
fi

echo
echo "Done. Check it with:"
echo "  $MEMO wake"
if [ -z "$REMOTE" ] && ! git -C "$MEM" remote get-url origin >/dev/null 2>&1; then
  echo
  echo "No remote is set, so this memory stays on this machine. To sync it,"
  echo "create a PRIVATE, EMPTY repo and re-run with:"
  echo "  $0 --remote git@github.com:<you>/claude-memory.git"
else
  echo "  git -C $MEM push -u origin HEAD    # first push"
fi
