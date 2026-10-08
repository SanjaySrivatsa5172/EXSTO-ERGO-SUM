# Setup — two ways to run this vault

These notes are plain Markdown text files. They need *no special app*. Pick one
of the two paths below; you can start with the first and add the second later
with zero migration (same files, nothing to convert).

## Path A — iCloud Drive only (no Obsidian)

1. Drag this folder into **iCloud Drive** (e.g. `iCloud Drive/learning-vault/`).
2. Edit notes in any text editor — TextEdit, VS Code, iA Writer, 1Writer, even
   the Files app on iPhone/iPad. Everything syncs across your devices.
3. `[[double-bracket links]]` show as plain text — that's fine, they still tell
   you (and Claude) what connects to what.

**What you give up:** the visual graph view and clickable backlinks. Nothing
else — the learning happens in the writing and the Claude prompts, not the app.

## Path B — Obsidian on top of iCloud (optional, free)

1. Do Path A first (files live in iCloud).
2. Install **Obsidian** (free), choose *Open folder as vault*, and point it at the
   same iCloud folder.
3. You now get clickable `[[links]]`, a **graph view**, and a backlinks panel.

Obsidian stores nothing of its own beyond a hidden `.obsidian/` config folder —
your notes stay portable plain Markdown. You can stop using it any time and the
files are unchanged.

> **iCloud Drive = where the files live. Obsidian = an optional lens for the graph.**

## One thing either way: let Claude reach the files

To run the daily and synthesis prompts (see `README.md`), Claude needs to read the
notes. Two options:
- **Paste** the relevant note(s) into the chat, or
- Work in a **local synced copy** of the folder that Claude can read directly.

The graph doesn't care which app you use — only that the text is reachable.
