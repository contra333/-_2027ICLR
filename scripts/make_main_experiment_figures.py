#!/usr/bin/env python3
"""Generate main experiment Figures 2--4."""

from __future__ import annotations

import os
import warnings
from pathlib import Path


MPLCONFIGDIR = Path(os.environ.get("MPLCONFIGDIR", "/tmp/matplotlib-cache"))
MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from matplotlib.ticker import FormatStrFormatter


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"
PROCESSED_DIR = ROOT / "results" / "processed" / "wrn350_selected_3seed_20260612"
GEOMETRY_LONG_CSV = PROCESSED_DIR / "geometry_mean_std_long.csv"

GEOMETRY_TABLE = ROOT / "tables" / "tab_geometry_fingerprint.tex"
DETECTOR_TABLE = ROOT / "tables" / "tab_detector_family_auroc.tex"
DIAGNOSTIC_TABLE = ROOT / "tables" / "tab_diagnostic_gap_summary.tex"

ICLR_TEXT_WIDTH_IN = 5.5
LATEX_INCLUDE_WIDTH = 0.98
FIG_WIDTH = ICLR_TEXT_WIDTH_IN * LATEX_INCLUDE_WIDTH

CONFIG_ORDER = [
    ("sgd_lr1e-1_wd5e-4_anchor", "SGD, wd 5e-4"),
    ("sgd_lr1e-1_wd2e-4", "SGD, wd 2e-4"),
    ("adam_lr1e-3_wd1e-4", "Adam"),
    ("adamw_lr5e-3_wd1e-4", "AdamW, wd 1e-4"),
    ("adamw_lr5e-3_wd5e-4_anchor", "AdamW, wd 5e-4"),
]
ANCHOR_LABEL = "SGD, wd 5e-4"
TARGET_CONFIGS = ["Adam", "AdamW, wd 1e-4", "AdamW, wd 5e-4"]
DETECTORS = ["Logit", "Maha", "Maha-L2", "kNN", "kNN-L2", "GMM-shr."]
SCORE_CONVENTION = "higher-is-ID"

FIGURE_OUTPUTS = {
    "fig2": [
        FIGURE_DIR / "fig2_geometry_fingerprint_heatmap.pdf",
        FIGURE_DIR / "fig2_geometry_fingerprint_heatmap.png",
    ],
    "fig3": [
        FIGURE_DIR / "fig3_detector_delta_auroc_heatmap.pdf",
        FIGURE_DIR / "fig3_detector_delta_auroc_heatmap.png",
    ],
    "fig4": [
        FIGURE_DIR / "fig4_l2_diagnostic_recovery.pdf",
        FIGURE_DIR / "fig4_l2_diagnostic_recovery.png",
    ],
}


def set_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.5,
            "axes.titlesize": 8.5,
            "axes.labelsize": 8.0,
            "xtick.labelsize": 7.2,
            "ytick.labelsize": 7.2,
            "legend.fontsize": 7.0,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.linewidth": 0.7,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
        }
    )


def geometry_table_values() -> pd.DataFrame:
    data = {
        "SGD, wd 5e-4": {
            "NC1": 0.051,
            "NC3": 0.950,
            "InterDist": 16.62,
            "WithinVar": 18.61,
            "Norm mean": 14.23,
            "Norm std.": 1.79,
            "Eff. rank": 59.55,
        },
        "SGD, wd 2e-4": {
            "NC1": 0.067,
            "NC3": 0.938,
            "InterDist": 14.28,
            "WithinVar": 17.52,
            "Norm mean": 12.88,
            "Norm std.": 1.74,
            "Eff. rank": 57.92,
        },
        "Adam": {
            "NC1": 0.190,
            "NC3": 0.905,
            "InterDist": 13.34,
            "WithinVar": 23.86,
            "Norm mean": 14.39,
            "Norm std.": 2.03,
            "Eff. rank": 25.55,
        },
        "AdamW, wd 1e-4": {
            "NC1": 0.277,
            "NC3": 0.613,
            "InterDist": 5.23,
            "WithinVar": 10.08,
            "Norm mean": 6.21,
            "Norm std.": 1.32,
            "Eff. rank": 76.92,
        },
        "AdamW, wd 5e-4": {
            "NC1": 0.269,
            "NC3": 0.615,
            "InterDist": 5.47,
            "WithinVar": 10.62,
            "Norm mean": 6.50,
            "Norm std.": 1.38,
            "Eff. rank": 74.15,
        },
    }
    return pd.DataFrame.from_dict(data, orient="index").loc[
        [label for _, label in CONFIG_ORDER]
    ]


