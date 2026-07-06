# GPT-Readable Paper Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the local ICLR paper workspace into a GitHub-backed, GPT-readable research workflow where ChatGPT can reliably inspect the current paper state without repeated zip uploads.

**Architecture:** GitHub is the canonical versioned store for the LaTeX source, scripts, figures, tables, and curated notes. A small documentation layer gives web ChatGPT a stable entry point, and a Python script generates `docs/gpt_context.md` as a single review snapshot containing the files ChatGPT should read first.

**Tech Stack:** Git, GitHub remote `<PRIVATE_REPO_URL>.git`, LaTeX, Makefile, Python 3.12 standard library, `unittest`.

---

## File Structure

- Create `.gitignore`: prevent LaTeX build byproducts, caches, old zip bundles, and raw experimental logs from entering Git.
- Create `README_FOR_GPT.md`: stable web ChatGPT entry point and review protocol.
- Create `notes/paper_state.md`: concise human-maintained state of the paper.
- Create `notes/decision_log.md`: chronological record of important research and workflow decisions.
- Create `docs/gpt_context.md`: generated single-file snapshot for web ChatGPT.
- Create `scripts/build_gpt_context.py`: deterministic context builder using only Python standard library.
- Create `tests/test_build_gpt_context.py`: tests for ordering, generated content, and recursion avoidance.
- Modify `Makefile`: add `PYTHON`, `gpt-context`, and `test` targets while preserving existing LaTeX targets.
- Initialize local Git in `$REPO_ROOT` and connect it to `<PRIVATE_REPO_URL>.git`.

## Task 1: Initialize Git Hygiene

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Write `.gitignore`**

Create `.gitignore` with this exact content:

```gitignore
# LaTeX build artifacts
*.aux
*.bbl
*.bcf
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.run.xml
*.synctex.gz
*.toc
*.lof
*.lot
*.nav
*.snm
*.vrb
*.xdv
main.pdf
iclr2026_conference.pdf
iclr2026_conference.log

# Python and local caches
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.matplotlib-cache/
.pip-cache/
.jupyter-config/
.jupyter-data/
.jupyter-runtime/
.venv/

# GPT exchange artifacts
draft_for_gpt_feedback.zip
*.zip

# Large or sensitive experiment stores
results/raw/
```

- [ ] **Step 2: Initialize Git locally**

Run:

```bash
git init -b main
git status --short
```

Expected: Git initializes on branch `main`; `git status --short` shows source files as untracked and does not show LaTeX build artifacts such as `main.aux`, `main.log`, or `draft_for_gpt_feedback.zip` after `.gitignore` exists.

- [ ] **Step 3: Add remote**

Run:

```bash
git remote add origin <PRIVATE_REPO_URL>.git
git remote -v
```

Expected:

```text
origin  <PRIVATE_REPO_URL>.git (fetch)
origin  <PRIVATE_REPO_URL>.git (push)
```

- [ ] **Step 4: Commit Git hygiene**

Run:

```bash
git add .gitignore
git commit -m "chore: initialize paper repository hygiene"
```

Expected: one commit containing only `.gitignore`.

## Task 2: Create GPT Entry Documents

**Files:**
- Create: `README_FOR_GPT.md`
- Create: `notes/paper_state.md`
- Create: `notes/decision_log.md`

- [ ] **Step 1: Create `README_FOR_GPT.md`**

Create `README_FOR_GPT.md` with this exact content:

```markdown
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
```

- [ ] **Step 2: Create `notes/paper_state.md`**

Create `notes/paper_state.md` with this exact content:

```markdown
# Paper State

Last updated: 2026-07-06

## Working Title

Optimizer-Conditioned Geometry for Feature-Based Uncertainty

## Current Stage

The project is in paper-structure reconstruction. The current LaTeX draft exists, but the logical backbone, contribution framing, experiment story, and figure/table plan are being reworked.

## Current Core Idea

The working hypothesis is that optimizer choice changes penultimate feature geometry, and that this geometry conditions how feature-based uncertainty or OOD readouts behave. The paper should make this relationship precise, identify which geometry summaries matter, and connect them to measurable detector behavior.

## Evidence Status

The repository contains a draft, planned tables, generated figures, and scripts. Web ChatGPT should treat all numeric claims and experiment conclusions as requiring source support from local result files or user-provided evidence.

## Current Review Questions

1. Is the central claim narrow enough for an ICLR paper?
2. Are the proposed geometry summaries necessary and interpretable?
3. Do the current experiments distinguish optimizer effects from incidental training differences?
4. Which table or figure should carry the main empirical claim?
5. What would a skeptical reviewer identify as the weakest unsupported link?

## Codex Role

Codex applies approved changes locally: LaTeX edits, table edits, reproducible figure scripts, compilation, and verification.
```

