# cnsplots API reference (Python)

Verified against **cnsplots 0.5.0** (`import cnsplots as cns`). Every signature
below was introspected from the installed package; every example renders. Docs:
<https://cnsplots.farid.one/> · repo: <https://github.com/faridrashidi/cnsplots>.

cnsplots is built on matplotlib and is seaborn-compatible: each plot function
draws on the current (or a supplied) Axes and returns it, so you can post-process
with plain matplotlib (`ax.set_ylabel(...)`, `ax.set_ylim(...)`, etc.).

## Table of contents
- [The three-line workflow](#the-three-line-workflow)
- [figure / savefig / settings](#figure--savefig--settings)
- [Statistical significance (`pairs=`)](#statistical-significance-pairs)
- [Basic plots](#basic-plots)
- [Distribution plots](#distribution-plots)
- [Relationship plots](#relationship-plots)
- [Categorical / part-to-whole](#categorical--part-to-whole)
- [Scientific plots](#scientific-plots)
- [Heatmap (AnnData)](#heatmap-anndata)
- [Multi-panel figures](#multi-panel-figures)
- [Datasets](#datasets)
- [Gotchas](#gotchas)

## The three-line workflow

```python
import cnsplots as cns
df = cns.datasets.load_dataset("tips")
cns.figure(width=100, height=150)          # 1. open a canvas (pixels)
cns.boxplot(data=df, x="day", y="total_bill")  # 2. draw
cns.savefig("figure.svg")                  # 3. export (vector for journals)
```

## figure / savefig / settings

```python
figure(width=None, height=None, color_cycle=None, color_map=None) -> None
```
- `width`, `height` — **axes size in pixels** (not inches). Journal single column
  ≈ 85 mm, double ≈ 174 mm; work in pixels and let `savefig` handle DPI.
- `color_cycle` — qualitative palette name for grouped/hue plots (default
  `Ecotyper1`). See `references/palettes.md`.
- `color_map` — sequential/diverging colormap for heatmaps, ridge, gsea, etc.
  (default `gnuplot`).

```python
savefig(filepath) -> None    # alias: save(filepath)
```
- `.svg` / `.pdf` → vector, editable in Adobe Illustrator — **use these for
  submission**. `.png` → raster preview. Font type is set to keep text editable.
- Optional: install MuPDF's `mutool` for enhanced SVG; without it a standard
  matplotlib SVG is written (a harmless RuntimeWarning notes this).

`cns.settings` holds global defaults (fonts, spine visibility, p-value format,
tick styling, `figure_width`/`figure_height`, `palette_qual`, `palette_seq`).
Set attributes on it before plotting to change house style, e.g.
`cns.settings.palette_qual = "Nature"`.

Named single colors are exposed as constants: `cns.BLUE, RED, GREEN, ORANGE,
PURPLE, PINK, BROWN, GRAY, YELLOW, VIOLET, CHOCOLATE`.

## Statistical significance (`pairs=`)

`boxplot`, `violinplot`, `barplot`, `stripplot`, `stackplot`, and `survivalplot`
accept `pairs` — a list of category tuples to compare. cnsplots picks an
appropriate test (e.g. Mann-Whitney U for two groups), runs it, prints which
test it used, and draws the bracket with a significance marker (`ns`, `*`,
`**`, `***`, `****`). It relies on `statannotations` under the hood.

```python
cns.boxplot(data=tips, x="day", y="total_bill",
            pairs=[("Thur", "Fri"), ("Sat", "Sun")])
```
Only list the comparisons you want annotated — brackets stack automatically.

## Basic plots

```python
boxplot(data, x, y, pairs=None, showoutliers=False, add_count=False, whis=1.5,
        *, hue=None, order=None, hue_order=None, ax=None, **kwargs) -> Axes
violinplot(data, x, y, pairs=None, width=0.6, add_box=True, add_count=False,
           *, hue=None, order=None, hue_order=None, ax=None, **kwargs) -> Axes
barplot(data, x, y, pairs=None, add_tip=False,
        *, hue=None, order=None, hue_order=None, ax=None, **kwargs) -> Axes
stripplot(data, x, y, size=2, showmedian=True, showmeans=False, add_count=False,
          *, hue=None, order=None, hue_order=None, ax=None, **kwargs) -> Axes
lineplot(data, x, y, *, hue=None, ax=None, **kwargs) -> Axes
```
- `add_count=True` annotates group n. `order` / `hue_order` fix category order.
- **Horizontal bars:** put the numeric column in `x` and the categorical in `y`
  (`barplot(data=df, x="total_bill", y="day")`).

## Distribution plots

```python
histplot(data, x, *, hue=None, ax=None, **kwargs) -> Axes
distplot(data, x, *, hue=None, ax=None, **kwargs) -> Axes   # hist + kde
kdeplot(data, x, add_mode=True, *, hue=None, hue_order=None, ax=None, **kwargs) -> Axes
ridgeplot(data, x, y, cmap="viridis", *, ax=None) -> Axes    # y = category rows
qqplot(data, x, *, ax=None, **kwargs) -> Axes
```
`kdeplot(..., hue="species")` overlays one density per group; `ridgeplot(x="value",
y="group")` stacks them as a ridge/joyplot.

## Relationship plots

```python
scatterplot(data, x, y, s=7, *, hue=None, hue_order=None, ax=None, **kwargs) -> Axes
regplot(data, x, y, hue=None, s=3, color="black", *, hue_order=None, ax=None, **kwargs) -> Axes
```
`regplot` draws the scatter, a fitted line with confidence band, and the
correlation/p-value annotation — the standard "is x associated with y" figure.

## Categorical / part-to-whole

```python
pieplot(data, x, legend="bottom", order=None, *, ax=None) -> Axes
donutplot(data, x, legend="bottom", order=None, *, ax=None) -> Axes
stackplot(data, x=None, y=None, *, stack, order=None, stack_order=None,
          width=0.5, normalize=True, pairs=None, add_count=False, n_factor=1, ax=None) -> Axes
slopeplot(data, x, y, hue, pair, *, hue_order=None, ax=None) -> Axes
sankeyplot(data, x, y, label_rotation=0, *, ax=None) -> Axes
lollipopplot(data, x, y, *, ax=None, **kwargs) -> Axes
dotplot(data, ...) -> Axes
```
- `pieplot`/`donutplot` count the categories in column `x` (pass the raw column,
  not pre-aggregated counts).
- `stackplot`: `x` is the axis, `stack` is the category split within each bar;
  `normalize=True` gives proportions (0-1). Accepts `pairs` for comparisons.
- **`slopeplot` data model** (easy to get wrong): `x` is the group axis (e.g.
  `site`), `hue` is the **two** paired conditions (exactly 2 values, e.g.
  `healthy`/`disease`), `pair` is the subject id. Each subject belongs to one `x`
  group and has exactly one `y` value per `hue` level. It draws a line per
  subject connecting its two condition values.

```python
# slopeplot — correct shape
cns.slopeplot(data=df, x="site", y="value", hue="condition", pair="subject_id")
```

## Scientific plots

```python
survivalplot(data, duration, event, hue, hue_order=None, time_label="Time",
             *, overall_test="logrank", pairs=None, ax=None) -> Axes
rocplot(data, true_label_col, pred_prob_cols, *, ax=None) -> Axes
volcanoplot(data, x="log2FoldChange", y="-log10(adjp)", symbol="symbol",
            show_list=None, n_show=10, *, ax=None) -> Axes
gseaplot(data, y, color="NES", cutoff=0.05, cmap="BuRd_custom", top_term=20,
         size=1.8, significance_column="FDR q-val", *, ax=None) -> Axes
forestplot(model, bar_width=None, add_pvalue=True, *, ax=None) -> Axes
confusionplot(...) -> Axes
cumulativeincidenceplot(...) -> Axes
upsetplot(...) ; phyloplot(...) ; prerank(...)
```
- **survivalplot**: Kaplan-Meier curves per `hue` group with an omnibus log-rank
  test; `event` is 1=event/0=censored. Uses `lifelines`.
- **rocplot**: `pred_prob_cols` may be one column or a list (one ROC + AUC per
  model, as in showcase panel M).
- **volcanoplot**: expects columns for effect size, significance, and label. The
  defaults (`log2FoldChange`, `-log10(adjp)`, `symbol`) match the common DE table;
  `show_list` labels specific genes, `n_show` caps auto-labels.
- **forestplot**: pass a fitted model — `cns.CoxModel` or `cns.LogisticModel`.

## Heatmap (AnnData)

`heatmapplot` takes an **AnnData** object (from `anndata`, which ships with
cnsplots), not a DataFrame — rows are `obs`, columns are `var`, and row/column
annotations are pulled from `.obs` / `.var` columns.

```python
heatmapplot(adata, layer=None, row_annotation=None, col_annotation=None,
            row_cluster=False, col_cluster=False, row_split=None, col_split=None,
            cmap=None, label="value", ...) -> ClusterMapPlotterNew
```

```python
import anndata as ad, pandas as pd, numpy as np
adata = ad.AnnData(
    X=matrix,                                   # samples x features
    obs=pd.DataFrame({"group": sample_labels}, index=sample_ids),
    var=pd.DataFrame({"module": feature_labels}, index=feature_ids),
)
cns.figure(width=95, height=75, color_map="BuRd_custom")
cns.heatmapplot(adata, row_annotation=["group"], col_annotation=["module"],
                row_cluster=True, col_cluster=True)
cns.savefig("heatmap.pdf")
```
Built on `PyComplexHeatmap`. `row_split`/`col_split` cut the dendrogram into
blocks. For a quick matrix without annotations, wrap it in a bare
`ad.AnnData(X=matrix)`.

## Multi-panel figures

The intended idiom — do **not** hand-roll `plt.subplot` on a tiny canvas (labels
collide). `multipanel(max_width=...)` returns an object; call `.panel(...)` before
drawing each panel; panels flow left-to-right and wrap at `max_width`.

```python
mp = cns.multipanel(max_width=380, title="Figure 1")
mp.panel("A", width=90, height=90, pad_left=42, pad_top=12)
cns.boxplot(data=tips, x="day", y="total_bill", pairs=[("Thur", "Fri")])
mp.panel("B", width=90, height=90, pad_left=42, pad_top=12)
cns.violinplot(data=iris, x="species", y="sepal_width")
cns.savefig("figure1.pdf")
```
- `.panel(name, width, height, pad_left, pad_top, margin_left, margin_top,
  margin_right, margin_bottom)` — `pad_left` reserves room for the y-axis label +
  the bold panel letter; bump it if the ylabel is long.
- `add_panel_label("A")` adds just the letter to the current axes when you are
  compositing some other way.

## Datasets

```python
cns.datasets.load_dataset(name)   # -> DataFrame
```
Bundled: `tips`, `iris`, `penguins`, `flights`, `fmri`. Use them for quick
prototypes and to sanity-check a plot before wiring in real data.

## Gotchas
- **Pixels, not inches** in `figure()`. A 60x60 axes is a small panel; a standalone
  figure is often 100-180 wide.
- **Fonts**: cnsplots targets Arial/Helvetica. If they are not installed you'll
  see `findfont: Font family 'Helvetica' not found` and it falls back to a system
  sans — output is fine, but install Arial/Helvetica for pixel-exact journal
  matching, or call `cns.apply_unicode_font()` for full Unicode glyph coverage.
- **Categorical `pairs`** must use category labels that exist in the data.
- **`heatmapplot` needs AnnData**, `vennplot` needs `list[set]` — everything else
  is DataFrame-in.
- cnsplots prints small status lines (e.g. the chosen statistical test, legend
  reflow notes). These are informational, not errors.
