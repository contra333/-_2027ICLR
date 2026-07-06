# Section 4 Real-Result Replacement Checklist

This checklist tracks every place where the current Section 4 draft uses
synthetic placeholders. None of the listed numeric values should be reported as
experimental evidence. Before submission, replace them with measured results,
regenerate the figures and tables, and remove placeholder-only warnings.

## Global Replacement Rules

- Replace every `SYNTHETIC PLACEHOLDER -- DO NOT REPORT` figure annotation,
  table caption phrase, and CSV warning after measured results are inserted.
- Remove or rewrite the `Placeholder status` paragraph in
  `sections/04_experiments.tex` once Section 4 contains real measurements.
- Rewrite the placeholder caveats in `sections/05_discussion.tex` so the
  Discussion describes measured findings rather than planned diagnostic
  comparisons.
- Regenerate every Section 4 figure from measured data using a reproducible
  script. Do not manually edit final PDF figures.
- Replace `results/processed/placeholders/` with a real processed-results
  directory or clearly rename the directory used by the final figure script.
- Keep the score-direction convention fixed before reporting AUROC, AUPR-IN,
  and FPR95. CTM-style and NECO-style diagnostics should remain appendix probes
  unless their score conventions and implementations are fixed.
- Keep DDU wording as DDU-style Gaussian feature-density / GMM unless the full
  original DDU training and implementation protocol is actually reproduced.

## Section Text To Revisit

### `sections/04_experiments.tex`

- Subsection `Experimental Protocol and Scope`:
  - Replace the placeholder-status paragraph.
  - Confirm final ID datasets, OOD datasets, architectures, optimizer set,
    detector families, and appendix scope.
  - Confirm whether ViT/Swin remain appendix-only after real runs.
- Subsection `Does Weight-Decay Coupling Move Geometry Without Changing Accuracy?`:
  - Replace all qualitative claims that currently describe expected behavior
    with measured findings.
  - Report measured ID accuracy, NC metrics, norm statistics, covariance
    spectra, effective rank, and detector-family responses along the
    AdamW-to-Adam interpolation.
  - State whether accuracy is stable enough for the interpolation to isolate
    geometry from model quality.
- Subsection `Is the Adam--AdamW Gap Larger Than the SGD--SGDW Gap?`:
  - Replace the placeholder comparison of adaptive and non-adaptive gaps with
    measured standardized geometry distances and detector-family distances.
  - State whether \(\Delta_{\mathrm{adapt}}>\Delta_{\mathrm{nonadapt}}\)
    actually holds by architecture.
- Subsection `Do Detector Families Inherit the Geometry Shift?`:
  - Replace the placeholder heatmap interpretation with measured
    optimizer-relative AUROC, AUPR-IN, and FPR95 gaps.
  - Confirm the matched SGD anchor for every architecture and dataset.
- Subsection `Does Radial Geometry Explain Raw Distance Failures?`:
  - Replace raw-to-L2 placeholder gaps with measured paired gaps.
  - Report whether L2 normalization recovers Mahalanobis and kNN behavior, and
    identify regimes where the raw gap remains after L2 normalization.
- Subsection `Are Covariance Failures Localized by Covariance Controls?`:
  - Replace covariance-control placeholder gaps with measured full, tied,
    diagonal, shrinkage, and PCA-projected covariance results.
  - State whether failures are localized to covariance estimation,
    ill-conditioning, nuisance directions, or broader representation mismatch.
- Subsection `Do Prototype and Subspace Diagnostics Track NC-Aligned Regimes?`:
  - Replace prototype/subspace placeholder trends with measured NC alignment,
    class-mean geometry, classifier-feature alignment, effective rank, PCA
    explained variance, residual energy, CTM-style scores, NECO-style scores,
    prototype-cosine scores, and residual-subspace scores.
  - Move CTM/NECO-style diagnostics to appendix if their score conventions are
    not fixed.
- Subsection `Can ID Geometry Recommend Detector Diagnostics?`:
  - Replace rule-based selector dummy hit rates with measured selector
    evaluation, or remove the hit-rate column if the selector is not evaluated.
  - Define the final selector target: detector family, diagnostic control type,
    or statistically competitive set across OOD regimes.

### `sections/05_discussion.tex`

- Rewrite the first two Discussion subsections after real values are available:
  - Replace language about planned diagnostic comparisons with measured
    evidence.
  - Update references to figures if the final figure numbering or labels
    change.
  - Remove the statement that Section 4 numbers are synthetic placeholders.
- Revisit the limitations section:
  - Replace draft-stage placeholder limitations with limitations tied to the
    actual dataset, architecture, optimizer, detector, seed, and OOD coverage.
  - Report any remaining ID-accuracy or calibration imbalance after measured
    results are inserted.

## Table Files To Replace

### `tables/tab_exp_protocol_matrix.tex`

