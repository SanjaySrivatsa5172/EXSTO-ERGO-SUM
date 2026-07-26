---
name: scientific-publication-plots
description: Create publication-ready scientific figures and multipanel diagrams for high-impact journals using cnsplots in Python or ggpubr in R. Activate whenever the user requests journal-quality plots, scientific diagram illustration, Cell/Nature/Science-style figures, or code for box, violin, bar, strip, scatter, regression, volcano, ROC, survival/Kaplan-Meier, heatmap, ridge, slope, Sankey, Venn, KDE, forest, GSEA, pie or donut plots — with statistical significance annotations, multipanel layouts with A/B/C panel labels, or professional visualizations for papers, manuscripts, posters and grants. Use it even when the user doesn't name a library, and prefer it over base matplotlib/seaborn or plain ggplot2 for anything destined for a scientific figure.
---

# Scientific Publication Plots

Generate clean, publication-ready scientific diagrams and multi-panel figures that
meet the visual standards of Cell, Nature, Science and similar journals. Prefer
these purpose-built packages over base matplotlib/seaborn or plain ggplot2.

- **cnsplots** (Python) — the default. Precise pixel sizing, multipanel figures
  with automatic A/B/C labels, SVG optimized for Adobe Illustrator, and
  specialized plots (volcano, survival, ROC, Sankey, ridge, slope, clustered
  heatmap, GSEA). Docs: <https://cnsplots.farid.one/>.
- **ggpubr** (R) — for R/ggplot2 workflows needing rapid common plots with
  built-in pairwise stats and significance annotations. Docs:
  <https://rpkgs.datanovia.com/ggpubr/>.
- Fall back to base libraries only for highly custom, unsupported needs.

Choose the plot from the *question*, not habit — `references/plot-gallery.md` maps
data + question to the right plot (the A–R selection table).

> Paths below are relative to this skill's directory (shown as the base directory
> when the skill is invoked). Run scripts from there, or prefix with that path.

## Workflow

1. **Understand the data and question** — variables, categorical vs numeric, how
   many groups, and what the figure must show (a difference? an association? a
   composition? survival?).
2. **Pick the plot** via `references/plot-gallery.md`. Choosing *well* matters as
   much as choosing correctly — show points for small n, avoid pie charts for many
   slices, use a difference plot for comparisons and a composition plot for parts.
3. **Pick the language** — Python/cnsplots by default; R/ggpubr if the user's
   workflow is R.
4. **Produce complete, runnable code** — imports, (sample) data if helpful, the
   plot, stats, and vector export.
5. **Render and actually look at it** — save a PNG and open it to confirm it says
   what the user wants (right groups, labels, significance, colors). A script that
   exits 0 is not proof the figure is right.
6. **Export for delivery** — SVG or PDF for submission (vector, editable); PNG for
   previews.

## Environment (Python)

cnsplots needs Python ≥ 3.10 and pulls in matplotlib, seaborn, pandas, scanpy,
lifelines and gseapy. Install once into a venv:

```bash
bash scripts/setup_env.sh          # prints the venv python path to use
```
(or `pip install cnsplots` into an existing environment). R users instead:
`install.packages("ggpubr")`.

## Two ways to build a figure

### Fast path — the bundled CLI (single panel from a CSV)
A dependable wrapper for the common plot types — a quick, correct figure with no
boilerplate:
```bash
.venv-cnsplots/bin/python scripts/make_figure.py \
    --data assets/example_expression.csv --kind violinplot \
    --x group --y expression --pairs "Control,DrugA;Control,DrugB" \
    --palette Nature --ylabel "Expression (TPM)" --out figure.svg
```
`--kind` covers box/violin/bar/strip/scatter/regplot/line/ridge/kde/hist/dist/
pie/donut/stack/slope/sankey/survival/volcano; run `--help` for every flag.

