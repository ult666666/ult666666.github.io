"""Portfolio integrity and accessibility smoke tests, no network or dependencies."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "index.html", ROOT / "fintech.html", *(ROOT / "projects").glob("*.html")]
CASE_NAMES = {"lineageguard.html", "motionx.html", "trading-research.html", "frontier-ai-valuation-lab.html", "engineering-lab.html", "foundations.html"}
CATEGORIES = {"ai", "web", "experimental", "fintech"}


class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.local_refs = []
        self.images = []
        self.headings = []
        self.external_links = []
        self.project_categories = []
        self.controls = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            link = a["href"]
            if link.startswith(("http://", "https://")):
                self.external_links.append(a)
            elif link.startswith("mailto:") or link.startswith("#"):
                pass
            elif not link.startswith(("javascript:", "data:")):
                self.local_refs.append(link)
        if tag in ("script", "link", "img") and "src" in a:
            self.local_refs.append(a["src"])
        if tag == "link" and "href" in a and a.get("rel") in ("stylesheet", "icon"):
            self.local_refs.append(a["href"])
        if tag == "img":
            self.images.append(a)
        if tag == "article" and "data-category" in a:
            self.project_categories.append(a["data-category"])
        if tag == "button":
            self.controls.append(a)
        if tag in ("h1", "h2", "h3"):
            self.headings.append(tag)


def parse(path: Path) -> Reader:
    x = Reader()
    x.feed(path.read_text(encoding="utf-8"))
    return x


class PortfolioTests(unittest.TestCase):
    def test_pages_and_case_count(self):
        self.assertEqual({p.name for p in (ROOT / "projects").glob("*.html")}, CASE_NAMES | {"catalog.html"})
        for page in PAGES:
            with self.subTest(page=page.name):
                self.assertTrue(page.stat().st_size > 1000)
                content = page.read_text(encoding="utf-8")
                self.assertIn('<meta name="viewport"', content)
                self.assertIn("Charles Dai", content)

    def test_internal_links_resolve(self):
        for page in PAGES:
            doc = parse(page)
            for raw in doc.local_refs:
                with self.subTest(page=page.name, href=raw):
                    clean = raw.split("#")[0].split("?")[0]
                    if not clean:
                        continue
                    if raw.startswith("/"):
                        candidate = ROOT / clean.lstrip("/")
                    else:
                        candidate = page.parent / clean
                    if candidate.is_dir():
                        candidate = candidate / "index.html"
                    self.assertTrue(candidate.exists(), f"broken local link {page.name}: {raw}")

    def test_every_image_has_alt_text(self):
        for page in PAGES:
            for img in parse(page).images:
                self.assertIn("alt", img)
                self.assertTrue(img["alt"].strip())

    def test_external_links_are_https_and_safe(self):
        for page in PAGES:
            for attrs in parse(page).external_links:
                href = attrs["href"]
                self.assertEqual(urlparse(href).scheme, "https")
                if attrs.get("target") == "_blank":
                    self.assertIn("noopener", attrs.get("rel", ""))
                    self.assertIn("noreferrer", attrs.get("rel", ""))

    def test_project_inventory_and_filters(self):
        doc = parse(ROOT / "index.html")
        self.assertEqual(len(doc.project_categories), 9)
        self.assertTrue(set(doc.project_categories) <= CATEGORIES)
        buttons = {a.get("data-filter"): a for a in doc.controls if "data-filter" in a}
        self.assertEqual(set(buttons), {"all", "fintech", "ai", "web", "experimental"})
        self.assertEqual(buttons["all"]["aria-pressed"], "true")
        self.assertIn("primary-nav", doc.ids)
        self.assertIn("project-count", doc.ids)

    def test_case_studies_are_generated_deterministically(self):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts" / "build_cases.py"),
                                 "--check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_case_pages_have_navigation_and_source(self):
        for name in CASE_NAMES:
            page = ROOT / "projects" / name
            with self.subTest(page=page.name):
                doc = parse(page)
                for sid in ("main", "section-1", "section-2", "section-3", "section-4"):
                    self.assertIn(sid, doc.ids)
                content = page.read_text()
                self.assertIn("https://github.com/ult666666/", content)
                self.assertIn("Back to all projects", content)

    def test_no_private_system_leakage_or_unsupported_stats(self):
        corpus = "\n".join(p.read_text(encoding="utf-8") for p in PAGES)
        for forbidden in ("/Users/prince/", "sk-proj-", "ghp_", "Bearer ",
                          "ACCOUNT_NUMBER", "guaranteed returns", "100% accuracy"):
            self.assertNotIn(forbidden, corpus)
        self.assertNotIn("live order execution", corpus.lower())

    def test_homepage_links_to_inspectable_engineering_evidence(self):
        page = (ROOT / 'index.html').read_text()
        self.assertIn('id="engineering-proof"', page)
        self.assertIn('docs/PUBLICATION_BOUNDARY.md', page)
        self.assertIn('frontier-ai-valuation-lab/blob/main/docs/VERIFICATION.md', page)
        self.assertIn('lineageguard-datahub-agent/blob/main/docs/ENGINEERING_REVIEW.md', page)
        self.assertEqual(page.count('class="proof-path"'), 3)

    def test_recent_projects_have_direct_code_and_demo_links(self):
        page = (ROOT / "index.html").read_text()
        self.assertEqual(page.count('id="recent-builds"'), 1)
        panel = page.split('<section class="recent-builds"', 1)[1].split('</section>', 1)[0]
        self.assertEqual(panel.count('class="recent-card"'), 6)
        for repo in ("saas-analytics-warehouse", "impact-ledger", "contrastkit",
                     "searchlite", "tracebench", "relaybox"):
            self.assertIn("https://github.com/ult666666/" + repo, panel)
        self.assertIn("synthetic", panel.lower())
        self.assertNotIn("data-category=", panel)

    def test_recent_visuals_have_pinned_public_provenance(self):
        import hashlib
        import json
        manifest = json.loads((ROOT / "docs/RECENT_VISUALS.json").read_text())
        self.assertEqual(manifest["schema"], "portfolio_visual_provenance/1")
        records = manifest["assets"]
        self.assertEqual(len(records), 4)
        inventory = set(json.loads((ROOT / "public-files.json").read_text())["files"])
        html = (ROOT / "index.html").read_text()
        for record in records:
            self.assertRegex(record["source_commit"], r"^[0-9a-f]{40}$")
            self.assertIn(record["asset"], inventory)
            path = ROOT / record["asset"]
            raw = path.read_bytes()
            self.assertEqual(raw[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(hashlib.sha256(raw).hexdigest(), record["sha256"])
            self.assertIn('src="/' + record["asset"] + '"', html)
            self.assertIn('id="' + record["anchor"] + '"', html)
            self.assertIn(record["alt"], html)

    def test_recruiter_routes_resolve_to_real_project_ids(self):
        html = (ROOT / "index.html").read_text()
        parsed = parse(ROOT / "index.html")
        self.assertIn('aria-label="Explore projects by specialty"', html)
        for anchor in ("frontier-ai-valuation-lab", "lineageguard",
                       "saas-analytics-warehouse", "contrastkit"):
            self.assertIn(anchor, parsed.ids)
            self.assertIn('href="#' + anchor + '"', html)
        self.assertEqual(html.count('class="recent-media'), 6)

    def test_css_and_js_exist_and_match_basic_contract(self):
        css = (ROOT / "styles.css").read_text()
        js = (ROOT / "script.js").read_text()
        self.assertIn("@media (prefers-reduced-motion:reduce)", css)
        self.assertIn(":focus-visible", css)
        self.assertIn(".project-card[hidden]", css)
        self.assertIn("aria-pressed", js)
        self.assertIn("aria-expanded", js)


if __name__ == "__main__":
    unittest.main(verbosity=2)
