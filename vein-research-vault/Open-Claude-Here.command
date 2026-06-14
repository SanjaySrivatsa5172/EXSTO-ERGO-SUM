#!/bin/bash
# Double-click this file to open Claude inside this folder — no typing needed.
#
# It works no matter what the folder is named or where it lives, because it
# uses its own location. Keep this file inside the vault folder.
#
# First time only: macOS may say it can't verify the developer. Right-click the
# file → Open → Open. After that, a normal double-click works.

# Move into the folder this script lives in.
cd "$(dirname "$0")" || exit 1

# Make sure Claude is findable even when launched from Finder (Finder uses a
# minimal PATH that may not include where Claude installed itself).
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

clear
echo "Starting Claude in:"
echo "  $(pwd)"
echo

# Helpful message if Claude isn't installed yet.
if ! command -v claude >/dev/null 2>&1; then
  echo "Claude isn't installed yet."
  echo "Install it once by pasting this line into Terminal, then try again:"
  echo
  echo "  curl -fsSL https://claude.ai/install.sh | bash"
  echo
  read -r -p "Press Return to close."
  exit 1
fi

# Replace this script with Claude itself, so the window is clean.
exec claude
