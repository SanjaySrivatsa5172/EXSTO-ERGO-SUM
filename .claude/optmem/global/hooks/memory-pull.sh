#!/usr/bin/env bash
# SessionStart hook (global): bring the shared memory store up to date.
#
# The store is its own git repository, shared by every project and every
# machine. Pulling at the start of a session is what makes a memory written
# on the desktop visible on the laptop an hour later.
#
# This runs in EVERY Claude Code session, so it must be fast, quiet, and
# incapable of blocking a session: every path exits 0.
#
# Installed by .claude/optmem/global/install.sh, which substitutes the store
# path below. Edit the template, re-run the installer — not this copy.
set -uo pipefail

MEM="@@MEMREPO@@"

[ -d "$MEM/.git" ] || exit 0
command -v git >/dev/null 2>&1 || exit 0

# Uncommitted memories from a session that ended badly (Stop hook never ran,
# machine slept, container reclaimed). Committing them here rather than
# pulling on top keeps them from being clobbered by the merge.
if ! git -C "$MEM" diff --quiet -- .optmem/memory 2>/dev/null ||
   [ -n "$(git -C "$MEM" ls-files --others --exclude-standard -- .optmem/memory 2>/dev/null)" ]; then
  git -C "$MEM" add -- .optmem/memory >/dev/null 2>&1
  git -C "$MEM" commit --quiet --no-verify \
    -m "memory: recover memories left uncommitted by a previous session" \
    -- .optmem/memory >/dev/null 2>&1 || true
fi

git -C "$MEM" remote get-url origin >/dev/null 2>&1 || exit 0

# --ff-only on purpose. OptMem records are fixed-width lines numbered #0, #1,
# …; two machines that both appended offline produce two different #14s, and
# any automatic merge (union included) yields duplicate indices that no longer
# match the TREE summaries. Refusing to merge leaves the store intact and
# repairable; merging it silently would not.
if ! git -C "$MEM" pull --ff-only --quiet origin HEAD >/dev/null 2>&1; then
  if git -C "$MEM" fetch --quiet origin >/dev/null 2>&1 &&
     [ -n "$(git -C "$MEM" log --oneline HEAD..@{u} 2>/dev/null)" ] &&
     [ -n "$(git -C "$MEM" log --oneline @{u}..HEAD 2>/dev/null)" ]; then
    echo "optmem: memory store has DIVERGED from its remote — two machines wrote" >&2
    echo "optmem: memories independently. Nothing was merged; the store is intact." >&2
    echo "optmem: see what each side has, then keep one and re-note the other's:" >&2
    echo "optmem:   git -C $MEM log --oneline @{u}..HEAD   # only here" >&2
    echo "optmem:   git -C $MEM log --oneline HEAD..@{u}   # only on the remote" >&2
  else
    echo "optmem: could not reach the memory remote — working from the local store." >&2
  fi
fi

exit 0