- [ ] **Step 3: Create `notes/decision_log.md`**

Create `notes/decision_log.md` with this exact content:

```markdown
# Decision Log

## 2026-07-06

- Adopt a private GitHub repository as the canonical versioned workspace for the paper.
- Avoid repeated zip uploads as the normal web ChatGPT workflow.
- Add `README_FOR_GPT.md` as the stable entry point for web ChatGPT.
- Add generated `docs/gpt_context.md` so web ChatGPT can review the paper from one curated text bundle.
- Keep Notion as the brainstorming and free-form thinking space, but move durable decisions into repository notes.
- Treat local Ubuntu/Codex as the execution environment for LaTeX edits, figure scripts, tables, tests, and compilation.
```

- [ ] **Step 4: Commit GPT entry documents**

Run:

```bash
git add README_FOR_GPT.md notes/paper_state.md notes/decision_log.md
git commit -m "docs: add GPT paper review entrypoints"
```

Expected: one commit containing the three new markdown files.

## Task 3: Write Context Builder Tests

**Files:**
- Create: `tests/test_build_gpt_context.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_build_gpt_context.py` with this exact content:

```python
import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "build_gpt_context.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_gpt_context", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_file(root: Path, relative_path: str, content: str) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


class BuildGptContextTest(unittest.TestCase):
    def test_collect_text_files_orders_entrypoints_before_sections(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_file(root, "sections/01_introduction.tex", "Intro text")
            write_file(root, "tables/tab_main.tex", "Table text")
            write_file(root, "README_FOR_GPT.md", "GPT entry")
            write_file(root, "AGENTS.md", "Agent rules")
            write_file(root, "README.md", "Project readme")
            write_file(root, "main.tex", "\\input{sections/01_introduction}")

            relative_paths = [
                path.relative_to(root).as_posix()
                for path in module.collect_text_files(root)
            ]

        self.assertEqual(
            relative_paths[:4],
            ["README_FOR_GPT.md", "AGENTS.md", "README.md", "main.tex"],
        )
        self.assertIn("sections/01_introduction.tex", relative_paths)
        self.assertIn("tables/tab_main.tex", relative_paths)

    def test_build_context_includes_source_contents_and_git_fallback(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_file(root, "README_FOR_GPT.md", "Read me first")
            write_file(root, "main.tex", "\\section{Introduction}")
            write_file(root, "sections/00_abstract.tex", "Abstract claim")

            context = module.build_context(root)

        self.assertIn("# GPT Review Context", context)
        self.assertIn("Git unavailable or uninitialized", context)
        self.assertIn("## File: README_FOR_GPT.md", context)
        self.assertIn("Read me first", context)
        self.assertIn("## File: sections/00_abstract.tex", context)
        self.assertIn("Abstract claim", context)

    def test_write_context_excludes_existing_generated_context(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_file(root, "README_FOR_GPT.md", "fresh entry")
            write_file(root, "docs/gpt_context.md", "old generated text")

            output_path = module.write_context(root)
            generated = output_path.read_text(encoding="utf-8")

        self.assertEqual(output_path.relative_to(root).as_posix(), "docs/gpt_context.md")
        self.assertIn("fresh entry", generated)
        self.assertNotIn("old generated text", generated)

    def test_binary_artifact_index_lists_figures_without_embedding_bytes(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_file(root, "README_FOR_GPT.md", "entry")
            figure_path = root / "figures" / "fig1.pdf"
            figure_path.parent.mkdir(parents=True, exist_ok=True)
            figure_path.write_bytes(b"%PDF-1.7 fake")

            context = module.build_context(root)

        self.assertIn("figures/fig1.pdf", context)
        self.assertIn("13 bytes", context)
        self.assertNotIn("%PDF-1.7 fake", context)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
${HOME}/envs/research/bin/python -m unittest tests/test_build_gpt_context.py -v
```

