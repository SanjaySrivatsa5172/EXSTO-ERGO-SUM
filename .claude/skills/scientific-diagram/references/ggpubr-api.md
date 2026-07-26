# ggpubr API reference (R)

The R counterpart to cnsplots. **ggpubr** wraps ggplot2 to produce
publication-ready plots with minimal code and built-in statistical annotation.
Use it when the user works in R. Docs: <https://rpkgs.datanovia.com/ggpubr/> ·
CRAN: `install.packages("ggpubr")` · repo: <https://github.com/kassambara/ggpubr>.

ggpubr functions return ggplot objects, so you can keep adding ggplot2 layers,
scales, and themes with `+`.

## Table of contents
- [Setup](#setup)
- [Core plotting functions](#core-plotting-functions)
- [Shared arguments](#shared-arguments)
- [Statistical annotations](#statistical-annotations)
- [Palettes](#palettes)
- [Arranging panels](#arranging-panels)
- [Export](#export)
- [Worked examples](#worked-examples)

## Setup
```r
install.packages("ggpubr")   # from CRAN
library(ggpubr)
```

## Core plotting functions
| Function | Plot | cnsplots analogue |
|---|---|---|
| `ggboxplot()` | box plot (optional jitter) | `boxplot` |
| `ggviolin()` | violin, often + inner boxplot | `violinplot` |
| `ggstripchart()` | strip / jitter chart | `stripplot` |
| `ggbarplot()` | bar chart (sortable) | `barplot` |
| `ggline()` | line / mean±error over groups | `lineplot` |
| `ggdotplot()` | dot plot | `dotplot` |
| `ggdotchart()` | Cleveland dot / lollipop | `lollipopplot` |
| `ggerrorplot()` | mean ± error | — |
| `ggpaired()` | before/after paired points+lines | `slopeplot` |
| `gghistogram()` | histogram | `histplot` |
| `ggdensity()` | density | `kdeplot` |
| `ggscatter()` | scatter + fit + `cor` | `scatterplot`/`regplot` |
| `ggpie()` | pie chart | `pieplot` |
| `ggdonutchart()` | donut chart | `donutplot` |
| `ggqqplot()` | Q-Q plot | `qqplot` |
| `ggmaplot()` | MA plot (DE) | ~`volcanoplot` |
| `ggecdf()` | empirical CDF | — |
| `ggballoonplot()` | balloon plot of a table | — |
| `ggsummarystats()` | plot + summary-stat table | — |

For volcano plots and heatmaps R users typically reach outside ggpubr
(`EnhancedVolcano`, `ComplexHeatmap`/`pheatmap`); note that if the user needs those.

## Shared arguments
Most `gg*` functions share these, which is what makes ggpubr terse:
- `data`, `x`, `y` — data frame and column names (strings).
- `color`, `fill` — outline / fill mapped to a grouping column name.
- `palette` — named journal palette (see below) or a vector of hex colors.
- `add` — overlay(s): `"mean"`, `"mean_sd"`, `"mean_se"`, `"median_iqr"`,
  `"jitter"`, `"boxplot"`, `"dotplot"`, `"violin"`. Combine as a vector.
- `add.params` — list controlling the overlay, e.g. `list(fill = "white")`.
- `order` — explicit category order (character vector).
- `facet.by`, `ncol`, `nrow` — small multiples.
- `label`, `label.select` — point/bar labels.
- `ggtheme` — base theme (default `theme_pubr()`).

`ggpar(p, ...)` adjusts titles, axis text, legend, limits, and log scales on an
existing plot; `theme_pubr()` and `labs_pubr()` apply the clean publication look.

## Statistical annotations
- `stat_compare_means()` — add group-comparison p-values to a plot.
  - `method` = `"wilcox.test"` / `"t.test"` (two groups) or `"kruskal.test"` /
    `"anova"` (global).
  - `comparisons = list(c("A","B"), c("B","C"))` draws pairwise brackets.
  - `label = "p.signif"` shows stars (`ns`,`*`,`**`,…); `"p.format"` shows values.
  - `label.y` positions the annotation; `ref.group = ".all."` compares each group
    to the grand mean or to a reference level.
- `compare_means(formula, data, method=...)` — the underlying test, returns a
  tidy data frame of p-values (useful to compute then place manually).
- `stat_pvalue_manual(stat.test, ...)` — draw p-values from a data frame you
  computed yourself (e.g. via **rstatix** `wilcox_test() %>% add_xy_position()`).
- `geom_pwc()` — pairwise comparisons with automatic bracket packing.
- `stat_cor()`, `stat_regline_equation()` — correlation coefficient / regression
  equation on scatter plots.

## Palettes
`palette=` accepts journal names from **ggsci** and standard sources:
`"npg"` (Nature), `"aaas"` (Science), `"lancet"`, `"jco"` (clinical oncology),
`"nejm"`, `"jama"`, `"ucscgb"`, `"d3"`, `"igv"`, `"startrek"`, `"simpsons"`,
`"rickandmorty"`, `"futurama"`, `"tron"`; RColorBrewer names (`"Set1"`, `"Dark2"`,
…); `"grey"`; or a hex vector `c("#00AFBB", "#E7B800", "#FC4E07")`.

## Arranging panels
```r
figure <- ggarrange(p1, p2, p3, p4,
                    labels = c("A", "B", "C", "D"),
                    ncol = 2, nrow = 2,
                    common.legend = TRUE, legend = "bottom")
annotate_figure(figure, top = text_grob("Figure 1", face = "bold"))
```

## Export
```r
ggexport(figure, filename = "figure1.pdf", width = 7, height = 6)  # inches
# or ggplot2's:
ggsave("figure1.svg", figure, width = 7, height = 6)   # vector for journals
```

## Worked examples

**Violin + inner boxplot + significance** (the classic ggpubr figure):
```r
my_comparisons <- list(c("0.5", "1"), c("1", "2"), c("0.5", "2"))
ggviolin(ToothGrowth, x = "dose", y = "len", fill = "dose",
         palette = c("#00AFBB", "#E7B800", "#FC4E07"),
         add = "boxplot", add.params = list(fill = "white")) +
  stat_compare_means(comparisons = my_comparisons, label = "p.signif") +
  stat_compare_means(label.y = 50)   # global test
```

**Boxplot with jittered points, journal palette:**
```r
ggboxplot(df, x = "day", y = "total_bill", color = "day",
          palette = "npg", add = "jitter") +
  stat_compare_means(comparisons = list(c("Thur","Fri"), c("Sat","Sun")))
```

**Scatter with correlation:**
```r
ggscatter(mtcars, x = "wt", y = "mpg",
          add = "reg.line", conf.int = TRUE,
          color = "cyl", palette = "jco") +
  stat_cor(aes(color = cyl))
```

**Ordered lollipop chart:**
```r
ggdotchart(df, x = "name", y = "value", color = "group", palette = "jco",
           sorting = "descending", add = "segments", rotate = TRUE)
```
