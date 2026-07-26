# Color palettes

Color is meaning, not decoration. Match the palette **type** to the data:
- **Qualitative** — unordered categories (species, treatment arm). Distinct hues.
- **Sequential** — ordered magnitude (expression level, count). One hue, light→dark.
- **Diverging** — a meaningful midpoint (log2 fold-change, z-score around 0).

## cnsplots

Set the qualitative cycle and the colormap on the figure:
```python
cns.figure(width=60, height=60, color_cycle="Nature", color_map="BuRd_custom")
```
Or globally: `cns.settings.palette_qual = "Nature"` / `cns.settings.palette_seq = ...`.
Defaults are `palette_qual="Ecotyper1"`, `palette_seq="gnuplot"`.

### Qualitative (`color_cycle=`)
Verified in cnsplots 0.5.0 with their color counts:

| Name | # colors | Use for |
|---|---|---|
| `Cell` | 10 | Cell-press-style categorical |
| `Nature` | 10 | Nature-style categorical |
| `Science` | 10 | Science/AAAS-style categorical |
| `Bold` | 10 | high-saturation categorical |
| `Tableau` | 10 | familiar Tableau 10 |
| `Set1` | 9 | bright, high-contrast |
| `Set2` | 8 | soft, colorblind-friendlier |
| `Set3` | 12 | many light categories |
| `Ecotyper1` | 9 | default |
| `Ecotyper2` | 5 | small category sets |
| `Ecotyper3` | 8 | — |
| `Ecotyper4` | 9 | — |
| `Ecotyper5` | 27 | many categories |
| `Ecotyper6` | 24 | many categories |

Pick a palette with **at least as many colors as you have groups**; for 2–3
groups any of them works, for >12 use `Ecotyper5`/`Ecotyper6`.

Inspect any palette's colors:
```python
import cnsplots as cns
cns.palettes("Nature")                 # -> list of RGB tuples
cns.get_hexcolors_from_apalette([0, 1, 2], palette="Set1")  # -> ['#e41a1c', ...]
```

### Sequential / diverging (`color_map=`)
- Diverging: `BuRd_custom` (blue-white-red), `BlueRed`, `OrBu_custom`
  (orange-white-blue) — best for z-scores / log2FC heatmaps around 0.
- Sequential: `gnuplot` (default) plus any matplotlib colormap by name
  (`viridis`, `magma`, `cividis`). Prefer perceptually-uniform ones (`viridis`,
  `cividis`) for ordered magnitude.

Single named colors (constants): `cns.RED, BLUE, GREEN, ORANGE, PURPLE, PINK,
BROWN, GRAY, YELLOW, VIOLET, CHOCOLATE`.

## ggpubr (R)

`palette=` on any `gg*` function accepts:
- **Journal palettes (ggsci):** `"npg"` (Nature), `"aaas"` (Science), `"lancet"`,
  `"jco"`, `"nejm"`, `"jama"`, `"ucscgb"`, `"d3"`, `"igv"`, `"startrek"`,
  `"simpsons"`, `"rickandmorty"`, `"futurama"`, `"tron"`.
- **RColorBrewer:** `"Set1"`, `"Dark2"`, `"Paired"`, `"Blues"`, `"RdBu"`, …
- **Grayscale:** `"grey"`.
- **Custom vector:** `c("#00AFBB", "#E7B800", "#FC4E07")`.

## Accessibility
- Prefer colorblind-safe sets (`Set2`, `viridis`, `cividis`, ggsci `"npg"`/`"jco"`).
- Don't rely on red/green alone to carry meaning.
- Check that the figure still reads in grayscale — if two categories collapse,
  add a non-color cue (shape, pattern, direct labels).
- Keep the palette consistent across all panels of a multi-panel figure so a
  color means the same thing everywhere.
