<!-- BEGIN OPTMEM GLOBAL -->
## Memory

Your memory is OptMem, and it is the same memory in every project:

- The tool is `@@MEMO@@`
- Your memories are in `@@STORE@@`

OptMem outlives every session, compaction, model and vendor change. Without it
you do not know who you are, or what was decided and tried.

Use the path above, never `~/.optmem/memo`: the bare tool would read an empty
store in `$HOME`. This store lives in its own git repository so it survives
ephemeral containers and syncs between machines. The wrapper rewrites what
OptMem prints, so any command it hands you is already correct — run it as given.

### At startup: activating OptMem (mandatory)

Run `@@MEMO@@ wake` before any other tool call, in every session, and then do
exactly what it prints, to the end of its output.

### While working: register memories (mandatory)

Call `@@MEMO@@ note "<1 line, max 280 bytes>"` whenever you learn something
new, or something worth keeping happens. That covers a task worth real effort,
a fact or insight the user teaches you, anything you learn about their life
(even indirectly), any event of lasting effect.

Because this memory spans every project, say *which* project a memory belongs
to when it is not obvious. A memory that reads "the build is broken" is
worthless six repositories later.

Do not register redundant memories.

If `@@MEMO@@ note` asks a compression: do it before your next action.

Never edit or delete anything under the store: the tool manages it. A
SessionStart hook pulls it and a Stop hook commits and pushes it, so memories
sync between machines on their own.

### When you need an old memory: search, or navigate

`@@MEMO@@ recall <regex>` searches every memory, word for word.

Your memories also form a binary tree: #0-1, #2-3 ... exist as one-line
summaries, pairs of those as #0-3, and so on — every `#a-b` line wake prints is
one node of it. `@@MEMO@@ zoom <a-b>` opens a node into its two halves, down to
the raw memories.

### If you're a subagent: skip everything above

Parallel sessions on this machine are all you, and may all write memories. A
subagent is not: it must never run `memo`, because it cannot judge what is
already known, and its notes would arrive duplicated and incorrectly. When you
spawn one, write: `You are a subagent. Don't run memo.`
<!-- END OPTMEM GLOBAL -->
