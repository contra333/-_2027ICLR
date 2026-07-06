import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "make_section4_placeholder_figures.py"
PLACEHOLDER_NOTICE = "SYNTHETIC PLACEHOLDER -- DO NOT REPORT"

EXPECTED_CSVS = [
    "fig2_wd_coupling_interpolation.csv",
    "fig3_adaptive_coupling_gap.csv",
    "fig4_detector_family_delta_heatmap.csv",
    "fig5_l2_recovery_paths.csv",
    "fig6_prototype_subspace_alignment.csv",
]

EXPECTED_FIGURES = [
    "fig2_wd_coupling_interpolation.pdf",
    "fig3_adaptive_coupling_gap.pdf",
    "fig4_detector_family_delta_heatmap.pdf",
    "fig5_l2_recovery_paths.pdf",
    "fig6_prototype_subspace_alignment.pdf",
]


def load_module():
    spec = importlib.util.spec_from_file_location(
        "make_section4_placeholder_figures", SCRIPT_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SectionFourPlaceholderFigureTest(unittest.TestCase):
    def test_generator_writes_all_placeholder_csvs_and_pdfs(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outputs = module.generate_placeholder_artifacts(output_root=root)

            csv_dir = root / "results" / "processed" / "placeholders"
            figure_dir = root / "figures"

            self.assertEqual(
                {path.name for path in outputs["csv"]},
                set(EXPECTED_CSVS),
            )
            self.assertEqual(
                {path.name for path in outputs["figures"]},
                set(EXPECTED_FIGURES),
            )

            for name in EXPECTED_CSVS:
                path = csv_dir / name
                text = path.read_text(encoding="utf-8")
                self.assertTrue(text.startswith(f"# {PLACEHOLDER_NOTICE}"))
                self.assertIn("placeholder_notice", text.splitlines()[1])
                self.assertIn(PLACEHOLDER_NOTICE, text)

            for name in EXPECTED_FIGURES:
                path = figure_dir / name
                self.assertTrue(path.read_bytes().startswith(b"%PDF"))
                self.assertGreater(path.stat().st_size, 5_000)

    def test_script_uses_matplotlib_without_dataframe_plotting_dependencies(self):
        script_text = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("import matplotlib", script_text)
        self.assertNotIn("import pandas", script_text)
        self.assertNotIn("import numpy", script_text)
        self.assertNotIn("import seaborn", script_text)


if __name__ == "__main__":
    unittest.main()
