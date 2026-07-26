#!/usr/bin/env python3
"""Generate a publication-ready scientific plot from a CSV with cnsplots.

This is a thin, dependable wrapper around the cnsplots API so a single command
produces a journal-quality figure without rewriting boilerplate each time. It
covers the common single-panel plot types; for multi-panel composites, ROC with
several models, heatmaps with rich annotations, or anything bespoke, write the
cnsplots calls directly (see references/cnsplots-api.md) — this CLI is the fast
path, not a cage.

Run with the interpreter from setup_env.sh, e.g.:

    .venv-cnsplots/bin/python make_figure.py \
        --data tips.csv --kind boxplot --x day --y total_bill \
        --pairs "Thur,Fri;Sat,Sun" --palette Nature \
        --width 55 --height 60 --out figure.svg

Save as .svg or .pdf for journals (vector, editable in Illustrator); .png for
quick previews. Use --self-test to render a known-good boxplot with no input.
"""
from __future__ import annotations

import argparse
import sys


# Plot kinds that take (data, x, y) and accept significance `pairs`.
_XY_COMPARISON = {"boxplot", "violinplot", "barplot", "stripplot"}
# Plot kinds that take (data, x, y) but no `pairs`.
_XY_PLAIN = {"scatterplot", "regplot", "lineplot", "ridgeplot"}
# Plot kinds that take a single distribution column `x`.
_X_ONLY = {"kdeplot", "histplot", "distplot", "pieplot", "donutplot"}

ALL_KINDS = sorted(
    _XY_COMPARISON
    | _XY_PLAIN
    | _X_ONLY
    | {"stackplot", "slopeplot", "sankeyplot", "survivalplot", "volcanoplot"}
)


def parse_pairs(spec: str | None):
    """"Thur,Fri;Sat,Sun" -> [("Thur","Fri"), ("Sat","Sun")]."""
    if not spec:
        return None
    pairs = []
    for chunk in spec.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        a, _, b = chunk.partition(",")
        pairs.append((a.strip(), b.strip()))
    return pairs or None


def parse_order(spec: str | None):
    if not spec:
        return None
    return [s.strip() for s in spec.split(",") if s.strip()]


def build(args, cns, pd):
    """Dispatch to the right cnsplots function. Returns nothing; draws on current figure."""
    if args.self_test:
        df = cns.datasets.load_dataset("tips")
        cns.boxplot(data=df, x="day", y="total_bill",
                    pairs=[("Thur", "Fri"), ("Sat", "Sun")])
        return

    df = pd.read_csv(args.data)
    kind = args.kind
    order = parse_order(args.order)
    pairs = parse_pairs(args.pairs)
    common = {}
    if args.hue:
        common["hue"] = args.hue

    if kind in _XY_COMPARISON:
        _require(args, "x", "y")
        kw = dict(data=df, x=args.x, y=args.y, **common)
        if order:
            kw["order"] = order
        if pairs:
            kw["pairs"] = pairs
        getattr(cns, kind)(**kw)

    elif kind in _XY_PLAIN:
        _require(args, "x", "y")
        getattr(cns, kind)(data=df, x=args.x, y=args.y, **common)

    elif kind in _X_ONLY:
        _require(args, "x")
        if kind in {"pieplot", "donutplot"}:
            getattr(cns, kind)(data=df, x=args.x)  # counts categories in x
        else:
            getattr(cns, kind)(data=df, x=args.x, **common)

    elif kind == "stackplot":
        _require(args, "x", "stack")
        cns.stackplot(data=df, x=args.x, stack=args.stack)

    elif kind == "slopeplot":
        _require(args, "x", "y", "hue", "pair")
        cns.slopeplot(data=df, x=args.x, y=args.y, hue=args.hue, pair=args.pair)

    elif kind == "sankeyplot":
        _require(args, "x", "y")
        cns.sankeyplot(data=df, x=args.x, y=args.y)

    elif kind == "survivalplot":
        _require(args, "duration", "event", "hue")
        cns.survivalplot(data=df, duration=args.duration, event=args.event, hue=args.hue)

    elif kind == "volcanoplot":
        # cnsplots defaults: x=log2FoldChange, y=-log10(adjp), symbol=symbol.
        kw = dict(data=df)
        if args.x:
            kw["x"] = args.x
        if args.y:
            kw["y"] = args.y
        if args.symbol:
            kw["symbol"] = args.symbol
        cns.volcanoplot(**kw)

    else:  # pragma: no cover - argparse choices guard this
        raise SystemExit(f"Unsupported --kind {kind!r}")


def _require(args, *fields):
    missing = [f"--{f}" for f in fields if not getattr(args, f, None)]
    if missing:
        raise SystemExit(
            f"--kind {args.kind} requires {', '.join(missing)}. "
            "See references/cnsplots-api.md for each plot's required columns."
        )


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data", help="Path to input CSV.")
    p.add_argument("--kind", choices=ALL_KINDS, help="Plot type.")
    p.add_argument("--x")
    p.add_argument("--y")
    p.add_argument("--hue", help="Grouping column for color.")
    p.add_argument("--pairs", help='Significance comparisons, e.g. "A,B;C,D".')
    p.add_argument("--order", help="Category order, comma-separated.")
    p.add_argument("--stack", help="stackplot: column to stack within each x.")
    p.add_argument("--pair", help="slopeplot: subject/observation id column.")
    p.add_argument("--duration", help="survivalplot: time-to-event column.")
    p.add_argument("--event", help="survivalplot: 1=event, 0=censored column.")
    p.add_argument("--symbol", help="volcanoplot: gene/feature label column.")
    p.add_argument("--palette", default="Nature",
                   help="Qualitative color cycle (Cell, Nature, Science, Bold, "
                        "Tableau, Set1-3, Ecotyper1-6). Default: Nature.")
    p.add_argument("--cmap", help="Sequential/diverging colormap for applicable "
                                  "plots (e.g. BuRd_custom, BlueRed, viridis).")
    p.add_argument("--width", type=float, default=60.0, help="Axes width in px.")
    p.add_argument("--height", type=float, default=60.0, help="Axes height in px.")
    p.add_argument("--title")
    p.add_argument("--xlabel")
    p.add_argument("--ylabel")
    p.add_argument("--out", required=True, help="Output path (.svg/.pdf/.png).")
    p.add_argument("--self-test", action="store_true",
                   help="Render a known-good boxplot from the bundled tips data.")
    args = p.parse_args(argv)

    if not args.self_test and (not args.data or not args.kind):
        p.error("--data and --kind are required unless --self-test is given.")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import pandas as pd
        import cnsplots as cns
    except ImportError as e:
        raise SystemExit(
            f"Missing dependency ({e}). Run scripts/setup_env.sh and use its "
            "python interpreter."
        )

    fig_kw = {"width": args.width, "height": args.height}
    if args.palette:
        fig_kw["color_cycle"] = args.palette
    if args.cmap:
        fig_kw["color_map"] = args.cmap
    cns.figure(**fig_kw)

    build(args, cns, pd)

    ax = plt.gca()
    if args.title:
        ax.set_title(args.title)
    if args.xlabel:
        ax.set_xlabel(args.xlabel)
    if args.ylabel:
        ax.set_ylabel(args.ylabel)

    cns.savefig(args.out)
    print(f"Wrote {args.out}")
    if args.out.lower().endswith(".png"):
        print("Tip: export .svg or .pdf for journal submission (vector, editable).")


if __name__ == "__main__":
    sys.exit(main())
