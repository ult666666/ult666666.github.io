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


class ScriptReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.found.append(dict(attrs))


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

    def test_selected_work_and_index_inventory(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        doc = parse(ROOT / "index.html")
        selected = re.findall(r'<article class="work(?: [^"]*)?" id="([^"]+)"', html)
        self.assertEqual(selected, ["frontier-ai-valuation-lab", "lineageguard", "luma-keys", "motionx"])
        table = html.split('<table class="index-table"', 1)[1].split("</table>", 1)[0]
        rows = re.findall(r'<th scope="row"[^>]*>([^<]+)</th>', table)
        self.assertEqual(len(rows), 17)
        self.assertEqual(len(rows), len(set(rows)))
        for name in ("Frontier AI Valuation Lab", "LineageGuard Studio", "Luma Keys", "MOTIONX", "quantkit",
                     "ledgerline", "powerlift", "citecheck", "searchlite", "ContrastKit", "TraceBench",
                     "RelayBox", "Impact Ledger", "SaaS Analytics Warehouse", "Agentic Trading Research",
                     "ProofCast", "Blast Radius Daily"):
            self.assertIn(name, rows)
        for row in table.split('<th scope="row"')[1:]:
            with self.subTest(row=row[:60]):
                self.assertIn('href="https://github.com/ult666666/', row.split("</tr>", 1)[0])
        self.assertEqual(doc.controls, [], "The homepage needs no buttons or scripted controls")
        self.assertIn("primary-nav", doc.ids)

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
        self.assertIn('frontier-ai-valuation-lab/blob/main/docs/VERIFICATION.md', page)
        self.assertIn('lineageguard-datahub-agent/blob/main/docs/ENGINEERING_REVIEW.md', page)
        self.assertEqual(page.count('class="proof-path"'), 2)

    def test_selected_work_images_have_intrinsic_sizes(self):
        import json
        import struct
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        inventory = set(json.loads((ROOT / "public-files.json").read_text())["files"])
        work = html.split('<div class="selected">', 1)[1].split("</section>", 1)[0]
        images = re.findall(r'<img src="/([^"]+)" width="(\d+)" height="(\d+)" alt="([^"]+)"', work)
        self.assertEqual(len(images), 4)
        for asset, width, height, alt in images:
            with self.subTest(asset=asset):
                self.assertIn(asset, inventory)
                raw = (ROOT / asset).read_bytes()
                if raw[:8] == b"\x89PNG\r\n\x1a\n":
                    self.assertEqual(struct.unpack(">II", raw[16:24]), (int(width), int(height)))
                self.assertGreater(len(alt), 20)
        for repo in ("saas-analytics-warehouse", "impact-ledger", "contrastkit", "searchlite", "tracebench", "relaybox"):
            self.assertIn('href="https://github.com/ult666666/' + repo + '"', html)
        self.assertEqual(html.count("synthetic data"), 1, "Say it once, in the index note")

    def test_navigation_targets_exist(self):
        parsed = parse(ROOT / "index.html")
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        nav = html.split('<nav class="primary-nav"', 1)[1].split("</nav>", 1)[0]
        self.assertEqual(re.findall(r'href="([^"]+)"', nav), ["#work", "#index", "#about", "#contact"])
        for anchor in ("work", "index", "about", "contact", "frontier-ai-valuation-lab", "lineageguard",
                       "luma-keys", "motionx"):
            self.assertIn(anchor, parsed.ids)
        for page in PAGES:
            if page.name == "index.html":
                continue
            with self.subTest(page=page.name):
                text = page.read_text(encoding="utf-8")
                inner = text.split('<nav class="primary-nav"', 1)[1].split("</nav>", 1)[0]
                self.assertEqual(re.findall(r'href="([^"]+)"', inner), ["/#work", "/#index", "/#about", "/#contact"])

    def test_styles_contract_and_no_scripts(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("@media (prefers-reduced-motion:reduce)", css)
        self.assertIn(":focus-visible", css)
        self.assertIn(".skip-link", css)
        self.assertFalse((ROOT / "script.js").exists())
        for page in [*PAGES, ROOT / "404.html"]:
            with self.subTest(page=page.name):
                text = page.read_text(encoding="utf-8")
                # HTMLParser lowercases tag and attribute names, so no spelling of <script> slips past.
                scripts = ScriptReader()
                scripts.feed(text)
                executable = [attrs for attrs in scripts.found
                              if (attrs.get("type") or "").strip().lower() != "application/ld+json"]
                allowed = [{"defer": None, "src": "/project-catalog.js"}] if page.name == "catalog.html" else []
                self.assertEqual(executable, allowed, "Only the project explorer's search may use JavaScript")
                self.assertIn('class="skip-link" href="#main"', text)
                self.assertNotIn('class="menu-toggle"', text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
