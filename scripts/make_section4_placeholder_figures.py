#!/usr/bin/env python3
"""Generate Section 4 synthetic placeholder CSV files and PDF figures."""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
from typing import Any


MPLCONFIGDIR = Path(os.environ.get("MPLCONFIGDIR", "/tmp/matplotlib-cache"))
MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER_NOTICE = "SYNTHETIC PLACEHOLDER -- DO NOT REPORT"
CSV_SUBDIR = Path("results") / "processed" / "placeholders"
FIGURE_SUBDIR = Path("figures")
FIG_WIDTH = 5.39

WD_COUPLING_INTERPOLATION = [
    {
        "gamma": "0.00",
        "accuracy": 95.4,
        "nc1": 0.081,
        "norm_std": 1.42,
        "eff_rank": 38.0,
        "raw_maha_gap": -0.072,
        "l2_maha_gap": -0.010,
    },
    {
        "gamma": "0.25",
        "accuracy": 95.5,
        "nc1": 0.069,
        "norm_std": 1.21,
        "eff_rank": 34.5,
        "raw_maha_gap": -0.044,
        "l2_maha_gap": -0.008,
    },
    {
        "gamma": "0.50",
        "accuracy": 95.6,
        "nc1": 0.055,
        "norm_std": 1.04,
        "eff_rank": 30.2,
        "raw_maha_gap": -0.018,
        "l2_maha_gap": -0.006,
    },
    {
        "gamma": "0.75",
        "accuracy": 95.5,
        "nc1": 0.043,
        "norm_std": 0.89,
        "eff_rank": 26.1,
        "raw_maha_gap": -0.006,
        "l2_maha_gap": -0.002,
    },
    {
        "gamma": "1.00",
        "accuracy": 95.4,
        "nc1": 0.037,
        "norm_std": 0.77,
        "eff_rank": 23.8,
        "raw_maha_gap": 0.004,
        "l2_maha_gap": 0.001,
    },
]

ADAPTIVE_COUPLING_GAP = [
    {"architecture": "VGG-style", "nonadaptive_gap": 0.18, "adaptive_gap": 0.61},
    {"architecture": "WideResNet", "nonadaptive_gap": 0.12, "adaptive_gap": 0.47},
    {"architecture": "ConvNeXt", "nonadaptive_gap": 0.15, "adaptive_gap": 0.39},
]

DETECTOR_FAMILY_DELTA_HEATMAP = [
    {
        "optimizer": "SGDW",
        "MSP": 0.002,
        "MaxLogit": 0.001,
        "Energy": 0.003,
        "Maha": -0.006,
        "Maha-L2": -0.002,
        "kNN": -0.004,
        "kNN-L2": -0.001,
        "GMM-shrinkage": -0.002,
    },
    {
        "optimizer": "Adam",
        "MSP": 0.011,
        "MaxLogit": 0.014,
        "Energy": 0.018,
        "Maha": -0.031,
        "Maha-L2": -0.006,
        "kNN": -0.026,
        "kNN-L2": -0.004,
        "GMM-shrinkage": -0.010,
    },
    {
        "optimizer": "AdamW",
        "MSP": 0.017,
        "MaxLogit": 0.021,
        "Energy": 0.026,
        "Maha": -0.084,
        "Maha-L2": -0.012,
        "kNN": -0.069,
        "kNN-L2": -0.009,
        "GMM-shrinkage": -0.027,
    },
]

L2_RECOVERY_PATHS = [
    {"optimizer": "SGDW", "detector": "Maha", "raw_gap": -0.006, "l2_gap": -0.002},
    {"optimizer": "SGDW", "detector": "kNN", "raw_gap": -0.004, "l2_gap": -0.001},
    {"optimizer": "Adam", "detector": "Maha", "raw_gap": -0.031, "l2_gap": -0.006},
    {"optimizer": "Adam", "detector": "kNN", "raw_gap": -0.026, "l2_gap": -0.004},
    {"optimizer": "AdamW", "detector": "Maha", "raw_gap": -0.084, "l2_gap": -0.012},
    {"optimizer": "AdamW", "detector": "kNN", "raw_gap": -0.069, "l2_gap": -0.009},
]

