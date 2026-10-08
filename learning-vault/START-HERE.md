# START HERE — using Claude with this folder on your Mac

This folder is your learning vault — for studying a subject deeply, not research
data. Here is the whole workflow. No Obsidian, no Git, no extra apps — just Claude
running on your Mac, working on these files, which sync to your iPhone through
iCloud automatically.

---

## One-time setup (about 10 minutes, do once)

1. **Open Terminal.** Press `⌘ + Space`, type **Terminal**, press Enter.
2. **Install Claude Code.** Paste this and press Enter:
   ```
   curl -fsSL https://claude.ai/install.sh | bash
   ```
   *(If it says it needs something else, try: `npm install -g @anthropic-ai/claude-code`)*
3. **Start it and log in.** Type `claude` and press Enter. The first time, it opens
   your browser to sign in with your Claude account. You only do this once.

---

## Every time you want Claude to work on this folder

1. In Terminal, type `cd ` (the letters **c**, **d**, then a **space**).
2. Open **Finder → iCloud Drive**, find this **Learning Vault** folder, and **drag it
   onto the Terminal window.** The full path fills in by itself. Press Enter.
3. Type `claude` and press Enter.

Claude is now "inside" this folder and can read and write every file in it.

---

## The learning loop (what makes this work)

1. **You** write a concept in your own words (copy `_concept-template.md` into
   `concepts/`). Where you get stuck is the thing you don't understand yet.
2. **Ask Claude** to connect it to your other notes and write recall questions:
   *"Link this note to related ones and give me application questions."*
3. **You** answer the questions cold — before re-reading — then check.
4. Every couple of weeks: *"Run a synthesis session on [subject]."*

The whole point is active recall + spaced review. Claude does the connecting,
questioning, and scheduling; you do the writing and the answering.

---

## How this vault is organized (optional)

- `concepts/` — one note per idea.
- `synthesis/` — integrated write-ups Claude produces on request.
- `CLAUDE.md` — instructions Claude reads automatically.
- `_concept-template.md` — the blank note format.
- `README.md` — the fuller method and the two prompts.

---

## The one thing to remember

**The Mac does the work; the iPhone shows the results.** Apple won't let any app
(Claude included) roam your iCloud files from an iPhone, so run Claude on the Mac.
Everything it produces syncs to your phone automatically for reading anywhere.
