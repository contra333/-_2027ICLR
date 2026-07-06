#!/usr/bin/env python3
"""Generate Figure 1: optimizer-conditioned geometry compatibility."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable


MPLCONFIGDIR = Path(os.environ.get("MPLCONFIGDIR", "/tmp/matplotlib-cache"))
MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from cairosvg import svg2pdf
from matplotlib.patches import FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "figures" / "fig1_optimizer_geometry_pipeline.pdf"
DEFAULT_SVG = ROOT / "figures" / "fig1_optimizer_geometry_pipeline.svg"
ICLR_TEXT_WIDTH_IN = 5.5
LATEX_INCLUDE_WIDTH = 0.98
FIGURE_SIZE = (ICLR_TEXT_WIDTH_IN * LATEX_INCLUDE_WIDTH, 1.95)
FIGURE_FONT = "Nimbus Roman"


COLORS = {
    "ink": "#20242A",
    "muted": "#5C6470",
    "line": "#A7ADB8",
    "panel_edge": "#D7DCE2",
    "divider": "#E7E9EE",
    "marker": "#8F96A3",
    "background": "#FFFFFF",
}


def get_pipeline_spec() -> list[dict[str, object]]:
    return [
        {
            "title": "Optimizer choice",
            "subtitle": "training",
            "items": ["SGD", "Adam", "AdamW"],
        },
        {
            "title": "Penultimate geometry",
            "subtitle": "feature geometry",
            "items": [
                "NC structure",
                "radial norm",
                "covariance",
                "local density",
                "ID subspace",
            ],
        },
        {
            "title": "Detector readout",
            "subtitle": "score channel",
            "items": [
                "logit margin",
                "GMM density",
                "kNN locality",
                "angular align.",
                "subspace align.",
            ],
        },
        {
            "title": "Reliability behavior",
            "subtitle": "OOD signal",
            "items": ["AUROC gap", "FPR95", "calibration"],
        },
    ]


def _set_style() -> None:
    plt.rcParams.update(
        {
            "font.family": FIGURE_FONT,
            "font.serif": [FIGURE_FONT],
            "font.sans-serif": [FIGURE_FONT],
            "font.size": 6.5,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "axes.linewidth": 0.8,
        }
    )


def _panel(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    subtitle: str,
    items: Iterable[str],
) -> None:
    panel = Rectangle(
        (x, y),
        w,
        h,
        linewidth=0.8,
        edgecolor=COLORS["panel_edge"],
        facecolor=COLORS["background"],
        zorder=2,
    )
    ax.add_patch(panel)

    title_display = {
        "Optimizer choice": "Optimizer\nchoice",
        "Penultimate geometry": "Penultimate\ngeometry",
        "Detector readout": "Detector\nreadout",
        "Reliability behavior": "Reliability\nbehavior",
    }.get(title, title)

    pad_x = 0.018
    title_x = x + pad_x
    top_y = y + h - 0.052

    ax.text(
        title_x,
        top_y,
        title_display,
        ha="left",
        va="top",
        color=COLORS["ink"],
        fontsize=8.1,
        fontweight="bold",
        linespacing=0.96,
        zorder=4,
    )
    ax.text(
        title_x,
        y + h - 0.245,
        subtitle,
        ha="left",
        va="top",
        color=COLORS["muted"],
        fontsize=7.0,
        zorder=4,
    )
    ax.plot(
        [x + pad_x, x + w - pad_x],
        [y + h - 0.315, y + h - 0.315],
        color=COLORS["divider"],
        linewidth=0.7,
        zorder=3,
    )

    item_list = list(items)
    start_y = y + h - 0.395
    gap = min(0.08, 0.34 / max(1, len(item_list) - 1)) if len(item_list) > 1 else 0.0
    marker_x = x + pad_x + 0.008
    text_x = marker_x + 0.02
    for idx, item in enumerate(item_list):
        yy = start_y - idx * gap
        ax.scatter(
            [marker_x],
            [yy],
            s=7,
            color=COLORS["marker"],
            linewidth=0.0,
            zorder=4,
        )
        ax.text(
            text_x,
            yy,
            item,
            ha="left",
            va="center",
            color=COLORS["ink"],
            fontsize=7.2,
            zorder=4,
        )


def _arrow(ax: plt.Axes, x0: float, x1: float, y: float) -> None:
    arrow = FancyArrowPatch(
        (x0, y),
        (x1, y),
        arrowstyle="-|>",
        mutation_scale=13,
        linewidth=1.25,
        color=COLORS["line"],
        shrinkA=2,
        shrinkB=2,
        zorder=2,
    )
    ax.add_patch(arrow)


def build_figure(
    pdf_path: str | Path = DEFAULT_PDF,
    svg_path: str | Path | None = DEFAULT_SVG,
) -> None:
    _set_style()
    pdf_path = Path(pdf_path)
    svg_path = Path(svg_path) if svg_path is not None else pdf_path.with_suffix(".svg")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.parent.mkdir(parents=True, exist_ok=True)

    stages = get_pipeline_spec()

    fig = plt.figure(figsize=FIGURE_SIZE)
    fig.patch.set_facecolor(COLORS["background"])
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    panel_w = 0.205
    panel_h = 0.82
    y = 0.09
    xs = [0.018, 0.276, 0.534, 0.792]
    for x, stage in zip(xs, stages):
        _panel(
            ax,
            x=x,
            y=y,
            w=panel_w,
            h=panel_h,
            title=str(stage["title"]),
            subtitle=str(stage["subtitle"]),
            items=stage["items"],
        )

    arrow_y = y + panel_h / 2 + 0.005
    for idx in range(3):
        _arrow(ax, xs[idx] + panel_w + 0.012, xs[idx + 1] - 0.012, arrow_y)

    fig.savefig(svg_path)
    plt.close(fig)
    svg2pdf(url=str(svg_path), write_to=str(pdf_path))


def main() -> None:
    build_figure()


if __name__ == "__main__":
    main()