Expected: failure because `scripts/build_gpt_context.py` does not exist yet.

## Task 4: Implement Context Builder

**Files:**
- Create: `scripts/build_gpt_context.py`
- Modify: `docs/gpt_context.md`

- [ ] **Step 1: Create `scripts/build_gpt_context.py`**

Create `scripts/build_gpt_context.py` with this exact content:

```python
#!/usr/bin/env python3
"""Build a curated single-file context bundle for web ChatGPT review."""

from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_RELATIVE_PATH = Path("docs/gpt_context.md")

ENTRYPOINT_FILES = [
    Path("README_FOR_GPT.md"),
    Path("AGENTS.md"),
    Path("README.md"),
    Path("main.tex"),
]

TEXT_GLOBS = [
    "sections/*.tex",
    "tables/*.tex",
    "docs/figure_guidelines.md",
    "figures/README.md",
    "notes/*.md",
    "references.bib",
]

BINARY_GLOBS = [
    "figures/*.pdf",
    "figures/*.png",
    "figures/*.svg",
    "main.pdf",
]


def run_git(root: Path, args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "Git unavailable or uninitialized"

    output = completed.stdout.strip()
    return output if output else "(empty)"


def detect_language(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".tex":
        return "tex"
    if suffix == ".bib":
        return "bibtex"
    if suffix == ".py":
        return "python"
    if suffix == ".md":
        return "markdown"
    return "text"


def collect_text_files(root: Path) -> list[Path]:
    output_path = root / OUTPUT_RELATIVE_PATH
    collected: list[Path] = []
    seen: set[Path] = set()

    def add(path: Path) -> None:
        if not path.exists() or not path.is_file():
            return
        resolved = path.resolve()
        if resolved == output_path.resolve() or resolved in seen:
            return
        seen.add(resolved)
        collected.append(path)

    for relative_path in ENTRYPOINT_FILES:
        add(root / relative_path)

    for pattern in TEXT_GLOBS:
        for path in sorted(root.glob(pattern)):
            add(path)

    return collected


def collect_binary_artifacts(root: Path) -> list[Path]:
    artifacts: list[Path] = []
    seen: set[Path] = set()
    for pattern in BINARY_GLOBS:
        for path in sorted(root.glob(pattern)):
            if not path.is_file():
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            artifacts.append(path)
    return artifacts


def format_file_block(root: Path, path: Path) -> str:
    relative_path = path.relative_to(root).as_posix()
    language = detect_language(path)
    content = path.read_text(encoding="utf-8")
    return "\n".join(
        [
            f"## File: {relative_path}",
            "",
            f"```{language}",
            content.rstrip(),
            "```",
            "",
        ]
    )


def format_binary_index(root: Path) -> str:
    artifacts = collect_binary_artifacts(root)
    if not artifacts:
        return "No binary figure or PDF artifacts found.\n"

    lines = []
    for path in artifacts:
        relative_path = path.relative_to(root).as_posix()
        size = path.stat().st_size
        lines.append(f"- `{relative_path}` ({size:,} bytes)")
    return "\n".join(lines) + "\n"


def build_context(root: Path = ROOT) -> str:
    root = root.resolve()
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    commit = run_git(root, ["rev-parse", "--short", "HEAD"])
    branch = run_git(root, ["branch", "--show-current"])
    status = run_git(root, ["status", "--short"])

    parts = [
        "# GPT Review Context",
        "",
        "This file is generated by `scripts/build_gpt_context.py`.",
        "Use it as the first-read bundle for web ChatGPT review. Source files remain authoritative.",
        "",
        "## Snapshot",
        "",
        f"- Generated at: {generated_at}",
        f"- Git branch: {branch}",
        f"- Git commit: {commit}",
        "",
        "## Git Status",
        "",
        "```text",
        status,
        "```",
        "",
        "## Binary Artifact Index",
        "",
        format_binary_index(root).rstrip(),
        "",
        "# Selected Text Sources",
        "",
    ]

    for path in collect_text_files(root):
        parts.append(format_file_block(root, path).rstrip())
        parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def write_context(root: Path = ROOT) -> Path:
    root = root.resolve()
    output_path = root / OUTPUT_RELATIVE_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_context(root), encoding="utf-8")
    return output_path


