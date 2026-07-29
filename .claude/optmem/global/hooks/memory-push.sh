#!/usr/bin/env bash
# Stop hook (global): commit and push the shared memory store.
#
# The repo-scoped version of this hook commits but never pushes, because the
# memories ride along with the next push of the branch you are already on.
# Here there is no such branch: the memory store is its own repository that
# nobody else pushes. If this hook does not push, a memory written in a
# container dies with it. So this one pushes.
#
# Runs in EVERY Claude Code session. Fast, quiet, always exits 0.
#
# Installed by .claude/optmem/global/install.sh, which substitutes the store
# path below. Edit the template, re-run the installer — not this copy.
set -uo pipefail

MEM="@@MEMREPO@@"

[ -d "$MEM/.git" ] || exit 0
command -v git >/dev/null 2>&1 || exit 0

# A merge/rebase in progress owns the index; don't add commits under it.
GIT_DIR="$(git -C "$MEM" rev-parse --git-dir 2>/dev/null)" || exit 0
case "$GIT_DIR" in /*) ;; *) GIT_DIR="$MEM/$GIT_DIR" ;; esac
for state in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD; do
  [ -e "$GIT_DIR/$state" ] && exit 0
done

git -C "$MEM" add -- .optmem/memory >/dev/null 2>&1 || exit 0

if ! git -C "$MEM" diff --cached --quiet -- .optmem/memory 2>/dev/null; then
  # New memories are lines appended to LOG.txt; a compression writes only to
  # TREE/. Both are worth committing, but only the first is "a new memory".
  COUNT="$(git -C "$MEM" diff --cached --numstat -- .optmem/memory/LOG.txt 2>/dev/null | awk '{print $1}')"
  COUNT="${COUNT:-0}"
  case "$COUNT" in
    0) SUBJECT="memory: compress summaries" ;;
    1) SUBJECT="memory: record 1 new memory" ;;
    *) SUBJECT="memory: record $COUNT new memories" ;;
  esac
  git -C "$MEM" commit --quiet --no-verify -m "$SUBJECT" -- .optmem/memory >/dev/null 2>&1 || exit 0
fi

git -C "$MEM" remote get-url origin >/dev/null 2>&1 || exit 0

# Nothing to push is the common case — say nothing.
[ -z "$(git -C "$MEM" log --oneline @{u}..HEAD 2>/dev/null)" ] && exit 0

if ! git -C "$MEM" push --quiet origin HEAD >/dev/null 2>&1; then
  echo "optmem: memories are committed locally but the push failed — they are" >&2
  echo "optmem: safe on this machine only. Retry: git -C $MEM push origin HEAD" >&2
fi

exit 0
