#!/usr/bin/env python3
"""Reproduce the cnsplots showcase (panels A-R) as verified, runnable examples.

Every function here is a copy-paste starting point for one plot type. Run the
whole file to render a PNG per plot plus a multi-panel composite into an output
directory, or read individual functions as templates. Data is loaded from
cnsplots' bundled datasets (tips, iris) or synthesized so the file is fully
self-contained.

    .venv-cnsplots/bin/python gallery_demo.py --out ./gallery_out

The panel letters match the showcase figure:
  A boxplot   B violinplot  C stripplot   D stackplot   E barplot(h)  F pieplot
  G vennplot  H donutplot   I regplot     J survivalplot K kdeplot     L volcanoplot
  M rocplot   N sankeyplot  O ridgeplot   P slopeplot   Q scatterplot R heatmapplot
"""
from __future__ import annotations

import argparse
import os

import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd
import cnsplots as cns


def render_all(out_dir: str) -> list[tuple[str, str]]:
    os.makedirs(out_dir, exist_ok=True)
    rng = np.random.default_rng(0)
    tips = cns.datasets.load_dataset("tips")
    iris = cns.datasets.load_dataset("iris")
    results: list[tuple[str, str]] = []

    def save(name):
        cns.savefig(os.path.join(out_dir, f"{name}.png"))
        results.append((name, "ok"))

    # A — Boxplot with pairwise significance (auto Mann-Whitney U).
    cns.figure(width=50, height=60, color_cycle="Nature")
    cns.boxplot(data=tips, x="day", y="total_bill",
                pairs=[("Thur", "Fri"), ("Sat", "Sun")])
    save("A_boxplot")

    # B — Violin with embedded box + significance.
    cns.figure(width=50, height=60, color_cycle="Cell")
    cns.violinplot(data=iris, x="species", y="sepal_width",
                   pairs=[("setosa", "versicolor"), ("versicolor", "virginica")])
    save("B_violinplot")

    # C — Strip plot, points colored by a second grouping.
    cns.figure(width=60, height=60, color_cycle="Set1")
    cns.stripplot(data=tips, x="day", y="tip", hue="sex")
    save("C_stripplot")

    # D — Stacked proportions of a category within each x group.
    cns.figure(width=55, height=60, color_cycle="Nature")
    cns.stackplot(data=tips, x="day", stack="sex")
    save("D_stackplot")

    # E — Horizontal bar plot (swap x/y so the categorical axis is vertical).
    cns.figure(width=65, height=45, color_cycle="Bold")
    cns.barplot(data=tips, x="total_bill", y="day")
    save("E_barplot_horizontal")

    # F — Pie chart of category counts.
    cns.figure(width=60, height=60, color_cycle="Science")
    cns.pieplot(data=iris, x="species")
    save("F_pieplot")

    # G — Venn diagram of 2-3 sets.
    cns.figure(width=60, height=60)
    cns.vennplot(lists=[set(range(0, 40)), set(range(25, 70)), set(range(50, 90))],
                 labels=["Set A", "Set B", "Set C"])
    save("G_vennplot")

    # H — Donut chart.
    cns.figure(width=60, height=60, color_cycle="Science")
    cns.donutplot(data=iris, x="species")
    save("H_donutplot")

    # I — Regression plot with fit + correlation.
    cns.figure(width=60, height=60)
    cns.regplot(data=tips, x="total_bill", y="tip")
    save("I_regplot")

    # J — Kaplan-Meier survival with log-rank test (synthetic cohort).
    n = 200
    arm = rng.choice(["Treatment", "Control"], n)
    surv = pd.DataFrame({
        "time": rng.exponential(np.where(arm == "Treatment", 60, 40), n),
        "status": rng.binomial(1, 0.7, n),
        "arm": arm,
    })
    cns.figure(width=65, height=60, color_cycle="Set1")
    cns.survivalplot(data=surv, duration="time", event="status", hue="arm")
    save("J_survivalplot")

    # K — Kernel density by group.
    cns.figure(width=60, height=60, color_cycle="Nature")
    cns.kdeplot(data=iris, x="petal_length", hue="species")
    save("K_kdeplot")

    # L — Volcano plot (synthetic differential expression).
    m = 500
    volc = pd.DataFrame({
        "log2FoldChange": rng.normal(0, 1.6, m),
        "-log10(adjp)": -np.log10(rng.uniform(0, 1, m) ** 3 + 1e-6),
        "symbol": [f"Gene{i}" for i in range(m)],
    })
    cns.figure(width=65, height=65)
    cns.volcanoplot(data=volc)
    save("L_volcanoplot")

    # M — ROC curves for multiple models (synthetic scores).
    k = 300
    y = rng.binomial(1, 0.5, k)
    roc = pd.DataFrame({
        "label": y,
        "Model A": np.clip(y * 0.25 + rng.normal(0.4, 0.3, k), 0, 1),
        "Model B": np.clip(y * 0.6 + rng.normal(0.2, 0.2, k), 0, 1),
    })
    cns.figure(width=65, height=60, color_cycle="Set1")
    cns.rocplot(data=roc, true_label_col="label", pred_prob_cols=["Model A", "Model B"])
    save("M_rocplot")

    # N — Sankey flows between two categoricals.
    cns.figure(width=50, height=65)
    cns.sankeyplot(data=tips[["day", "sex"]], x="day", y="sex")
    save("N_sankeyplot")

    # O — Ridge plot (stacked densities) per category.
    cns.figure(width=60, height=60)
    cns.ridgeplot(data=iris, x="petal_length", y="species")
    save("O_ridgeplot")

    # P — Slope plot: two paired conditions (hue) per subject, grouped by x.
    rows = []
    sid = 0
    for site in ["site1", "site2", "site3"]:
        for _ in range(12):
            sid += 1
            base = rng.normal(2, 0.5)
            rows.append({"site": site, "value": base, "condition": "healthy", "id": sid})
            rows.append({"site": site, "value": base + rng.normal(1.0, 0.4),
                         "condition": "disease", "id": sid})
    slope = pd.DataFrame(rows)
    cns.figure(width=55, height=60, color_cycle="Set1")
    cns.slopeplot(data=slope, x="site", y="value", hue="condition", pair="id")
    save("P_slopeplot")

    # Q — Scatter plot colored by group.
    cns.figure(width=60, height=60, color_cycle="Set1")
    cns.scatterplot(data=iris, x="sepal_length", y="sepal_width", hue="species")
    save("Q_scatterplot")

    # R — Clustered heatmap. cnsplots takes an AnnData: obs=rows, var=cols,
    #     with annotation columns pulled from .obs / .var.
    try:
        import anndata as ad
        n_obs, n_var = 30, 24
        X = rng.normal(0, 1, (n_obs, n_var))
        X[:15, :12] += 2.0
        X[15:, 12:] += 2.0
        adata = ad.AnnData(
            X=X,
            obs=pd.DataFrame({"Ensemble": rng.choice(["ens0", "ens1", "ens2"], n_obs)},
                             index=[f"P{i}" for i in range(n_obs)]),
            var=pd.DataFrame({"blobs": rng.choice(["b0", "b1", "b2"], n_var)},
                             index=[f"g{j}" for j in range(n_var)]),
        )
        cns.figure(width=95, height=75, color_map="BuRd_custom")
        cns.heatmapplot(adata, row_annotation=["Ensemble"], col_annotation=["blobs"],
                        row_cluster=True, col_cluster=True)
        save("R_heatmapplot")
    except Exception as e:  # anndata should ship with cnsplots; guard just in case
        results.append(("R_heatmapplot", f"skipped: {e}"))

    # Composite — the intended multi-panel idiom.
    mp = cns.multipanel(max_width=380, title="Figure 1")
    for lab, fn in [
        ("A", lambda: cns.boxplot(data=tips, x="day", y="total_bill",
                                  pairs=[("Thur", "Fri"), ("Sat", "Sun")])),
        ("B", lambda: cns.violinplot(data=iris, x="species", y="sepal_width",
                                     pairs=[("setosa", "versicolor")])),
        ("C", lambda: cns.scatterplot(data=iris, x="sepal_length", y="sepal_width",
                                      hue="species")),
        ("D", lambda: cns.kdeplot(data=iris, x="petal_length", hue="species")),
    ]:
        mp.panel(lab, width=90, height=90, pad_left=42, pad_top=12)
        fn()
    cns.savefig(os.path.join(out_dir, "composite_figure1.png"))
    results.append(("composite_figure1", "ok"))

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="./gallery_out", help="Output directory.")
    args = ap.parse_args()
    results = render_all(args.out)
    ok = sum(1 for _, s in results if s == "ok")
    for name, status in results:
        print(f"  {name:24s} {status}")
    print(f"\n{ok}/{len(results)} rendered into {args.out}")


if __name__ == "__main__":
    main()