- Confirm the final experimental protocol rather than leaving this as a planned
  matrix.
- Remove `SYNTHETIC PLACEHOLDER -- DO NOT REPORT as results` from the caption.
- Update datasets, architectures, optimizer sweep, detector families, metrics,
  and geometry channels if the actual runs differ from the current plan.

### `tables/tab_dummy_interpolation_summary.tex`

Replace every dummy value:

- `gamma`
- `ID Acc.`
- `NC1`
- `Norm std.`
- `Eff. rank`
- `Near AUROC gap`

Rename the file and label if it becomes a real result table, for example
`tab_interpolation_summary.tex`.

### `tables/tab_dummy_covariance_controls.tex`

Replace every dummy AUROC gap:

- `Full GMM`
- `Tied GMM`
- `Diag. GMM`
- `Shrinkage GMM`
- `PCA-GMM`
- Rows for `SGDW`, `Adam`, and `AdamW`

Add mean/std, confidence intervals, or seed-count notation if the final paper
reports aggregate values.

### `tables/tab_dummy_geometry_selector.tex`

Replace or remove:

- `Dummy hit rate`
- Rule thresholds implied by each ID geometry signal
- Suggested diagnostic choices if the final selector uses learned or
  statistically selected rules
- CTM-style and NECO-style entries if their score conventions are not fixed

Rename the file and label if it becomes a real result table, for example
`tab_geometry_selector.tex`.

## Placeholder CSV Files To Replace

All files below live in `results/processed/placeholders/`. They should be
replaced by measured processed outputs, and the `placeholder_notice` column
should be removed from final result CSVs.

### `fig2_wd_coupling_interpolation.csv`

Replace:

- `gamma`
- `accuracy`
- `nc1`
- `norm_std`
- `eff_rank`
- `raw_maha_gap`
- `l2_maha_gap`

### `fig3_adaptive_coupling_gap.csv`

Replace:

- `architecture`
- `nonadaptive_gap`
- `adaptive_gap`

The final values should be computed from standardized ID geometry fingerprints
and, if retained, matched detector-family output distances.

### `fig4_detector_family_delta_heatmap.csv`

Replace optimizer-relative detector gaps for:

- `MSP`
- `MaxLogit`
- `Energy`
- `Maha`
- `Maha-L2`
- `kNN`
- `kNN-L2`
- `GMM-shrinkage`

Confirm whether additional detector families such as angular or subspace
readouts belong in the main heatmap.

### `fig5_l2_recovery_paths.csv`

Replace paired raw/L2 gaps for:

- `optimizer`
- `detector`
- `raw_gap`
- `l2_gap`

Ensure every raw score and L2-normalized score uses the same checkpoint, ID
feature bank, OOD split, metric, and score-orientation convention.

### `fig6_prototype_subspace_alignment.csv`

Replace:

- `optimizer`
- `nc_alignment`
- `ctm_gap`
- `residual_energy`
- `neco_gap`

Only keep CTM-style or NECO-style values in the main figure if the score
conventions are fixed and documented.

## Figure Files To Regenerate

All current Section 4 figure PDFs are synthetic placeholders and must be
regenerated from measured values:

- `figures/fig2_wd_coupling_interpolation.pdf`
- `figures/fig3_adaptive_coupling_gap.pdf`
- `figures/fig4_detector_family_delta_heatmap.pdf`
- `figures/fig5_l2_recovery_paths.pdf`
- `figures/fig6_prototype_subspace_alignment.pdf`

After regeneration:

- Remove the in-figure `SYNTHETIC PLACEHOLDER -- DO NOT REPORT` note.
- Update captions in `sections/04_experiments.tex` from placeholder layout
  descriptions to measured-result interpretations.
- Verify final figures are still readable at ICLR text width.
- Run `make` and confirm the figures are included in `main.pdf`.

## Figure Script To Replace Or Refactor

### `scripts/make_section4_placeholder_figures.py`

The current script hard-codes dummy values. Before submission:

- Replace hard-coded dummy constants with reads from measured processed CSVs.
- Rename the script if the final source is no longer placeholder-only.
- Remove the `PLACEHOLDER_NOTICE` CSV column and PDF annotation from final
  outputs.
- Preserve deterministic output paths and matplotlib-only reproducibility unless
  the project intentionally moves to a richer plotting stack.
- Keep a test that verifies expected final CSV inputs and PDF outputs exist.

## Final Verification Before Submission

- Run a repository-wide search for:
  - `SYNTHETIC PLACEHOLDER`
  - `DO NOT REPORT`
  - `dummy`
  - `placeholder`
- Confirm any remaining occurrences are intentional notes, not main-paper
  claims or result artifacts.
- Run `make test`.
- Run `make`.
- Inspect `main.log` for unresolved references or citations.
- Review the compiled `main.pdf` to confirm no placeholder captions,
  annotations, or dummy result labels remain.
