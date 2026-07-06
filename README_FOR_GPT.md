# README For Web ChatGPT

This repository is an ICLR-style LaTeX paper workspace. The human researcher uses web ChatGPT for paper strategy and logic review, and uses local Ubuntu/Codex for concrete editing, compiling, plotting, and table generation.

## Read Order

Read these files first, in this order:

1. `docs/gpt_context.md`
2. `notes/paper_state.md`
3. `notes/decision_log.md`
4. `AGENTS.md`
5. `main.tex`

If `docs/gpt_context.md` exists, treat it as the preferred review bundle. The source files remain authoritative if the generated bundle and source files disagree.

## What To Review

Focus on:

- problem definition
- central claim and contribution
- section-level logic
- whether the method and experiments support the claim
- missing baselines, metrics, datasets, ablations, or diagnostic checks
- whether figures and tables answer the right reviewer questions
- overclaiming, unsupported causal language, or double-blind risks

## What Not To Do

Do not invent experimental results, numeric values, citations, datasets, or baselines. If evidence is missing, say what evidence is needed.

Do not directly rewrite large LaTeX sections unless explicitly asked. Prefer producing a concrete instruction list that Codex can apply locally.

Do not assume every figure or table is final. Treat current figures and tables as working artifacts unless `notes/paper_state.md` says they are final.

## Preferred Output Format

Use this structure when giving feedback:

1. Core diagnosis
2. Highest-impact changes
3. Section-by-section notes
4. Figure/table recommendations
5. Concrete Codex handoff tasks

For Codex handoff tasks, name exact files such as `sections/01_introduction.tex`, `sections/03_method.tex`, `tables/tab_geometry_fingerprint.tex`, or `scripts/make_main_experiment_figures.py`.
