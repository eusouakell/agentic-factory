import unittest

from quality.visual_evidence import validate_visual_manifest


def capture(section="hero", viewport=1440):
    return {
        "viewport_width": viewport,
        "viewport_height": 1000,
        "section_id": section,
        "dom_anchor": "top" if section == "hero" else section,
        "artifact_ref": f"artifact://{viewport}/{section}",
        "content_sha256": ("a" if section == "hero" else "b") * 64,
        "observed_heading": "Heading",
        "reviewer_id": "browser-probe",
        "review_run_id": f"probe-{viewport}-{section}",
        "status": "pass",
        "document_metrics": {"scroll_width": viewport, "client_width": viewport},
        "section_box": {"left": 0, "right": viewport, "width": viewport, "height": 900},
        "typography": {"heading_tag": "h1", "heading_font_px": 72, "body_font_px": 18},
        "images": [
            {
                "src": "hero.webp",
                "natural_width": 1200,
                "natural_height": 800,
                "rendered_width": 600,
                "rendered_height": 400,
                "object_fit": "cover",
            }
        ],
    }


def manifest():
    return {
        "candidate_ref": "https://example.test/case/",
        "require_geometry": True,
        "required_viewports": [1440],
        "required_sections": ["hero"],
        "section_anchors": {"hero": "top"},
        "constraints": {
            "horizontal_overflow_tolerance_px": 2,
            "max_image_aspect_ratio_delta": 0.04,
            "min_heading_body_ratio": 1.4,
            "max_heading_body_ratio": 7.5,
        },
        "captures": [capture()],
    }


class VisualGeometryAcceptanceTests(unittest.TestCase):
    def test_geometry_manifest_passes(self):
        result = validate_visual_manifest(manifest())
        self.assertTrue(result.passed, result.issues)

    def test_horizontal_overflow_is_blocker(self):
        data = manifest()
        data["captures"][0]["document_metrics"]["scroll_width"] = 1500
        result = validate_visual_manifest(data)
        self.assertFalse(result.passed)
        self.assertIn("visual_manifest:1440:hero:horizontal_overflow", result.issues)

    def test_image_aspect_distortion_is_blocker(self):
        data = manifest()
        data["captures"][0]["images"][0]["rendered_height"] = 700
        result = validate_visual_manifest(data)
        self.assertFalse(result.passed)
        self.assertIn("visual_manifest:1440:hero:image_0:aspect_ratio_distorted", result.issues)

    def test_extreme_heading_hierarchy_is_blocker(self):
        data = manifest()
        data["captures"][0]["typography"]["heading_font_px"] = 160
        result = validate_visual_manifest(data)
        self.assertFalse(result.passed)
        self.assertIn("visual_manifest:1440:hero:heading_hierarchy_too_extreme", result.issues)

    def test_section_specific_image_dominance_limit(self):
        data = manifest()
        data["section_constraints"] = {"hero": {"max_image_width_ratio": 0.3}}
        result = validate_visual_manifest(data)
        self.assertFalse(result.passed)
        self.assertIn("visual_manifest:1440:hero:image_0:width_dominance_exceeded", result.issues)


if __name__ == "__main__":
    unittest.main()