PROTOTYPE_SUBSPACE_ALIGNMENT = [
    {
        "optimizer": "SGD",
        "nc_alignment": 0.92,
        "ctm_gap": 0.004,
        "residual_energy": 0.18,
        "neco_gap": 0.002,
    },
    {
        "optimizer": "SGDW",
        "nc_alignment": 0.88,
        "ctm_gap": 0.002,
        "residual_energy": 0.21,
        "neco_gap": 0.000,
    },
    {
        "optimizer": "Adam",
        "nc_alignment": 0.76,
        "ctm_gap": -0.006,
        "residual_energy": 0.34,
        "neco_gap": -0.004,
    },
    {
        "optimizer": "AdamW",
        "nc_alignment": 0.61,
        "ctm_gap": -0.019,
        "residual_energy": 0.49,
        "neco_gap": -0.012,
    },
]


def set_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.4,
            "axes.titlesize": 8.2,
            "axes.labelsize": 7.8,
            "xtick.labelsize": 7.0,
            "ytick.labelsize": 7.0,
            "legend.fontsize": 6.8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.linewidth": 0.7,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
        }
    )


def _float_series(rows: list[dict[str, Any]], key: str) -> list[float]:
    return [float(row[key]) for row in rows]


def _minmax(values: list[float]) -> list[float]:
    low = min(values)
    high = max(values)
    if high == low:
        return [0.0 for _value in values]
    return [(value - low) / (high - low) for value in values]