def add_condition_number_if_available(geometry: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    if not GEOMETRY_LONG_CSV.exists():
        print("condition number not found; omitted from Figure 2")
        return geometry, False

    long_df = pd.read_csv(GEOMETRY_LONG_CSV)
    cond_df = long_df[long_df["metric"] == "condition_number_clipped"]
    cond_by_key = dict(zip(cond_df["config_label"], cond_df["mean"]))

    values = []
    for config_key, _label in CONFIG_ORDER:
        if config_key not in cond_by_key:
            print("condition number not found; omitted from Figure 2")
            return geometry, False
        values.append(float(cond_by_key[config_key]))

    geometry = geometry.copy()
    geometry["Cond. #"] = values
    print("condition number found; included in Figure 2")
    return geometry, True


def standardized_delta_from_anchor(values: pd.DataFrame) -> pd.DataFrame:
    anchor = values.loc[ANCHOR_LABEL]
    std = values.std(axis=0, ddof=0)
    delta = values.copy()

    for column in values.columns:
        if np.isclose(std[column], 0.0):
            warnings.warn(
                f"zero across-config std for {column}; standardized deltas set to 0",
                RuntimeWarning,
            )
            delta[column] = 0.0
        else:
            delta[column] = (values[column] - anchor[column]) / std[column]

    delta.loc[ANCHOR_LABEL] = 0.0
    return delta


def detector_auroc_table_values() -> dict[str, pd.DataFrame]:
    near = pd.DataFrame(
        {
            "Logit": [0.855, 0.845, 0.900, 0.900, 0.901],
            "Maha": [0.867, 0.860, 0.568, 0.416, 0.418],
            "Maha-L2": [0.886, 0.870, 0.728, 0.856, 0.855],
            "kNN": [0.903, 0.903, 0.849, 0.568, 0.590],
            "kNN-L2": [0.903, 0.902, 0.881, 0.890, 0.888],
            "GMM-shr.": [0.907, 0.905, 0.804, 0.793, 0.796],
        },
        index=[label for _, label in CONFIG_ORDER],
    )
    far = pd.DataFrame(
        {
            "Logit": [0.939, 0.933, 0.920, 0.922, 0.900],
            "Maha": [0.974, 0.963, 0.635, 0.541, 0.610],
            "Maha-L2": [0.984, 0.982, 0.917, 0.988, 0.992],
            "kNN": [0.937, 0.935, 0.881, 0.674, 0.762],
            "kNN-L2": [0.955, 0.952, 0.911, 0.988, 0.991],
            "GMM-shr.": [0.957, 0.946, 0.737, 0.758, 0.782],
        },
        index=[label for _, label in CONFIG_ORDER],
    )
    return {"Near-OOD": near, "Far/easy-far OOD": far}


def detector_delta_tables() -> dict[str, pd.DataFrame]:
    auroc = detector_auroc_table_values()
    deltas: dict[str, pd.DataFrame] = {}
    for regime, table in auroc.items():
        delta = table.loc[TARGET_CONFIGS, DETECTORS].subtract(
            table.loc[ANCHOR_LABEL, DETECTORS], axis="columns"
        )
        deltas[regime] = delta.T
    return deltas


def assert_expected_detector_deltas(deltas: dict[str, pd.DataFrame]) -> None:
    expected_near = pd.DataFrame(
        {
            "Adam": [0.045, -0.299, -0.158, -0.054, -0.022, -0.103],
            "AdamW, wd 1e-4": [0.045, -0.451, -0.030, -0.335, -0.013, -0.114],
            "AdamW, wd 5e-4": [0.046, -0.449, -0.031, -0.313, -0.015, -0.111],
        },
        index=DETECTORS,
    )
    expected_far = pd.DataFrame(
        {
            "Adam": [-0.019, -0.339, -0.067, -0.056, -0.044, -0.220],
            "AdamW, wd 1e-4": [-0.017, -0.433, 0.004, -0.263, 0.033, -0.199],
            "AdamW, wd 5e-4": [-0.039, -0.364, 0.008, -0.175, 0.036, -0.175],
        },
        index=DETECTORS,
    )
    np.testing.assert_allclose(
        deltas["Near-OOD"].loc[DETECTORS, TARGET_CONFIGS].to_numpy(),
        expected_near.loc[DETECTORS, TARGET_CONFIGS].to_numpy(),
        atol=5e-4,
    )
    np.testing.assert_allclose(
        deltas["Far/easy-far OOD"].loc[DETECTORS, TARGET_CONFIGS].to_numpy(),
        expected_far.loc[DETECTORS, TARGET_CONFIGS].to_numpy(),
        atol=5e-4,
    )
    print("Figure 3 delta checks passed")


def draw_heatmap(
    ax: plt.Axes,
    data: pd.DataFrame,
    cmap: str,
    norm: TwoSlopeNorm,
    *,
    annotate: bool = False,
    annotation_fmt: str = ".3f",
    show_ylabels: bool = True,
) -> matplotlib.collections.QuadMesh:
    rows, cols = data.shape
    x_edges = np.arange(cols + 1)
    y_edges = np.arange(rows + 1)
    mesh = ax.pcolormesh(
        x_edges,
        y_edges,
        data.to_numpy(),
        cmap=cmap,
        norm=norm,
        edgecolors="white",
        linewidth=0.75,
        shading="flat",
    )
    ax.set_xlim(0, cols)
    ax.set_ylim(rows, 0)
    ax.set_xticks(np.arange(cols) + 0.5)
    ax.set_xticklabels(data.columns, rotation=35, ha="right", rotation_mode="anchor")
    ax.set_yticks(np.arange(rows) + 0.5)
    ax.set_yticklabels(data.index if show_ylabels else [])
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    if annotate:
        for row_idx in range(rows):
            for col_idx in range(cols):
                value = data.iat[row_idx, col_idx]
                text_color = "white" if abs(value) > 0.27 else "#1F2328"
                ax.text(
                    col_idx + 0.5,
                    row_idx + 0.5,
                    format(value, annotation_fmt),
                    ha="center",
                    va="center",
                    fontsize=7.0,
                    color=text_color,
                )
    return mesh


def add_vector_colorbar(
    ax: plt.Axes,
    *,
    cmap: str,
    norm: TwoSlopeNorm,
    label: str,
    ticks: list[float],
    labelsize: float = 8.0,
    ticksize: float = 7.0,
    x0: float = 1.03,
    y0: float = 0.10,
    width: float = 0.025,
    height: float = 0.82,
    tick_format: str = "%.1f",
) -> plt.Axes:
    cax = ax.inset_axes([x0, y0, width, height])
    y_edges = np.linspace(norm.vmin, norm.vmax, 257)
    values = ((y_edges[:-1] + y_edges[1:]) / 2.0).reshape(-1, 1)
    cax.pcolormesh(
        [0, 1],
        y_edges,
        values,
        cmap=cmap,
        norm=norm,
        shading="flat",
        linewidth=0,
    )
    cax.set_xlim(0, 1)
    cax.set_ylim(norm.vmin, norm.vmax)
    cax.set_xticks([])
    cax.set_yticks(ticks)
    cax.yaxis.set_major_formatter(FormatStrFormatter(tick_format))
    cax.yaxis.tick_right()
    cax.yaxis.set_label_position("right")
    cax.tick_params(axis="y", labelsize=ticksize, width=0.7, length=3)
    cax.set_ylabel(label, fontsize=labelsize, rotation=270, labelpad=13)
    for spine in cax.spines.values():
        spine.set_linewidth(0.7)
    return cax


def save_figure(fig: plt.Figure, paths: list[Path]) -> None:
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix.lower() == ".png":
            fig.savefig(path, dpi=320, bbox_inches="tight")
        else:
            fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def make_figure2() -> bool:
    geometry, has_condition = add_condition_number_if_available(geometry_table_values())
    standardized = standardized_delta_from_anchor(geometry)
    limit = max(1.0, float(np.nanmax(np.abs(standardized.to_numpy()))))
    limit = float(np.ceil(limit * 2.0) / 2.0)
    norm = TwoSlopeNorm(vmin=-limit, vcenter=0.0, vmax=limit)

    fig, ax = plt.subplots(figsize=(FIG_WIDTH, 2.65), layout="constrained")
    draw_heatmap(ax, standardized, "coolwarm", norm, annotate=False)
    ax.set_xlabel("")
    ax.set_ylabel("")
    add_vector_colorbar(
        ax,
        cmap="coolwarm",
        norm=norm,
        label="Standardized difference from SGD anchor",
        ticks=[-2, -1, 0, 1, 2],
        labelsize=7.0,
        x0=1.025,
        y0=0.08,
        height=0.86,
        tick_format="%.0f",
    )
    save_figure(fig, FIGURE_OUTPUTS["fig2"])
    return has_condition


def make_figure3() -> None:
    deltas = detector_delta_tables()
    assert_expected_detector_deltas(deltas)
    max_abs = max(float(np.nanmax(np.abs(table.to_numpy()))) for table in deltas.values())
    limit = float(np.ceil(max_abs * 20.0) / 20.0)
    norm = TwoSlopeNorm(vmin=-limit, vcenter=0.0, vmax=limit)

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(FIG_WIDTH, 2.45),
        layout="constrained",
    )
    for ax, (regime, data) in zip(axes, deltas.items()):
        draw_heatmap(
            ax,
            data,
            "RdBu_r",
            norm,
            annotate=True,
            show_ylabels=(ax is axes[0]),
        )
        ax.set_title(regime, pad=5)
        ax.set_xlabel("")
        ax.set_ylabel("")
    add_vector_colorbar(
        axes[1],
        cmap="RdBu_r",
        norm=norm,
        label=r"$\Delta$AUROC",
        ticks=[-0.4, -0.2, 0.0, 0.2, 0.4],
        labelsize=8.0,
        x0=1.04,
        y0=0.08,
        height=0.86,
        tick_format="%.1f",
    )
    save_figure(fig, FIGURE_OUTPUTS["fig3"])


