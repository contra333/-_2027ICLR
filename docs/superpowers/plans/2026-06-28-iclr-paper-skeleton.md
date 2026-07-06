# ICLR Paper Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local ICLR 2026 LaTeX paper skeleton under `0628논문뼈대초안` that compiles with TeX Live and supports section-by-section drafting.

**Architecture:** Keep official ICLR style files unchanged. Use `main.tex` as the compile entrypoint, split paper prose into `sections/`, place reusable table snippets in `tables/`, and provide `Makefile` commands for local compilation.

**Tech Stack:** LaTeX, BibTeX, latexmk, ICLR 2026 official template files.

---

### Task 1: Official Template

**Files:**
- Create: `0628논문뼈대초안/iclr2026_conference.sty`
- Create: `0628논문뼈대초안/iclr2026_conference.bst`
- Create: `0628논문뼈대초안/math_commands.tex`
- Create: `0628논문뼈대초안/natbib.sty`
- Create: `0628논문뼈대초안/fancyhdr.sty`

- [x] **Step 1: Download ICLR 2026 template zip**

Run:

```bash
curl -L -o /tmp/iclr2026.zip https://github.com/ICLR/Master-Template/raw/master/iclr2026.zip
```

Expected: `/tmp/iclr2026.zip` exists and contains the official `iclr2026/` files.

- [x] **Step 2: Extract only official template files**

Run:

```bash
unzip -j -q /tmp/iclr2026.zip 'iclr2026/*' -d 0628논문뼈대초안
```

Expected: ICLR style files exist directly under `0628논문뼈대초안`.

### Task 2: Draft Structure

**Files:**
- Create: `0628논문뼈대초안/main.tex`
- Create: `0628논문뼈대초안/sections/00_abstract.tex`
- Create: `0628논문뼈대초안/sections/01_introduction.tex`
- Create: `0628논문뼈대초안/sections/02_related_work.tex`
- Create: `0628논문뼈대초안/sections/03_method.tex`
- Create: `0628논문뼈대초안/sections/04_experiments.tex`
- Create: `0628논문뼈대초안/sections/05_discussion.tex`
- Create: `0628논문뼈대초안/sections/06_conclusion.tex`
- Create: `0628논문뼈대초안/sections/a1_experimental_details.tex`
- Create: `0628논문뼈대초안/tables/main_results_plan.tex`
- Create: `0628논문뼈대초안/references.bib`

- [x] **Step 1: Add compile entrypoint**

Create `main.tex` with the ICLR 2026 style package, anonymous author setting, section inputs, bibliography, and appendix.

- [x] **Step 2: Add section skeletons**

Create section files that compile and show where to write abstract, introduction, related work, method, experiments, discussion, conclusion, and appendix content.

- [x] **Step 3: Add table and bibliography seeds**

Create a placeholder main-results table and a minimal BibTeX file with one sample citation.

### Task 3: Local Workflow

**Files:**
- Create: `0628논문뼈대초안/Makefile`
- Create: `0628논문뼈대초안/.latexmkrc`
- Create: `0628논문뼈대초안/README.md`
- Create: `0628논문뼈대초안/figures/README.md`

- [x] **Step 1: Add Makefile commands**

Provide `make`, `make watch`, `make clean`, and `make cleanall`.

- [x] **Step 2: Add usage documentation**

Document compile commands, file responsibilities, writing order, and ICLR submission cautions.

- [x] **Step 3: Verify compile**

Run:

```bash
cd 0628논문뼈대초안
make
```

Expected: `main.pdf` is generated without LaTeX errors.
