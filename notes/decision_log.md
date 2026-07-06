# Decision Log

## 2026-07-06

- Adopt a private GitHub repository as the canonical versioned workspace for the paper.
- Avoid repeated zip uploads as the normal web ChatGPT workflow.
- Add `README_FOR_GPT.md` as the stable entry point for web ChatGPT.
- Add generated `docs/gpt_context.md` so web ChatGPT can review the paper from one curated text bundle.
- Keep Notion as the brainstorming and free-form thinking space, but move durable decisions into repository notes.
- Treat local Ubuntu/Codex as the execution environment for LaTeX edits, figure scripts, tables, tests, and compilation.

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