def _write_csv(
    csv_dir: Path, filename: str, rows: list[dict[str, Any]], fieldnames: list[str]
) -> Path:
    path = csv_dir / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        handle.write(f"# {PLACEHOLDER_NOTICE}\n")
        writer = csv.DictWriter(
            handle, fieldnames=["placeholder_notice", *fieldnames]
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({"placeholder_notice": PLACEHOLDER_NOTICE, **row})
    return path


def _annotate_placeholder(fig: plt.Figure) -> None:
    fig.text(
        0.5,
        -0.035,
        PLACEHOLDER_NOTICE,
        ha="center",
        va="top",
        fontsize=6.5,
        color="#8a1f11",
    )


def _save_pdf(fig: plt.Figure, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    _annotate_placeholder(fig)
    fig.savefig(path, format="pdf", bbox_inches="tight")
    plt.close(fig)
    return path


def plot_wd_coupling_interpolation(rows: list[dict[str, Any]], figure_dir: Path) -> Path:
    gammas = _float_series(rows, "gamma")
    fig, axes = plt.subplots(1, 3, figsize=(FIG_WIDTH, 2.05), layout="constrained")

    axes[0].plot(gammas, _float_series(rows, "accuracy"), marker="o", color="#3568a8")
    axes[0].set_xlabel("coupled fraction gamma")
    axes[0].set_ylabel("ID accuracy placeholder (%)")
    axes[0].set_title("(a) ID quality")
    axes[0].set_ylim(95.25, 95.75)

    geometry_series = {
        "NC1": _minmax(_float_series(rows, "nc1")),
        "norm std.": _minmax(_float_series(rows, "norm_std")),
        "eff. rank": _minmax(_float_series(rows, "eff_rank")),
    }
    for label, values in geometry_series.items():
        axes[1].plot(gammas, values, marker="o", linewidth=1.2, label=label)
    axes[1].set_xlabel("coupled fraction gamma")
    axes[1].set_ylabel("normalized placeholder geometry")
    axes[1].set_title("(b) Geometry channel")
    axes[1].legend(frameon=False, loc="best")

    axes[2].axhline(0.0, color="#5f5f5f", linewidth=0.7, linestyle=":")
    axes[2].plot(
        gammas,
        _float_series(rows, "raw_maha_gap"),
        marker="o",
        color="#b6403a",
        label="raw Maha",
    )
    axes[2].plot(
        gammas,
        _float_series(rows, "l2_maha_gap"),
        marker="s",
        color="#26735b",
        label="L2 Maha",
    )
    axes[2].set_xlabel("coupled fraction gamma")
    axes[2].set_ylabel("AUROC gap placeholder")
    axes[2].set_title("(c) Detector readout")
    axes[2].legend(frameon=False, loc="lower right")

    return _save_pdf(fig, figure_dir / "fig2_wd_coupling_interpolation.pdf")


def plot_adaptive_coupling_gap(rows: list[dict[str, Any]], figure_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, 2.25), layout="constrained")
    x_positions = list(range(len(rows)))
    width = 0.34
    nonadapt = _float_series(rows, "nonadaptive_gap")
    adapt = _float_series(rows, "adaptive_gap")

    ax.bar(
        [x - width / 2 for x in x_positions],
        nonadapt,
        width=width,
        label="SGD--SGDW",
        color="#8fb6d9",
        edgecolor="#303030",
        linewidth=0.4,
    )
    ax.bar(
        [x + width / 2 for x in x_positions],
        adapt,
        width=width,
        label="Adam--AdamW",
        color="#d89a7c",
        edgecolor="#303030",
        linewidth=0.4,
    )
    ax.set_xticks(x_positions, [row["architecture"] for row in rows])
    ax.set_ylabel("standardized placeholder gap")
    ax.set_xlabel("architecture family")
    ax.legend(frameon=False, loc="upper right")
    ax.set_ylim(0.0, 0.70)

    return _save_pdf(fig, figure_dir / "fig3_adaptive_coupling_gap.pdf")


def plot_detector_family_delta_heatmap(
    rows: list[dict[str, Any]], figure_dir: Path
) -> Path:
    detector_columns = [
        "MSP",
        "MaxLogit",
        "Energy",
        "Maha",
        "Maha-L2",
        "kNN",
        "kNN-L2",
        "GMM-shrinkage",
    ]
    values = [[float(row[column]) for column in detector_columns] for row in rows]

    fig, ax = plt.subplots(figsize=(FIG_WIDTH, 2.45), layout="constrained")
    image = ax.imshow(values, cmap="RdBu_r", vmin=-0.09, vmax=0.09, aspect="auto")
    ax.set_xticks(range(len(detector_columns)), detector_columns, rotation=35, ha="right")
    ax.set_yticks(range(len(rows)), [row["optimizer"] for row in rows])
    ax.set_xlabel("detector family")
    ax.set_ylabel("optimizer")

    for i, row in enumerate(values):
        for j, value in enumerate(row):
            text_color = "white" if abs(value) > 0.045 else "#202020"
            ax.text(j, i, f"{value:+.3f}", ha="center", va="center", color=text_color)

    colorbar = fig.colorbar(image, ax=ax, shrink=0.86)
    colorbar.set_label("AUROC gap placeholder")

    return _save_pdf(fig, figure_dir / "fig4_detector_family_delta_heatmap.pdf")


def plot_l2_recovery_paths(rows: list[dict[str, Any]], figure_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, 2.3), layout="constrained")
    colors = {"SGDW": "#5b8cc0", "Adam": "#7a6aae", "AdamW": "#bd5b4b"}
    markers = {"Maha": "o", "kNN": "s"}

    for row in rows:
        optimizer = str(row["optimizer"])
        detector = str(row["detector"])
        ax.plot(
            [0, 1],
            [float(row["raw_gap"]), float(row["l2_gap"])],
            marker=markers[detector],
            color=colors[optimizer],
            linewidth=1.3,
            label=f"{optimizer} {detector}",
        )
        ax.text(
            1.03,
            float(row["l2_gap"]),
            f"{optimizer} {detector}",
            va="center",
            fontsize=6.4,
        )

    ax.axhline(0.0, color="#5f5f5f", linewidth=0.7, linestyle=":")
    ax.set_xlim(-0.08, 1.48)
    ax.set_xticks([0, 1], ["raw", "L2-normalized"])
    ax.set_ylabel("AUROC gap placeholder")
    ax.set_xlabel("distance-score variant")
    ax.legend(frameon=False, loc="lower left", ncols=2)

    return _save_pdf(fig, figure_dir / "fig5_l2_recovery_paths.pdf")


