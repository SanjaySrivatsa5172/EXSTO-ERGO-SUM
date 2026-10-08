---
name: youtube-search
description: Search YouTube and return structured, ranked video results with engagement metrics. Use when the user wants to find, research, or compare YouTube videos by query or topic, or analyze view counts, subscriber counts, and view-to-subscriber engagement ratios. Returns the top 20 results by default, filtered to recent uploads (default last 6 months, adjustable), with human-readable per-video metadata: title, channel name, subscriber count, view count, duration, upload date, URL, and a views-to-subscribers ratio. Built on yt-dlp.
---

# YouTube Search

Search YouTube for videos matching a query and return clean, structured results
with an engagement metric. This skill wraps `yt-dlp` (no API key required).

## When to use

- The user wants to find or research YouTube videos on a topic.
- The user wants to compare channels or gauge how a video is performing relative
  to the channel's audience (views-to-subscribers ratio).
- The user wants recent videos (defaults to the last 6 months).

## Prerequisite: yt-dlp

The skill requires `yt-dlp` on PATH. Check and install if missing:

```bash
yt-dlp --version || pip install -U yt-dlp
```

(`pipx install yt-dlp` or `brew install yt-dlp` also work.)

## Usage

Run the helper script with a query:

```bash
python3 scripts/search_youtube.py "QUERY"
```

Use the path relative to this skill's directory. Common options:

| Flag        | Default      | Meaning                                                        |
|-------------|--------------|----------------------------------------------------------------|
| `--limit`   | `20`         | Number of results to return.                                   |
| `--months`  | `6`          | Only include uploads from the last N months. `0` = no filter.  |
| `--pool`    | `limit * 3`  | Candidates fetched before date-filtering. Raise for coverage.  |

### Examples

```bash
# Default: top 20, last 6 months
python3 scripts/search_youtube.py "claude code tutorial"

# Top 10 from the last year
python3 scripts/search_youtube.py "rust async" --limit 10 --months 12

# Very recent, wider candidate pool to fill the list
python3 scripts/search_youtube.py "nba highlights" --months 1 --pool 90

# No date filter at all
python3 scripts/search_youtube.py "lofi study mix" --months 0
```

## Output

Each result is printed with dividers and human-readable numbers (e.g. `1.2M`
views, `8:42` duration, `2024-11-03` upload date). The **Views/Subs** line is the
engagement metric: `view_count / channel_follower_count`, shown as e.g. `3.40x`
(the video earned ~3.4 views per subscriber).

## Notes & behavior

- **Recency vs. completeness:** date filtering is applied per video. Because
  YouTube search results are not strictly ordered by date, the script fetches a
  larger candidate pool (`--pool`) and keeps the first `--limit` that fall inside
  the window. If fewer than `--limit` recent videos exist, it returns what it
  found and prints a note suggesting a larger `--pool` or `--months`.
- **Subscriber count** comes from `channel_follower_count`. It is occasionally
  unavailable; in that case it and the ratio show `N/A`.
- **Speed:** full metadata requires extracting each candidate, so larger
  `--pool` / `--limit` values take longer. Defaults are tuned for a balance.
- The script prints progress and notes to stderr and results to stdout, so you
  can redirect results cleanly if needed.
