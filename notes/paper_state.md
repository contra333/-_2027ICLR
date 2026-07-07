# Paper State

Last updated: 2026-07-07

## Working Title

Optimizer-Conditioned Geometry for Feature-Based Uncertainty

## Current Stage

The repository contains a framework-safe ICLR-style paper draft. The main text
has been reorganized around optimizer-induced penultimate geometry and
geometry--detector compatibility. The draft is not yet a results paper:
Section 4 still uses synthetic placeholder figures and tables to stabilize the
layout, experiment story, and replacement checklist.

## Current Core Idea

Optimizer choice is treated as a training-side geometry intervention. The paper
frames a three-step pathway: optimizer update rules shape the ID penultimate
geometry fingerprint \(G(h,W)\), detector families read different channels of
that geometry, and OOD behavior depends on compatibility between the learned
geometry and the detector readout. The intended claim is diagnostic and
compatibility-focused, not an optimizer ranking or a complete causal proof.

## Current Draft Structure

- Section 3 now states the framework through empirical questions rather than
  numbered H1/H2/H3 hypotheses.
- Section 4 is organized around result-message subsections, but all numeric
  figure/table content remains synthetic placeholder material.
- Section 5 discusses compatibility, diagnostic interpretability, and scope
  without treating placeholder figures as measured results.
- Section 6 gives a short two-paragraph conclusion focused on the
  optimizer--geometry--detector pathway.
- Appendix A5 keeps the optimizer update derivations and the detailed
  question-to-experiment map.

## Evidence Status

Web ChatGPT should treat every Section 4 value, plotted trend, and dummy table
entry as non-evidence. The placeholder figures and tables are layout and
analysis targets only. Any empirical claim about Adam, AdamW, SGD, SGDW,
Mahalanobis, kNN, DDU-style Gaussian feature-density, CTM, NECO, prototype, or
subspace readouts requires measured data from the local experiment pipeline or
explicit user-provided evidence.

DDU-style Gaussian feature-density refers to the post-hoc Gaussian density
scoring component unless an experiment explicitly fixes a faithful DDU training
recipe. CTM-, NECO-, prototype-, and residual-subspace diagnostics should be
treated as extended probes unless their score conventions and implementations
are fixed in the same evaluation protocol.

## Current Review Questions

1. Is the geometry--detector compatibility claim narrow and compelling enough
   for an ICLR-style paper?
2. Does Section 4 specify the right measured evidence needed to replace the
   synthetic placeholders?
3. Which figure or table should carry the main empirical claim once real
   results are available?
4. Are the diagnostic controls sufficient to distinguish radial, covariance,
   local-neighborhood, angular, and subspace channels?
5. What would a skeptical reviewer identify as the weakest unsupported link
   before real Section 4 measurements are inserted?

## Codex Role

Codex applies approved changes locally: LaTeX edits, table edits, reproducible
figure scripts, context regeneration, compilation, and verification. Durable
paper decisions should be recorded in repository notes before regenerating
`docs/gpt_context.md`.
