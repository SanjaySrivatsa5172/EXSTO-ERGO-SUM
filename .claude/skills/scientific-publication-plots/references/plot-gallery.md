# Plot gallery & selection guide

Map the user's data and question to the right plot. Panel letters (A–R) match the
cnsplots showcase figure. Each row gives the cnsplots function and the ggpubr
equivalent; see the API references for signatures.

## Pick by question

| You want to show… | Use | Panel | cnsplots | ggpubr |
|---|---|---|---|---|
| Distribution of a numeric value across a few groups | box plot | A | `boxplot` | `ggboxplot` |
| Distribution **shape** across groups (bi-modality) | violin (+box) | B | `violinplot` | `ggviolin` |
| Every data point across groups (small n) | strip / jitter | C | `stripplot` | `ggstripchart` |
| Composition (proportions) across groups | stacked bar | D | `stackplot` | `ggbarplot(position=...)` |
| A single summary value per category | bar plot | E | `barplot` | `ggbarplot` |
| Parts of one whole | pie | F | `pieplot` | `ggpie` |
| Overlap between 2–3 sets | Venn | G | `vennplot` | *(ggVennDiagram)* |
| Parts of a whole, modern look | donut | H | `donutplot` | `ggdonutchart` |
| Association between two numeric variables | regression | I | `regplot` | `ggscatter`+`stat_cor` |
| Time-to-event by group | Kaplan-Meier | J | `survivalplot` | *(survminer)* |
| Smooth distribution by group | KDE | K | `kdeplot` | `ggdensity` |
| Differential expression (effect vs significance) | volcano | L | `volcanoplot` | *(EnhancedVolcano)* |
| Classifier performance / model comparison | ROC + AUC | M | `rocplot` | `ggroc`/pROC |
| Flow between categorical stages | Sankey | N | `sankeyplot` | *(ggalluvial)* |
| Many distributions stacked (compact) | ridge | O | `ridgeplot` | *(ggridges)* |
| Paired change between two conditions | slope | P | `slopeplot` | `ggpaired` |
| Two numeric variables, points by group | scatter | Q | `scatterplot` | `ggscatter` |
| Matrix of values with clustering | heatmap | R | `heatmapplot` | *(ComplexHeatmap)* |

Not in the showcase but available in cnsplots: `lineplot`, `histplot`,
`distplot`, `qqplot`, `dotplot`, `lollipopplot`, `forestplot` (Cox/logistic),
`gseaplot`, `confusionplot`, `cumulativeincidenceplot`, `upsetplot`, `phyloplot`.

## Choosing well (not just correctly)
- **Few points → show them.** With n ≲ 15 per group prefer strip/jitter (C) or a
  box/violin with points overlaid; a bare bar plot hides the distribution.
- **Box vs violin.** Box for medians/spread/outliers; violin when the *shape*
  matters (skew, bimodality). Violin needs enough points to estimate a density.
- **Avoid pie/donut for >4 slices or for comparisons** — bars are read more
  accurately. Reserve F/H for a small, familiar part-to-whole.
- **Composition across groups → stackplot (D)** with `normalize=True`, not
  side-by-side pies.
- **Correlation → regplot (I)**, which adds the fit, band, and r/p; plain scatter
  (Q) is for showing group structure in 2-D.
- **Significance:** add `pairs=` only for the comparisons you're actually testing;
  don't bracket every pair. State the test in the caption (cnsplots prints it).
- **Color = meaning.** Use a qualitative palette for categories, sequential for
  ordered magnitude, diverging for a meaningful midpoint (log2FC, z-score). See
  `references/palettes.md`.
- **Colorblind safety & grayscale.** Prefer palettes that survive both; don't
  encode a distinction by hue alone if it's load-bearing.

## Data-shape cheatsheet (cnsplots)
- Long/tidy DataFrame for almost everything: one row per observation, columns for
  `x`, `y`, and any `hue`.
- `pieplot`/`donutplot`: pass the **raw category column** as `x` (it counts).
- `stackplot`: `x` = axis, `stack` = the split category.
- `slopeplot`: `x` = group, `hue` = the two paired conditions, `pair` = subject.
- `survivalplot`: `duration` (time), `event` (1/0), `hue` (arm).
- `rocplot`: `true_label_col` + one or more `pred_prob_cols`.
- `volcanoplot`: effect column (`log2FoldChange`), significance (`-log10(adjp)`),
  and a `symbol` label column.
- `vennplot`: `lists=[set, set, ...]`, `labels=[...]`.
- `heatmapplot`: an **AnnData** (rows=`obs`, cols=`var`, annotations from each).