def main() -> None:
    output_path = write_context(ROOT)
    print(output_path.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run context builder tests**

Run:

```bash
${HOME}/envs/research/bin/python -m unittest tests/test_build_gpt_context.py -v
```

Expected: all four tests pass.

- [ ] **Step 3: Generate `docs/gpt_context.md`**

Run:

```bash
${HOME}/envs/research/bin/python scripts/build_gpt_context.py
```

Expected:

```text
docs/gpt_context.md
```

- [ ] **Step 4: Inspect generated context**

Run:

```bash
sed -n '1,120p' docs/gpt_context.md
```

Expected: the output starts with `# GPT Review Context`, includes snapshot metadata, lists binary artifacts, and then includes `README_FOR_GPT.md`.

- [ ] **Step 5: Commit context builder**

Run:

```bash
git add scripts/build_gpt_context.py tests/test_build_gpt_context.py docs/gpt_context.md
git commit -m "feat: add GPT review context builder"
```

Expected: one commit containing the script, tests, and generated context bundle.

## Task 5: Add Makefile Workflow Commands

**Files:**
- Modify: `Makefile`

- [ ] **Step 1: Replace `Makefile` with expanded targets**

Replace the full `Makefile` content with:

```makefile
MAIN := main
LATEXMK := latexmk
PYTHON ?= $${RESEARCH_PYTHON:-$${HOME}/envs/research/bin/python}

.PHONY: all pdf watch clean cleanall gpt-context test

all: pdf

pdf:
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error $(MAIN).tex

watch:
	$(LATEXMK) -pdf -pvc -interaction=nonstopmode -halt-on-error $(MAIN).tex

gpt-context:
	$(PYTHON) scripts/build_gpt_context.py

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

clean:
	$(LATEXMK) -c $(MAIN).tex

cleanall:
	$(LATEXMK) -C $(MAIN).tex
```

- [ ] **Step 2: Verify GPT context target**

Run:

```bash
make gpt-context
```

Expected:

```text
${HOME}/envs/research/bin/python scripts/build_gpt_context.py
docs/gpt_context.md
```

- [ ] **Step 3: Verify tests**

Run:

```bash
make test
```

Expected: `unittest` reports all tests in `tests/` pass. Existing figure tests may run in addition to the new context builder tests.

- [ ] **Step 4: Commit Makefile integration**

Run:

```bash
git add Makefile docs/gpt_context.md
git commit -m "chore: add GPT context Makefile workflow"
```

Expected: one commit containing the Makefile change and refreshed generated context.

## Task 6: Commit Existing Paper Sources

**Files:**
- Track existing source files under `sections/`, `tables/`, `figures/`, `scripts/`, `tests/`, and root LaTeX template files.

- [ ] **Step 1: Review tracked candidates**

Run:

```bash
git status --short
```

Expected: source files are untracked, while ignored build artifacts such as `main.aux`, `main.log`, `main.pdf`, and `draft_for_gpt_feedback.zip` are absent from the listing.

- [ ] **Step 2: Stage paper source**

Run:

```bash
git add README.md AGENTS.md Makefile main.tex math_commands.tex references.bib iclr2026_conference.bst iclr2026_conference.sty fancyhdr.sty natbib.sty docs figures notes scripts sections tables tests
```

Expected: source files, generated figures, notes, scripts, and tests are staged.

- [ ] **Step 3: Confirm no ignored artifacts are staged**

Run:

```bash
git diff --cached --name-only
```

Expected: output includes `main.tex`, `sections/01_introduction.tex`, `figures/fig1_optimizer_geometry_pipeline.pdf`, and `docs/gpt_context.md`; output does not include `main.aux`, `main.log`, `main.pdf`, or `draft_for_gpt_feedback.zip`.

- [ ] **Step 4: Commit paper workspace**

Run:

```bash
git commit -m "chore: add current ICLR paper workspace"
```

Expected: one commit containing the current paper source workspace.

## Task 7: Push To GitHub

**Files:**
- No file edits.

- [ ] **Step 1: Inspect remote heads**

Run:

```bash
git ls-remote --heads origin
```

Expected if the GitHub repo is empty: no branch lines are printed. If GitHub created an initial README or license, output includes a line ending in `refs/heads/main`.

- [ ] **Step 2: Push main branch**

Run:

```bash
git push -u origin main
```

Expected if the remote is empty: push succeeds and sets upstream for `main`.

- [ ] **Step 3: Handle non-empty remote only if push is rejected**

If `git push -u origin main` is rejected because the remote already has commits, run:

```bash
git fetch origin main
git log --oneline --decorate --all --max-count=20
```

Expected: the log shows both local commits and the remote `origin/main` commit. If the remote only contains GitHub-created boilerplate such as `README.md`, merge it with:

```bash
git pull --rebase origin main --allow-unrelated-histories
git push -u origin main
```

Expected: the local branch rebases onto the remote boilerplate commit and push succeeds. If the remote contains meaningful paper content, stop and ask the user before merging.

## Task 8: Establish Web ChatGPT Review Routine

**Files:**
- Modify: `notes/decision_log.md`
- Modify: `docs/gpt_context.md`

- [ ] **Step 1: Add operating routine to decision log**

Append this section to `notes/decision_log.md`:

```markdown

## Operating Routine

Before asking web ChatGPT for paper review:

1. Apply local edits.
2. Run `make gpt-context`.
3. Commit the updated source and `docs/gpt_context.md`.
4. Push `main` to GitHub.
5. Ask web ChatGPT to read `README_FOR_GPT.md` and `docs/gpt_context.md` first.

After web ChatGPT gives feedback:

1. Move durable decisions into `notes/decision_log.md`.
2. Move current paper status changes into `notes/paper_state.md`.
3. Ask Codex to apply concrete file-level edits locally.
4. Rebuild, test, regenerate `docs/gpt_context.md`, commit, and push.
```

- [ ] **Step 2: Regenerate GPT context**

Run:

```bash
make gpt-context
```

Expected: `docs/gpt_context.md` includes the new operating routine from `notes/decision_log.md`.

- [ ] **Step 3: Commit operating routine**

Run:

```bash
git add notes/decision_log.md docs/gpt_context.md
git commit -m "docs: document GPT review operating routine"
```

Expected: one commit containing the routine and regenerated context bundle.

- [ ] **Step 4: Push routine update**

Run:

```bash
git push
```

Expected: GitHub `main` is updated.

## Task 9: First Web ChatGPT Prompt

**Files:**
- No file edits.

- [ ] **Step 1: Copy this prompt into web ChatGPT**

Use this exact prompt:

```text
You are reviewing my ICLR-style ML paper repository.

Repository: <PRIVATE_REPO_URL>

First read README_FOR_GPT.md and docs/gpt_context.md. Treat docs/gpt_context.md as the current review bundle, but treat the source files as authoritative if there is any mismatch.

Please do not invent experimental results, citations, datasets, baselines, or numeric values. If evidence is missing, identify the missing evidence.

I want to rebuild the paper's logical backbone. Review the current draft for:

1. central claim clarity,
2. contribution strength,
3. introduction logic,
4. method-to-experiment alignment,
5. figure/table usefulness,
6. likely reviewer objections,
7. concrete Codex handoff tasks by file path.

Return your answer in this format:

1. Core diagnosis
2. Highest-impact changes
3. Section-by-section notes
4. Figure/table recommendations
5. Concrete Codex handoff tasks
```

- [ ] **Step 2: Save durable outcomes locally**

After reviewing web ChatGPT's response, update:

```text
notes/decision_log.md
notes/paper_state.md
```

Expected: transient brainstorming remains in ChatGPT or Notion, while durable decisions are moved into the repository.

## Verification Commands

Run these commands before considering the workflow complete:

```bash
make gpt-context
make test
git status --short
git log --oneline --max-count=8
git remote -v
```

Expected:

- `make gpt-context` prints `docs/gpt_context.md`.
- `make test` passes.
- `git status --short` is empty after committing.
- `git log --oneline --max-count=8` shows the workflow commits.
- `git remote -v` points to `<PRIVATE_REPO_URL>.git`.

## Self-Review

- Spec coverage: The plan covers GitHub setup, GPT entry documents, generated review bundle, tests, Makefile integration, push routine, and first web ChatGPT prompt.
- Placeholder scan: No task relies on unspecified files or unnamed commands.
- Type consistency: The script exposes `collect_text_files`, `build_context`, and `write_context`; tests call those exact functions.
