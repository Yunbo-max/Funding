"""Static README and SVG safety tests (no network or personal files)."""
from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SVG_NAMES = ("hero.svg", "workflow.svg", "yearly-roadmap.svg", "proposal-strategies.svg")


class ReadmeAssetsTests(unittest.TestCase):
    def test_all_svg_assets_parse_as_xml(self):
        for name in SVG_NAMES:
            with self.subTest(name=name):
                file = ROOT / "assets" / name
                self.assertTrue(file.exists(), f"Missing SVG: {file}")
                root = ET.parse(file).getroot()
                self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
                self.assertTrue(root.attrib.get("viewBox"))

    def test_readme_shows_all_graphics(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        for name in SVG_NAMES:
            with self.subTest(name=name):
                self.assertIn("assets/" + name, content)
        self.assertIn("12-month funding roadmap", content)
        self.assertIn("Writing for different funding schemes", content)

    def test_readme_relative_links_exist(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        paths = set(re.findall(r"\]\(((?!https?://|mailto:|#)[^)#]+)", content))
        paths.update(re.findall(r'\bsrc="([^"]+)"', content))
        missing = [p for p in sorted(paths) if not (ROOT / p).exists()]
        self.assertEqual(missing, [], f"Broken relative README references: {missing}")

    def test_comparison_is_transparent(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("PaperBreak", content)
        self.assertIn("GrantWell", content)
        self.assertIn("grant-finder", content)
        self.assertIn("UKRI's recent RSS feed", content)
        self.assertIn("We do not claim to be the first", content)

    def test_no_github_actions_workflows(self):
        workflows = ROOT / ".github" / "workflows"
        self.assertFalse(workflows.exists(), "Funding must not add GitHub Actions workflow files")


if __name__ == "__main__":
    unittest.main()
