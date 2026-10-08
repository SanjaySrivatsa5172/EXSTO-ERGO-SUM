#!/usr/bin/env python3
"""Search YouTube via yt-dlp and print structured, human-readable results.

Returns the top N videos for a query (default 20), filtered to recent uploads
(default last 6 months), with per-video metadata and a views-to-subscribers
engagement ratio.

Metadata per video: title, channel name, subscriber count, view count,
duration, upload date, URL, and views/subscribers ratio.

Examples:
    search_youtube.py "claude code tutorial"
    search_youtube.py "rust async" --limit 10 --months 12
    search_youtube.py "nba highlights" --months 1 --pool 90
"""

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def ensure_yt_dlp() -> str:
    """Return the path to yt-dlp, or exit with install guidance."""
    path = shutil.which("yt-dlp")
    if path:
        return path
    eprint("error: yt-dlp is not installed or not on PATH.")
    eprint("Install it with one of:")
    eprint("    pip install -U yt-dlp")
    eprint("    pipx install yt-dlp")
    eprint("    brew install yt-dlp        # macOS")
    sys.exit(2)


def months_ago(months: int) -> dt.date:
    """Return the date `months` calendar months before today."""
    today = dt.date.today()
    month_index = today.year * 12 + (today.month - 1) - months
    year, month = divmod(month_index, 12)
    month += 1
    # Clamp day to the last valid day of the target month.
    day = today.day
    while True:
        try:
            return dt.date(year, month, day)
        except ValueError:
            day -= 1


def human_number(n) -> str:
    """Format an integer as a compact human-readable string (1.2K, 3.4M)."""
    if n is None:
        return "N/A"
    try:
        n = int(n)
    except (TypeError, ValueError):
        return "N/A"
    if n < 1000:
        return str(n)
    for unit, threshold in (("B", 1_000_000_000), ("M", 1_000_000), ("K", 1_000)):
        if n >= threshold:
            value = n / threshold
            # Drop the decimal for clean round-ish values (e.g. 12M not 12.0M).
            if value >= 100 or value == int(value):
                return f"{int(round(value))}{unit}"
            return f"{value:.1f}{unit}"
    return str(n)


def human_duration(seconds) -> str:
    """Format a duration in seconds as H:MM:SS or M:SS."""
    if seconds is None:
        return "N/A"
    try:
        seconds = int(seconds)
    except (TypeError, ValueError):
        return "N/A"
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_date(yyyymmdd) -> tuple:
    """Return (display_string, date_or_None) for a YYYYMMDD upload_date."""
    if not yyyymmdd:
        return "Unknown", None
    s = str(yyyymmdd)
    try:
        d = dt.datetime.strptime(s, "%Y%m%d").date()
    except ValueError:
        return s, None
    return d.isoformat(), d


def engagement_ratio(views, subs):
    """views / subscribers, or None if not computable."""
    try:
        views = int(views)
        subs = int(subs)
    except (TypeError, ValueError):
        return None
    if subs <= 0:
        return None
    return views / subs


def run_search(yt_dlp: str, query: str, pool: int, cutoff: dt.date):
    """Run yt-dlp and yield parsed video dicts (one per result)."""
    cmd = [
        yt_dlp,
        f"ytsearch{pool}:{query}",
        "--dump-json",
        "--skip-download",
        "--no-warnings",
        "--ignore-errors",
        # Let yt-dlp skip clearly-old uploads during extraction; we also
        # re-filter below since some videos lack a reliable upload_date.
        "--dateafter",
        cutoff.strftime("%Y%m%d"),
    ]
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue
    proc.wait()
    if proc.returncode not in (0, 101):  # 101 = yt-dlp "download stopped" / partial
        err = proc.stderr.read().strip()
        if err:
            eprint(err)


def build_results(videos, cutoff, limit, no_date_filter):
    results = []
    for v in videos:
        date_str, date_obj = format_date(v.get("upload_date"))
        if not no_date_filter and date_obj is not None and date_obj < cutoff:
            continue
        views = v.get("view_count")
        subs = v.get("channel_follower_count")
        results.append(
            {
                "title": v.get("title") or "Untitled",
                "channel": v.get("channel") or v.get("uploader") or "Unknown channel",
                "subscribers": subs,
                "views": views,
                "duration": v.get("duration"),
                "upload_date": date_str,
                "url": v.get("webpage_url")
                or (f"https://www.youtube.com/watch?v={v['id']}" if v.get("id") else "N/A"),
                "ratio": engagement_ratio(views, subs),
            }
        )
        if len(results) >= limit:
            break
    return results


def print_results(results, query, months, no_date_filter):
    divider = "─" * 72
    window = "all time" if no_date_filter else f"last {months} month(s)"
    print(divider)
    print(f"YouTube search: \"{query}\"  ·  window: {window}  ·  {len(results)} result(s)")
    print(divider)
    if not results:
        print("No videos found matching the criteria.")
        print(divider)
        return
    for i, r in enumerate(results, 1):
        ratio = r["ratio"]
        ratio_str = f"{ratio:.2f}x" if ratio is not None else "N/A"
        print(f"[{i:>2}] {r['title']}")
        print(f"     Channel      : {r['channel']}  ({human_number(r['subscribers'])} subs)")
        print(f"     Views        : {human_number(r['views'])}")
        print(f"     Duration     : {human_duration(r['duration'])}")
        print(f"     Uploaded     : {r['upload_date']}")
        print(f"     Views/Subs   : {ratio_str}  (engagement metric)")
        print(f"     URL          : {r['url']}")
        print(divider)


def main():
    parser = argparse.ArgumentParser(
        description="Search YouTube and return structured video results via yt-dlp."
    )
    parser.add_argument("query", help="Search query.")
    parser.add_argument(
        "--limit", type=int, default=20, help="Number of results to return (default: 20)."
    )
    parser.add_argument(
        "--months",
        type=int,
        default=6,
        help="Only include uploads from the last N months (default: 6). Use 0 for no filter.",
    )
    parser.add_argument(
        "--pool",
        type=int,
        default=None,
        help="How many candidates to fetch before date-filtering "
        "(default: limit*3, min 30). Increase if too few recent results come back.",
    )
    args = parser.parse_args()

    if args.limit < 1:
        eprint("error: --limit must be >= 1")
        sys.exit(2)

    no_date_filter = args.months <= 0
    cutoff = months_ago(args.months) if not no_date_filter else dt.date.min
    pool = args.pool if args.pool else max(args.limit * 3, 30)

    yt_dlp = ensure_yt_dlp()
    eprint(f"Searching YouTube for {args.query!r} (fetching up to {pool} candidates)...")

    videos = run_search(yt_dlp, args.query, pool, cutoff if not no_date_filter else dt.date(1970, 1, 1))
    results = build_results(videos, cutoff, args.limit, no_date_filter)
    print_results(results, args.query, args.months, no_date_filter)

    if not no_date_filter and len(results) < args.limit:
        eprint(
            f"note: only {len(results)} result(s) within the last {args.months} month(s). "
            f"Try a larger --pool or --months to widen the search."
        )


if __name__ == "__main__":
    main()
