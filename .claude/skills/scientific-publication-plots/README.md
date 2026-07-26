# scientific-publication-plots

A Claude skill for creating **publication-ready scientific figures** — clean,
journal-quality plots and multi-panel diagrams in the style of *Cell*, *Nature*,
and *Science* — using **[cnsplots](https://github.com/faridrashidi/cnsplots)**
(Python) or **[ggpubr](https://rpkgs.datanovia.com/ggpubr/)** (R).

It covers the ~18 core plot types (box, violin, strip, stacked bar, bar, pie,
Venn, donut, regression, survival/Kaplan-Meier, KDE, volcano, ROC, Sankey, ridge,
slope, scatter, clustered heatmap) with automatic statistical significance
annotations, journal color palettes, and multi-panel composites with A/B/C labels.

## Install in Claude Code

1. Unzip the archive.
2. Place the entire `scientific-publication-plots` folder into either:
   - `~/.claude/skills/scientific-publication-plots/` (personal, recommended), or
   - `.claude/skills/scientific-publication-plots/` inside a project.
3. Start a new Claude Code session — it will be auto-discovered.

You can also invoke it explicitly with `/scientific-publication-plots`.

## Install in Claude.ai (web)

Zip this folder (so the folder sits at the root of the zip), then in Claude.ai go
to **Customize → Skills → Upload** and select the zip.

## What's inside

```
scientific-publication-plots/
├── SKILL.md                     # the skill: when to use it + the workflow
├── README.md                    # this file
├── references/
│   ├── plot-gallery.md          # A–R selection guide: which plot for which question
│   ├── cnsplots-api.md          # full verified Python API (signatures, gotchas)
│   ├── ggpubr-api.md            # full R API (functions, stats, palettes, arrange)
│   └── palettes.md              # palette catalog + accessibility
├── scripts/
│   ├── setup_env.sh             # create a venv and install cnsplots
│   ├── make_figure.py           # CLI: CSV → single-panel publication figure
│   └── gallery_demo.py          # verified templates for all 18 plots + a composite
└── assets/
    └── example_expression.csv   # small runnable example dataset
```

## Quick start (Python)

```bash
# from inside the skill folder
bash scripts/setup_env.sh                       # installs cnsplots into .venv-cnsplots

.venv-cnsplots/bin/python scripts/make_figure.py \
    --data assets/example_expression.csv --kind violinplot \
    --x group --y expression --pairs "Control,DrugA;Control,DrugB" \
    --palette Nature --ylabel "Expression (TPM)" --out figure.svg
```

Or reproduce the full showcase gallery:

```bash
.venv-cnsplots/bin/python scripts/gallery_demo.py --out ./gallery_out
```

## Requirements

- **Python ≥ 3.10** for cnsplots (`pip install cnsplots`; pulls in matplotlib,
  seaborn, pandas, scanpy, lifelines, gseapy).
- **R** with `install.packages("ggpubr")` for the R path.

## Credits

Built around cnsplots (Farid Rashidi) and ggpubr (Alboukadel Kassambara). The
API reference and example scripts in this package were verified against
cnsplots 0.5.0.