def make_figure4() -> None:
    deltas = detector_delta_tables()["Near-OOD"]
    panel_specs = [
        ("Mahalanobis", "Maha", "Maha-L2"),
        ("kNN", "kNN", "kNN-L2"),
    ]
    colors = {
        "Adam": "#0072B2",
        "AdamW, wd 1e-4": "#D55E00",
        "AdamW, wd 5e-4": "#009E73",
    }
    markers = {"Adam": "o", "AdamW, wd 1e-4": "s", "AdamW, wd 5e-4": "^"}
    linestyles = {"Adam": "-", "AdamW, wd 1e-4": "--", "AdamW, wd 5e-4": "-."}

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(FIG_WIDTH, 2.25),
        layout="constrained",
        sharey=True,
    )
    x = np.array([0, 1])
    for ax, (title, raw_key, l2_key) in zip(axes, panel_specs):
        ax.axhline(0.0, color="#6E7781", linestyle="--", linewidth=0.9, zorder=1)
        for config in TARGET_CONFIGS:
            y = np.array([deltas.loc[raw_key, config], deltas.loc[l2_key, config]])
            ax.plot(
                x,
                y,
                color=colors[config],
                marker=markers[config],
                linestyle=linestyles[config],
                linewidth=1.35,
                markersize=4.4,
                label=config,
                zorder=3,
            )
        ax.set_title(title, pad=5)
        ax.set_xticks(x)
        ax.set_xticklabels(["Raw", "L2"])
        ax.set_xlim(-0.25, 1.25)
        ax.set_ylim(-0.50, 0.055)
        ax.grid(axis="y", color="#E5E8EC", linewidth=0.7)
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)

    axes[0].set_ylabel(r"$\Delta$AUROC vs. SGD anchor")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=3,
        frameon=False,
    )
    save_figure(fig, FIGURE_OUTPUTS["fig4"])


def main() -> None:
    set_style()
    print(f"score convention: {SCORE_CONVENTION}")
    print(f"source table: {GEOMETRY_TABLE.relative_to(ROOT)}")
    print(f"source table: {DETECTOR_TABLE.relative_to(ROOT)}")
    print(f"source table: {DIAGNOSTIC_TABLE.relative_to(ROOT)}")
    has_condition = make_figure2()
    make_figure3()
    make_figure4()
    for paths in FIGURE_OUTPUTS.values():
        for path in paths:
            print(f"wrote {path.relative_to(ROOT)}")
    print(f"condition_number_included={has_condition}")


if __name__ == "__main__":
    main()
