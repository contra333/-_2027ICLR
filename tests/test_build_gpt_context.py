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
