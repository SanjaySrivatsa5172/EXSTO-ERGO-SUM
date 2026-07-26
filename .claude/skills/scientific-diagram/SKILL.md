---
name: scientific-diagram
description: >-
  Create publication-ready scientific plots, figures, and diagrams for papers,
  manuscripts, posters, and grants — the kind of clean, journal-quality graphics
  seen in Cell, Nature, and Science. Use this skill WHENEVER the user wants to
  plot or visualize scientific/experimental/statistical data, or asks for a box
  plot, violin plot, bar plot, strip/jitter plot, scatter, regression, survival
  / Kaplan-Meier curve, ROC curve, volcano plot, heatmap, Venn diagram, Sankey
  diagram, ridge/joy plot, KDE/density, forest plot, GSEA plot, pie/donut, slope
  plot, or a multi-panel figure — even if they don't name a library. Also use it
  whenever cnsplots or ggpubr is mentioned, when a figure needs statistical
  significance annotations (p-values, asterisks), when data must be turned into a
  figure for submission, or when the user asks to make a chart "look
  publication-ready." Prefer this over ad-hoc matplotlib/seaborn for anything
  destined for a scientific figure. Python uses cnsplots; R uses ggpubr.
---

# Scientific diagram illustration

Produce clean, journal-quality scientific figures with minimal code, using two
purpose-built libraries:

- **Python → `cnsplots`** (built on matplotlib; Cell/Nature/Science styling,
  statistical annotations, vector export editable in Illustrator). This is the
  default. Docs: <https://cnsplots.farid.one/>.
- **R → `ggpubr`** (built on ggplot2; publication-ready plots + stats). Use when
  the user works in R. Docs: <https://rpkgs.datanovia.com/ggpubr/>.

Both cover the same ~18 core plot types (box, violin, strip, stack, bar, pie,
Venn, donut, regression, survival, KDE, volcano, ROC, Sankey, ridge, slope,
scatter, heatmap). Choose the plot from the *question*, not habit — see
`references/plot-gallery.md`.

## When you're asked for a scientific figure, do this

1. **Understand the data and the question.** What are the variables, which are
   categorical vs numeric, how many groups, and what is the figure meant to show
   (a difference? an association? a composition? survival?). If real data exists,
   glance at the columns; if not, you can prototype on a bundled dataset.
2. **Pick the plot type** using `references/plot-gallery.md` (the A–R selection
   table). Choosing *well* matters as much as choosing correctly — e.g. show
   points for small n, avoid pie charts for many slices.
3. **Pick the language.** Default to Python/cnsplots. Switch to R/ggpubr only if
   the user's workflow is R (see `references/ggpubr-api.md`).
4. **Set up the environment** (Python), then generate the figure.
5. **Render and actually look at it.** Save a PNG and open it (Read the image) to
   confirm it says what the user wants before delivering. A script that exits 0
   is not proof the figure is right — a diff is not evidence.
6. **Export for delivery.** `.svg` or `.pdf` for submission (vector, editable);
   `.png` for previews.

## Python setup (cnsplots)

cnsplots requires Python ≥ 3.10 and pulls in matplotlib, seaborn, pandas,
scanpy, lifelines, and gseapy, so install it into a venv once:

```bash
bash .claude/skills/scientific-diagram/scripts/setup_env.sh
# → prints the venv python path; use it to run the scripts below.
```

Sanity-check the install:
```bash
.venv-cnsplots/bin/python .claude/skills/scientific-diagram/scripts/make_figure.py \
    --self-test --out /tmp/selftest.png
```

## Two ways to build a figure

### Fast path — `make_figure.py` (single-panel from a CSV)
A dependable CLI that wraps the common plot types. Good for a quick, correct
figure without writing boilerplate.

```bash
# Runnable verbatim against the bundled example dataset:
.venv-cnsplots/bin/python .claude/skills/scientific-diagram/scripts/make_figure.py \
    --data .claude/skills/scientific-diagram/assets/example_expression.csv \
    --kind boxplot --x group --y expression \
    --pairs "Control,DrugA;Control,DrugB" --palette Nature \
    --width 55 --height 60 --ylabel "Expression (TPM)" --out figure.svg
```
Run it with `--help` for every flag. `--kind` accepts: boxplot, violinplot,
barplot, stripplot, scatterplot, regplot, lineplot, ridgeplot, kdeplot, histplot,
distplot, pieplot, donutplot, stackplot, slopeplot, sankeyplot, survivalplot,
volcanoplot. Significance goes in `--pairs "A,B;C,D"`.

