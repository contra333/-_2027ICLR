# Internal TODO: Experiment Coverage for a Stronger Main Claim

This note is for research management only. Do not include it in the paper body.
The main text should describe the reported controlled CIFAR-10 / WRN-28-10
setting and move coverage limitations to appendix or discussion.

## 1. Tighter Accuracy Matching

Current issue: the SGD anchor has about 1.3--1.5 percentage points higher ID test
accuracy than the Adam/AdamW selected configurations.

Actions:
- Add a local LR/WD grid for each optimizer.
- Select configurations by ID validation accuracy using the same rule for all
  optimizers.
- Keep the existing five configurations as pilot or appendix evidence if better
  matched configurations are found.

Paper wording:
- Use "accuracy-controlled selected configurations" for the current draft.
- Use "accuracy-matched" only after the tighter selection is complete.

## 2. Full OOD Coverage

Current issue: reported CIFAR-10 ID results cover CIFAR-100, TinyImageNet, SVHN,
and MNIST. Textures and Places365 are not included in the reported coverage.

Actions:
- Add Textures and Places365 evaluation for CIFAR-10 ID.
- Recompute near/far aggregate metrics after adding the full coverage.
- Consider far-OOD datasets beyond MNIST when avoiding easy-far dominance.

Paper wording:
- Current draft: "near-OOD and far/easy-far controls."
- After full coverage: stronger OpenOOD-style near/far protocol wording.

## 3. CIFAR-100 ID Experiments

Current issue: the reported results are centered on CIFAR-10 ID.

Actions:
- Train selected SGD/Adam/AdamW configurations on CIFAR-100 ID.
- Evaluate near-OOD with CIFAR-10 and TinyImageNet.
- Evaluate far-OOD with SVHN, Textures, Places365, and any additional selected
  controls.
- Recheck whether Mahalanobis and DDU-style GMM need stronger shrinkage or PCA
  controls under the larger label space.

Paper wording:
- Keep CIFAR-10 as the controlled diagnostic study until CIFAR-100 results are
  ready.
- Add CIFAR-100 as robustness or an additional main subsection once complete.

## 4. CTM / NeCo Implementation

Current issue: NCC, prototype-cosine, and ViM diagnostics are present, but they
must not be renamed as CTM or NeCo.

Actions:
- Implement the official CTM score and record the score direction.
- Decide whether NeCo uses the official formula or a project-specific variant.
- Avoid temporary names such as `neco_lite` in main results.
- Record detector parameters, feature source, PCA dimension, and score direction.

Paper wording:
- Keep CTM/NeCo as conceptual probes in the readout map until results are fixed.
- Report them in main figures only after implementation and convention are fixed.

## 5. Optimizer Effect vs Hyperparameter Effect

Current issue: optimizer-specific LR/WD selection gives practical fairness, but
does not fully separate optimizer identity from hyperparameter regime.

Actions:
- Add a shared-recipe comparison with the same scheduler, LR/WD, and training
  budget where feasible.
- Keep the accuracy-controlled selected comparison for deployment-style model
  selection.
- Use the local LR/WD grid to compare multiple configurations within the same
  accuracy band.

Paper wording:
- Prefer "optimizer-conditioned geometry regimes" for the current draft.
- Use stronger causal language only when shared-recipe or local-grid controls
  support it.

## 6. Geometry--Detector Association Analysis

Current issue: five configurations and three seeds are not enough for strong
correlation or Mantel-style claims.

Actions:
- Increase the number of configurations.
- Compute seed-paired `Delta_geo` and `Delta_det`.
- Use detector-family Spearman correlations or simple regressions as secondary
  analysis.
- Treat Mantel-style analysis as an association check, not causal proof.

Paper wording:
- Main text should use descriptive paired-gap patterns.
- Association statistics belong in appendix or robustness analysis.

## 7. Figure Generation

Current issue: too many main-text tables make the paper read like a detector
benchmark.

Actions:
- Generate a geometry fingerprint heatmap from processed geometry summaries.
- Generate a detector Delta-AUROC heatmap relative to the SGD anchor.
- Generate a diagnostic recovery plot for raw vs L2 and GMM covariance controls.
- Keep full numeric tables in appendix.

Paper wording:
- Main evidence should emphasize geometry diagnosis and optimizer-detector
  compatibility.
- Appendix should carry full numerical reproducibility tables.
