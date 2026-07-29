# OptMem everywhere: one memory across every Claude Code project

The setup in this repository's `CLAUDE.md` is repo-scoped — OptMem only wakes
when Claude is working *inside* EXSTO-ERGO-SUM. This directory makes it the
memory of **every** Claude Code session on a machine, in any project.

Nothing here runs automatically. It is installed per machine, by you.

## What it installs

| Path | |
|---|---|
| `~/claude-memory/` | the store, as a git repo of its own (path configurable) |
| `~/claude-memory/.claude/optmem/memo` | the wrapper — a copy, not a fork |
| `~/claude-memory/.claude/hooks/` | `memory-pull.sh`, `memory-push.sh` |
| `~/.claude/CLAUDE.md` | the prompt block, between `OPTMEM GLOBAL` markers |
| `~/.claude/settings.json` | registers the two hooks globally |

The store repo deliberately mirrors this repo's layout (`.claude/optmem/memo`
beside `.optmem/memory/`). The wrapper resolves its store as
`$HERE/../../.optmem/memory`, so the **same wrapper works unmodified** in both
places — there is no second copy to keep in sync.

## Install

```bash
# 1. Create a PRIVATE, EMPTY repo (no README — an empty remote can't be cloned)
# 2. On the first machine, seeding from this repo's existing memories:
.claude/optmem/global/install.sh \
    --remote git@github.com:<you>/claude-memory.git \
    --seed-from /path/to/EXSTO-ERGO-SUM
git -C ~/claude-memory push -u origin HEAD

# 3. On every other machine — clone, don't seed:
.claude/optmem/global/install.sh --remote git@github.com:<you>/claude-memory.git
```

`--dry-run` prints what would happen and writes nothing. Re-running is a no-op
that upgrades the wrapper, hooks and prompt block; it never overwrites a
non-empty store and never deletes a memory.

## How syncing works

`SessionStart` pulls, `Stop` commits and pushes. A memory written on the
desktop is visible on the Mac at the start of its next session.

The pull is `--ff-only` **on purpose**. OptMem records are fixed-width lines
numbered `#0, #1, …`. If two machines each append while the other is offline,
both create a `#14`, and *any* automatic merge — git's `union` driver
included — yields duplicate indices that no longer match the `TREE` summaries.
So a diverged store is refused, loudly, with both sides listed; nothing is
merged and nothing is lost. Resolve it by keeping one side and re-noting the
other's memories.

In practice divergence needs two machines writing memories in overlapping
sessions. Working on one machine at a time never triggers it.

## Limits worth knowing before you rely on it

- **Remote / web Claude Code sessions** (like the container this was built in)
  have neither `~/.claude` nor the memory repo — they are built fresh from the
  session's sources. For those sessions to share the global memory, add
  `claude-memory` as a **second source** on the environment. Until you do,
  web sessions on this repo keep using the repo-local `.optmem/memory`, and
  the two stores drift apart for EXSTO memories.
- **Windows**: the wrapper is bash, so it needs Git Bash or WSL. OptMem itself
  is Windows-native (`python memo`); only the wrapper is the obstacle. A
  `.ps1` companion is deliberately unbuilt.
- **claude.ai chat** has no shell and cannot run this at all — by decision, it
  uses its own native memory instead.
- The hooks are global, so they run for every project. Both exit 0 on every
  path and stay silent unless something needs your attention.

## After installing: this repo's own block

Once the global store is authoritative, this repo's `CLAUDE.md` "Memory"
section becomes a second, competing store. Either delete that section and add
`claude-memory` as a source to the web environment (one memory, everywhere),
or keep it and accept that web sessions on this repo remember separately.
Don't leave both live on the same machine without deciding which one wins.