def plot_prototype_subspace_alignment(
    rows: list[dict[str, Any]], figure_dir: Path
) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(FIG_WIDTH, 2.25), layout="constrained")

    nc_rows = sorted(rows, key=lambda row: float(row["nc_alignment"]))
    axes[0].plot(
        _float_series(nc_rows, "nc_alignment"),
        _float_series(nc_rows, "ctm_gap"),
        marker="o",
        color="#3568a8",
        linewidth=1.2,
    )
    for row in nc_rows:
        axes[0].text(
            float(row["nc_alignment"]) + 0.006,
            float(row["ctm_gap"]),
            str(row["optimizer"]),
            fontsize=6.5,
            va="center",
        )
    axes[0].axhline(0.0, color="#5f5f5f", linewidth=0.7, linestyle=":")
    axes[0].set_xlabel("NC alignment placeholder")
    axes[0].set_ylabel("CTM-style gap placeholder")
    axes[0].set_title("(a) Prototype readout")

    residual_rows = sorted(rows, key=lambda row: float(row["residual_energy"]))
    axes[1].plot(
        _float_series(residual_rows, "residual_energy"),
        _float_series(residual_rows, "neco_gap"),
        marker="s",
        color="#bd5b4b",
        linewidth=1.2,
    )
    for row in residual_rows:
        axes[1].text(
            float(row["residual_energy"]) + 0.008,
            float(row["neco_gap"]),
            str(row["optimizer"]),
            fontsize=6.5,
            va="center",
        )
    axes[1].axhline(0.0, color="#5f5f5f", linewidth=0.7, linestyle=":")
    axes[1].set_xlabel("residual energy placeholder")
    axes[1].set_ylabel("NECO-style gap placeholder")
    axes[1].set_title("(b) Subspace readout")

    return _save_pdf(fig, figure_dir / "fig6_prototype_subspace_alignment.pdf")


def generate_placeholder_artifacts(output_root: Path | str = ROOT) -> dict[str, list[Path]]:
    root = Path(output_root)
    csv_dir = root / CSV_SUBDIR
    figure_dir = root / FIGURE_SUBDIR
    set_style()

    csv_outputs = [
        _write_csv(
            csv_dir,
            "fig2_wd_coupling_interpolation.csv",
            WD_COUPLING_INTERPOLATION,
            [
                "gamma",
                "accuracy",
                "nc1",
                "norm_std",
                "eff_rank",
                "raw_maha_gap",
                "l2_maha_gap",
            ],
        ),
        _write_csv(
            csv_dir,
            "fig3_adaptive_coupling_gap.csv",
            ADAPTIVE_COUPLING_GAP,
            ["architecture", "nonadaptive_gap", "adaptive_gap"],
        ),
        _write_csv(
            csv_dir,
            "fig4_detector_family_delta_heatmap.csv",
            DETECTOR_FAMILY_DELTA_HEATMAP,
            [
                "optimizer",
                "MSP",
                "MaxLogit",
                "Energy",
                "Maha",
                "Maha-L2",
                "kNN",
                "kNN-L2",
                "GMM-shrinkage",
            ],
        ),
        _write_csv(
            csv_dir,
            "fig5_l2_recovery_paths.csv",
            L2_RECOVERY_PATHS,
            ["optimizer", "detector", "raw_gap", "l2_gap"],
        ),
        _write_csv(
            csv_dir,
            "fig6_prototype_subspace_alignment.csv",
            PROTOTYPE_SUBSPACE_ALIGNMENT,
            ["optimizer", "nc_alignment", "ctm_gap", "residual_energy", "neco_gap"],
        ),
    ]

    figure_outputs = [
        plot_wd_coupling_interpolation(WD_COUPLING_INTERPOLATION, figure_dir),
        plot_adaptive_coupling_gap(ADAPTIVE_COUPLING_GAP, figure_dir),
        plot_detector_family_delta_heatmap(DETECTOR_FAMILY_DELTA_HEATMAP, figure_dir),
        plot_l2_recovery_paths(L2_RECOVERY_PATHS, figure_dir),
        plot_prototype_subspace_alignment(PROTOTYPE_SUBSPACE_ALIGNMENT, figure_dir),
    ]

    return {"csv": csv_outputs, "figures": figure_outputs}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Section 4 synthetic placeholder figures."
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT,
        help="Repository root where results/ and figures/ should be written.",
    )
    args = parser.parse_args()
    outputs = generate_placeholder_artifacts(output_root=args.output_root)
    for path in [*outputs["csv"], *outputs["figures"]]:
        print(path.relative_to(args.output_root))


if __name__ == "__main__":
    main()
