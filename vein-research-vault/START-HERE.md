# START HERE — using Claude with this folder on your Mac

This folder is your venous research vault. Here is the whole workflow. No Obsidian,
no Git, no extra apps — just Claude running on your Mac, working on these files,
which sync to your iPhone through iCloud automatically.

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
2. Open **Finder → iCloud Drive**, find this **Venous Research** folder, and **drag it
   onto the Terminal window.** The full path fills in by itself. Press Enter.
3. Type `claude` and press Enter.

Claude is now "inside" this folder and can read and write every file in it.

---

## Things you can just ask it to do

- "Read every PDF in here and give me a one-page summary of each."
- "Create a concept note for this paper and link it to the related notes."
- "Organize these files into subfolders by topic."
- "Find where two of my studies contradict each other and tell me what trial would settle it."
- "Update the review dates on the notes due this week."

It works on your real files. Whatever it changes shows up on your iPhone within seconds.

---

## How this vault is organized (optional — you can ignore it)

- `findings/` — one note per concept, study, finding, or hypothesis.
- `synthesis/` — longer integrated write-ups Claude produces on request.
- `CLAUDE.md` — instructions Claude reads automatically so it knows how to help here.
- `_finding-template.md` — the blank note format, if you want to add one by hand.
- `README.md` — the fuller explanation of the method and the two prompts.

You do not have to learn any of this. You can just talk to Claude in plain English
and let it handle the structure.

---

## The one thing to remember

**The Mac does the work; the iPhone shows the results.** Apple won't let any app
(Claude included) roam your iCloud files from an iPhone, so run Claude on the Mac.
Everything it produces syncs to your phone automatically for reading anywhere.