### Direct path — write cnsplots code (multi-panel, custom, or specialized)
For multi-panel composites, ROC with several models, annotated heatmaps, or
anything bespoke, write the calls directly. The pattern is always three lines —
open a canvas, draw, save:

```python
import cnsplots as cns
df = cns.datasets.load_dataset("tips")          # or pd.read_csv(...)
cns.figure(width=55, height=60, color_cycle="Nature")
cns.boxplot(data=df, x="day", y="total_bill",
            pairs=[("Thur", "Fri"), ("Sat", "Sun")])   # auto stats + brackets
cns.savefig("figure.svg")
```

Full signatures, every plot type, palettes, and gotchas are in
`references/cnsplots-api.md`. Copy-paste-ready templates for **all 18 showcase
plots plus a multi-panel composite** are in `scripts/gallery_demo.py` — run it to
regenerate the whole gallery, or lift one function as a starting point:

```bash
.venv-cnsplots/bin/python .claude/skills/scientific-diagram/scripts/gallery_demo.py \
    --out ./gallery_out
```

## Key techniques

- **Statistical significance.** Pass `pairs=[("A","B"), ...]` to box/violin/bar/
  strip plots. cnsplots runs an appropriate test, prints which one, and draws the
  bracket with `ns`/`*`/`**`/… Only annotate the comparisons you're testing, and
  name the test in the caption. (ggpubr: `stat_compare_means`.)
- **Multi-panel figures.** Use the `multipanel` idiom — do not hand-roll
  `plt.subplot` on a small canvas (labels collide):
  ```python
  mp = cns.multipanel(max_width=380, title="Figure 1")
  mp.panel("A", width=90, height=90, pad_left=42, pad_top=12)
  cns.boxplot(data=df, x="day", y="total_bill")
  mp.panel("B", width=90, height=90, pad_left=42, pad_top=12)
  cns.violinplot(data=iris, x="species", y="sepal_width")
  cns.savefig("figure1.pdf")
  ```
  (ggpubr: `ggarrange(p1, p2, labels=c("A","B"), ncol=2)`.)
- **Color with meaning.** Qualitative palette for categories, sequential for
  ordered magnitude, diverging for a midpoint (log2FC, z-score). Keep it
  consistent across panels and colorblind-safe. See `references/palettes.md`.
- **Sizing.** `figure(width, height)` is in **pixels**, not inches. Panels are
  ~50–90 px; standalone figures ~100–180 px wide.
- **Fonts.** cnsplots targets Arial/Helvetica; if absent it falls back to a
  system sans (a harmless `findfont` warning). Install Arial/Helvetica for
  pixel-exact journal matching.

## R path (ggpubr)

When the user is in R, don't install cnsplots — write ggpubr. Full API,
statistical annotation, journal palettes (`"npg"`, `"jco"`, …), and `ggarrange`
are in `references/ggpubr-api.md`. Canonical example:

```r
library(ggpubr)
ggviolin(df, x = "dose", y = "len", fill = "dose", palette = "npg",
         add = "boxplot", add.params = list(fill = "white")) +
  stat_compare_means(comparisons = list(c("0.5","1"), c("1","2")),
                     label = "p.signif")
```

## Delivering the figure
- Save the working/preview copy as `.png` and **open it to verify** it reads
  correctly (right groups, labels, significance, colors).
- Provide the submission copy as `.svg` or `.pdf` (vector — scales cleanly and is
  editable in Illustrator/Inkscape).
- In the caption, state n per group and the statistical test used.

## Reference files
- `references/plot-gallery.md` — which plot for which question (A–R table) + how to
  choose well. **Start here** when the plot type isn't already decided.
- `references/cnsplots-api.md` — full verified Python API (every function,
  signature, example, and gotcha).
- `references/ggpubr-api.md` — full R API (functions, stats, palettes, arrange).
- `references/palettes.md` — cnsplots + ggpubr palette catalog and accessibility.

## Scripts
- `scripts/setup_env.sh` — create a venv and install cnsplots.
- `scripts/make_figure.py` — CLI: CSV → single-panel publication figure.
- `scripts/gallery_demo.py` — verified templates for all 18 plots + a composite.
