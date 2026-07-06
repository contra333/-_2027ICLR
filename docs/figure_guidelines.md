# Figure Guidelines

These rules define the local figure style for the ICLR-format paper. ICLR does
not provide a detailed figure-typography guide comparable to publisher-specific
production guides; therefore the project uses the ICLR LaTeX style file as the
primary sizing reference and uses publisher guides only as general production
advice.

## Core Rules

- Use Python `matplotlib`/`seaborn` plus `pandas` as the default workflow for
  empirical ML figures. Scripts should read curated CSV/JSON files from
  `results/processed/` and write paper-ready outputs to `figures/`.
- Prefer vector PDF outputs for plots and diagrams. Generate SVG as an auxiliary
  artifact only when SVG rendering, inspection, or SVG-to-PDF conversion is
  materially better than the native Matplotlib PDF backend.
- Keep text editable in the vector output. In Matplotlib, set `pdf.fonttype=42`
  and `svg.fonttype="none"` unless a venue requires outlined fonts.
- Use a plain white background and avoid decorative effects: no drop shadows,
  gradients, transparency tricks, 3D effects, or unnecessary texture.
- For ICLR-style schematic figures, prefer `Nimbus Roman` so figure text is close
  to the Times-like main paper font. If a plot becomes too dense, use a standard
  sans-serif font only for that empirical plot.
- ICLR uses a 5.5 inch text width. If a figure is included as
  `width=0.98\linewidth`, generate the source figure at approximately 5.39 inch
  width so it is not substantially rescaled by LaTeX.
- Keep figure text at least 7 pt at final PDF size. Use roughly 7--8 pt for
  labels, ticks, legends, and list items, and roughly 8--9 pt for short panel
  headings.
- Do not put the figure title inside the image. Put the explanatory title and
  claim in the LaTeX caption.
- Use consistent line widths, marker sizes, and spacing across all figures.
- Use colorblind-accessible palettes and never rely on color alone. Use labels,
  line styles, marker shapes, or grouping to carry the same information.
- Crop tightly enough to avoid wasted whitespace, but leave enough margin that
  labels are not clipped.
- Keep figure panels aligned on a regular grid. If panels are labeled, use
  lowercase bold panel labels such as `(a)`, `(b)`.
- For schematic figures, avoid `bbox_inches="tight"` when it changes the natural
  PDF size relative to the LaTeX insertion width.

## Data And Directory Layout

- Keep raw experiment packages under `results/raw/`. Do not edit raw logs,
  metadata, or seed-level outputs while preparing paper figures.
- Keep curated figure/table inputs under `results/processed/<experiment_id>/`.
  These files should be small CSV/JSON summaries derived from the raw package.
- Keep all reproducible figure scripts under `scripts/`. A script name should
  make its target obvious, for example `make_wrn350_ood_auroc.py`.
- Keep generated paper artifacts under `figures/`. The main artifact included by
  LaTeX should normally be a PDF, for example `figures/wrn350_ood_auroc.pdf`.
- Do not use spreadsheets or manual GUI edits as the only source of a figure.
  If a visual is adjusted manually, encode the adjustment back into the script or
  document the exact reproducible conversion step.

Recommended empirical workflow:

```text
results/raw/<experiment_package>/
    -> results/processed/<experiment_id>/*.csv
    -> scripts/make_<figure_name>.py
    -> figures/<figure_name>.pdf
    -> LaTeX \includegraphics{figures/<figure_name>.pdf}
```

## Empirical Plot Defaults

- Start empirical plot scripts with a paper context, such as
  `seaborn.set_theme(style="ticks", context="paper")`, then override only what
  the figure needs.
- Use `plt.style.use(...)`, a local `.mplstyle`, or explicit `rcParams` when a
  set of figures should share font sizes, line widths, marker sizes, and color
  cycles.
- Use `figsize` that matches the intended LaTeX insertion width: about
  3.25 inches for a half-width figure and about 5.39 inches for
  `width=0.98\linewidth` in the ICLR template.
- Use `layout="constrained"` for ordinary plots. Use `bbox_inches="tight"` at
  save time only when it does not change the intended visual scale or clip text.
- Save ordinary empirical figures with `fig.savefig(..., bbox_inches="tight")`
  unless the figure has an intentional fixed canvas size.
- Prefer direct PDF output from Matplotlib for ordinary plots. Add SVG output
  only when there is a concrete review or conversion reason.
- Use LaTeX text rendering (`usetex`) or the PGF backend only when math/font
  consistency is worth the added dependency and compile fragility.
- Use PGFPlots/TikZ mainly for simple LaTeX-native conceptual plots. For
  experiment-heavy CSV plots, prefer Python scripts.

## Raster Images

- Use raster only when the data are inherently raster images, such as example
  inputs or qualitative image grids.
- Keep raster images at sufficient resolution for their final printed size.
- Do not upscale low-resolution rasters to create artificial sharpness.

## Project Workflow

- Every generated figure should have a script under `scripts/`.
- Generated paper figures should live under `figures/`.
- Scripts should be deterministic and should not depend on manual GUI editing.
- The `research` environment should include `matplotlib`, `seaborn`, `pandas`,
  and `numpy` for empirical plots. It should also include `cairosvg` for the
  current Figure 1 SVG-to-PDF workflow.
- If a figure uses experiment outputs, the script should point to the exact
  curated file under `results/processed/`. If the script intentionally reads a
  raw file, explain why in a short comment.
- After generating a figure, verify:
  - the script runs in the `research` environment;
  - the expected PDF file is created, plus SVG/PNG only when intentionally used;
  - `pdfimages -list <figure.pdf>` reports no embedded raster images for pure
    vector diagrams or plots;
  - `make` includes the figure in `main.pdf`.

## Figure 1 Policy

Figure 1 is a conceptual schematic, not an empirical result. It should not show
AUROC numbers, detector rankings, or CTM/NeCo results that are not present in the
current experiment package. Its role is to define the paper's causal framing:

```text
optimizer choice
-> penultimate geometry
-> detector-family readout
-> OOD / reliability behavior
```

Empirical figures should separately show geometry fingerprints, detector gaps,
and diagnostic interventions.
