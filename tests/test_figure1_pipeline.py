import importlib.util
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "make_figure1_pipeline.py"


def load_module():
    spec = importlib.util.spec_from_file_location("make_figure1_pipeline", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FigureOnePipelineTest(unittest.TestCase):
    def test_pipeline_spec_has_four_ordered_stages(self):
        module = load_module()
        stages = module.get_pipeline_spec()

        self.assertEqual(
            [stage["title"] for stage in stages],
            [
                "Optimizer choice",
                "Penultimate geometry",
                "Detector readout",
                "Reliability behavior",
            ],
        )
        self.assertEqual(len(stages), 4)
        self.assertTrue(all(stage["items"] for stage in stages))
        self.assertFalse(any("label" in stage for stage in stages))

    def test_stage_text_is_short_enough_for_svg_to_pdf_conversion(self):
        module = load_module()
        stages = module.get_pipeline_spec()

        all_visible_lines = []
        for stage in stages:
            all_visible_lines.extend(str(stage["title"]).split())
            all_visible_lines.extend(str(stage["subtitle"]).split())
            all_visible_lines.extend(str(item) for item in stage["items"])

        self.assertLessEqual(max(len(line) for line in all_visible_lines), 16)
        self.assertNotIn("Gaussian density", all_visible_lines)

    def test_figure_uses_iclr_like_serif_font(self):
        module = load_module()

        self.assertEqual(module.FIGURE_FONT, "Nimbus Roman")

    def test_build_figure_writes_vector_outputs(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            pdf_path = out_dir / "figure1.pdf"
            svg_path = out_dir / "figure1.svg"

            module.build_figure(pdf_path=pdf_path, svg_path=svg_path)

            self.assertGreater(pdf_path.stat().st_size, 10_000)
            self.assertGreater(svg_path.stat().st_size, 10_000)
            self.assertTrue(pdf_path.read_bytes().startswith(b"%PDF"))
            svg_text = svg_path.read_text(encoding="utf-8")
            self.assertIn("<svg", svg_text)
            self.assertIn("Optimizer", svg_text)
            self.assertIn("choice", svg_text)
            self.assertIn("Detector", svg_text)
            self.assertIn("readout", svg_text)

    def test_generated_svg_follows_publication_figure_text_rules(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmp:
            svg_path = Path(tmp) / "figure1.svg"
            module.build_figure(pdf_path=Path(tmp) / "figure1.pdf", svg_path=svg_path)
            svg_text = svg_path.read_text(encoding="utf-8")

            self.assertNotIn("Optimizer-conditioned geometry compatibility", svg_text)
            self.assertIn("Nimbus Roman", svg_text)
            font_sizes = [
                float(size)
                for size in re.findall(r"font-size: ([0-9.]+)px", svg_text)
            ]
            self.assertTrue(font_sizes)
            self.assertGreaterEqual(min(font_sizes), 7.0)
            self.assertLessEqual(max(font_sizes), 8.6)
            self.assertNotIn("opacity: 0.9", svg_text)

    def test_figure_matches_iclr_insert_width_without_tight_bbox_scaling(self):
        module = load_module()
        script_text = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertAlmostEqual(module.FIGURE_SIZE[0], 5.39, places=2)
        self.assertNotIn("bbox_inches=\"tight\"", script_text)

    def test_pdf_is_converted_from_svg_artifact(self):
        script_text = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("from cairosvg import svg2pdf", script_text)
        self.assertIn("svg2pdf(url=str(svg_path), write_to=str(pdf_path))", script_text)
        self.assertNotIn("fig.savefig(pdf_path", script_text)

    def test_script_avoids_template_like_rounded_boxes(self):
        script_text = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertNotIn("FancyBboxPatch", script_text)
        self.assertNotIn("boxstyle=", script_text)
        self.assertNotIn("pill", script_text.lower())
        self.assertNotIn("\"accent\"", script_text)
        self.assertNotIn("\"label\"", script_text)


if __name__ == "__main__":
    unittest.main()