### Direct path — write cnsplots (multipanel, custom, or specialized)
The pattern is three lines — open a canvas (pixels), draw, save:
```python
import cnsplots as cns
df = cns.datasets.load_dataset("tips")               # or pd.read_csv(...)
cns.figure(width=150, height=150, color_cycle="Nature")   # dimensions in PIXELS
cns.boxplot(data=df, x="day", y="total_bill",
            pairs=[("Thur", "Fri"), ("Sat", "Sun")])       # auto stats + brackets
cns.savefig("figure.svg")                             # SVG/PDF preferred
```

Multipanel — use the `multipanel` idiom (do **not** hand-roll `plt.subplot` on a
small canvas; labels collide):
```python
mp = cns.multipanel(max_width=540, title="Figure 1")
mp.panel("A", width=180, height=150, pad_left=48, pad_top=14)
cns.boxplot(data=df, x="day", y="total_bill")
mp.panel("B", width=180, height=150, pad_left=48, pad_top=14)
cns.volcanoplot(data=deg)
cns.savefig("figure1.pdf")
```

Copy-paste templates for **all 18 showcase plots plus a composite** live in
`scripts/gallery_demo.py`. Full verified signatures, palettes and gotchas are in
`references/cnsplots-api.md`.

### Key plot types (cnsplots)
- **Comparison:** boxplot, violinplot, stripplot, barplot, stackplot
- **Distribution:** histplot, kdeplot, ridgeplot
- **Scatter / trend:** scatterplot, regplot, lineplot, slopeplot
- **Proportion:** pieplot, donutplot, vennplot, sankeyplot
- **Scientific:** survivalplot, rocplot, volcanoplot, heatmapplot, forestplot, gseaplot

Pass `pairs=[("A","B"), ...]` (or `pairs="all"`) to comparison plots for automatic
statistical tests + significance brackets; cnsplots prints which test it used.
Most functions accept `ax=` and return the Axes for further matplotlib tweaks.

## ggpubr essentials (R)
```r
library(ggpubr)
ggboxplot(df, x = "day", y = "total_bill", color = "sex", palette = "jco",
          add = "jitter") +
  theme_pubr() +
  stat_compare_means(comparisons = list(c("Thur","Fri"), c("Sat","Sun")),
                     label = "p.signif")
```
Functions: ggboxplot, ggviolin, ggbarplot, ggscatter, ggdensity, gghistogram,
ggdotchart, ggline, ggpie, ggdonutchart. Stats: stat_compare_means, geom_pwc,
compare_means, stat_pvalue_manual. Arrange: `ggarrange(..., labels=c("A","B"))`,
annotate_figure. Palettes: "jco"/"npg"/"lancet". Details in
`references/ggpubr-api.md`.

## Best practices
- Export vector formats (SVG/PDF) for editability and journal submission.
- Use package journal palettes (`color_cycle="Cell"/"Nature"/"Science"` or
  `palette="jco"`); keep them consistent across panels and colorblind-safe
  (`references/palettes.md`).
- Label panels A, B, C… clearly. cnsplots `figure()` sizes are **pixels**
  (single column ≈ 85–90 mm, double ≈ 170–180 mm — size accordingly).
- Always disclose n, the statistical method, and what error bars/CI represent in
  the caption.
- Maximize data-ink; keep designs clean. Survival: add risk tables when space
  permits. Volcano: label key points and set clear thresholds.

## Reference files
- `references/plot-gallery.md` — which plot for which question (A–R) + how to
  choose well. **Start here** when the plot type isn't already decided.
- `references/cnsplots-api.md` — full verified Python API (every function,
  signature, example, and gotcha).
- `references/ggpubr-api.md` — full R API (functions, stats, palettes, arrange).
- `references/palettes.md` — cnsplots + ggpubr palette catalog and accessibility.

## Scripts
- `scripts/setup_env.sh` — create a venv and install cnsplots.
- `scripts/make_figure.py` — CLI: CSV → single-panel publication figure.
- `scripts/gallery_demo.py` — verified templates for all 18 plots + a composite.
