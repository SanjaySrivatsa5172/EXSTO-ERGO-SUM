#!/usr/bin/env bash
# Stop hook: commit OptMem memory so a session's memories survive the machine.
#
# Memories are written to .optmem/memory/ during the session. In a remote
# container an uncommitted file is gone when the container is reclaimed, and
# the agent that wrote the memory is not always the one that remembers to
# commit it. So this runs at the end of every session and commits the memory
# store — and nothing else.
#
# It commits only; it never pushes. The memory commit rides along with the
# next `git push` of the branch you are already working on.
set -euo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$ROOT" || exit 0

git rev-parse --git-dir >/dev/null 2>&1 || exit 0
[ -d .optmem/memory ] || exit 0

# Never commit to main — this repo's rule is that work lands on a claude/…
# branch. Say so rather than failing silently, so the memories can be moved.
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')"
if [ "$BRANCH" = "main" ]; then
  if ! git diff --quiet -- .optmem/memory 2>/dev/null ||
     [ -n "$(git ls-files --others --exclude-standard -- .optmem/memory)" ]; then
    echo "optmem: new memories on main, left uncommitted — switch to a branch and commit .optmem/memory" >&2
  fi
  exit 0
fi

# A merge/rebase in progress owns the index; don't add commits under it.
GIT_DIR="$(git rev-parse --git-dir)"
for state in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD; do
  [ -e "$GIT_DIR/$state" ] && exit 0
done

git add -- .optmem/memory 2>/dev/null || exit 0

# --cached against HEAD: is there actually anything of ours to commit?
if git diff --cached --quiet -- .optmem/memory 2>/dev/null; then
  exit 0
fi

# New memories are lines appended to LOG.txt; a compression writes only to
# TREE/. Both are worth committing, but only the first is "a new memory".
COUNT="$(git diff --cached --numstat -- .optmem/memory/LOG.txt 2>/dev/null | awk '{print $1}')"
COUNT="${COUNT:-0}"
case "$COUNT" in
  0) SUBJECT="memory: compress summaries" ;;
  1) SUBJECT="memory: record 1 new memory" ;;
  *) SUBJECT="memory: record $COUNT new memories" ;;
esac

# `commit -- <path>` commits those paths only, leaving anything else the
# session has staged untouched and uncommitted.
git commit --quiet --no-verify -m "$SUBJECT" -- .optmem/memory 2>/dev/null &&
  echo "optmem: committed memory ($SUBJECT) — push the branch to persist it." >&2

exit 0
