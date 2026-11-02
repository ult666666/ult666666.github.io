"""Review guides keep authored text inert and expose honest, safe demo entry points."""
from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("case_builder", ROOT / "scripts" / "build_cases.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ReviewReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.elements = []
        self.links = []
        self.active_link = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.elements.append((tag, attributes))
        if tag == "a":
            self.active_link = {"attributes": attributes, "text": []}
            self.links.append(self.active_link)

    def handle_endtag(self, tag):
        if tag == "a":
            self.active_link = None

    def handle_data(self, data):
        self.text.append(data)
        if self.active_link is not None:
            self.active_link["text"].append(data)


class CaseReviewTests(unittest.TestCase):
    def test_objective_preview_entry_points_preserve_the_primary_studio_route(self):
        preview_url = "https://frontier-ai-valuation-lab.vercel.app/capital.html#capital-explore"
        studio_url = "https://frontier-ai-valuation-lab.vercel.app/capital.html#worked-decision"
        for path in (ROOT / "fintech.html", ROOT / "projects/frontier-ai-valuation-lab.html"):
            with self.subTest(page=path.name):
                reader = ReviewReader()
                reader.feed(path.read_text(encoding="utf-8"))
                previews = [link for link in reader.links if link["attributes"].get("href") == preview_url]
                self.assertEqual(len(previews), 1)
                self.assertIn("Preview", "".join(previews[0]["text"]))
                self.assertEqual(previews[0]["attributes"].get("target"), "_blank")
                self.assertTrue({"noopener", "noreferrer"} <= set(previews[0]["attributes"].get("rel", "").split()))
                primary = [link for link in reader.links
                           if "button-primary" in link["attributes"].get("class", "").split()
                           and "Try Capital Strategy Studio" in "".join(link["text"])]
                self.assertEqual(len(primary), 1)
                self.assertEqual(" ".join("".join(primary[0]["text"]).split()), "Try Capital Strategy Studio")
                self.assertEqual(primary[0]["attributes"]["href"], studio_url)

    def test_objective_guide_separates_current_plan_preview_from_explicit_apply(self):
        case = next(case for case in builder.CASES if case["slug"] == "frontier-ai-valuation-lab")
        guide = next(section for section in case["sections"] if section["id"] == "review-guide")
        reader = ReviewReader()
        reader.feed(builder.render_section(guide))
        text = " ".join("".join(reader.text).split())
        claims = ("against your current plans", "worked three-plan example",
                  "a $25bn goal and an 88% floor, Plans A and B are eligible",
                  "a 90% floor: only A remains", "Preview $30bn with 90%: no plan qualifies.",
                  "Return the floor to 88% and B qualifies.",
                  "Previewing does not change your draft.",
                  "Apply to change only the capital objective and retention floor",
                  "Plan terms and decision notes stay intact.",
                  "explicitly apply $25bn and 88% again")
        for claim in claims:
            with self.subTest(claim=claim):
                self.assertTrue(claim in text, f"Missing preview/apply guidance: {claim}")
        # Previewing comes before applying, and re-applying the worked objectives comes last.
        positions = [text.index(claim) for claim in ("Previewing does not change your draft.",
                                                     "Apply to change only the capital objective and retention floor",
                                                     "explicitly apply $25bn and 88% again")]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual([tag for tag, _ in reader.elements].count("ol"), 1, "The steps are an ordered list")

    def test_case_text_and_link_labels_cannot_inject_elements_or_attributes(self):
        # Removing escaping from the renderer would turn this visible text
        # into an image, a script, or a second link attribute.
        unsafe = '<img src=x onerror="alert(1)">'
        label = 'Read "the model" <script>alert(2)</script>'
        section = {"id": "section-1", "heading": unsafe, "body": [unsafe, [unsafe, (label, "https://example.org/source?a=1&b=2")]],
                   "items": [unsafe, [(label, "https://example.org/model"), unsafe]], "ordered": True,
                   "after": [unsafe], "links": [(label, "https://example.org/checks")]}
        case = dict(builder.CASES[0], image=None, hero=unsafe, sections=[section],
                    docs=[[(label, "https://example.org/docs"), unsafe]])
        reader = ReviewReader()
        reader.feed(builder.render(case))
        rendered_text = "".join(reader.text)
        self.assertIn(unsafe, rendered_text)
        self.assertIn(label, rendered_text)
        self.assertFalse(any(tag == "img" for tag, _ in reader.elements))
        self.assertFalse(any("onerror" in attrs for _, attrs in reader.elements))
        scripts = [attrs for tag, attrs in reader.elements if tag == "script"]
        self.assertEqual(scripts, [], "Case studies are plain HTML and CSS")
        links = [attrs["href"] for tag, attrs in reader.elements if tag == "a"]
        self.assertIn("https://example.org/source?a=1&b=2", links)
        for href in ("https://example.org/model", "https://example.org/checks", "https://example.org/docs"):
            self.assertIn(href, links)

    def test_case_studies_end_with_a_plain_list_of_code_and_docs(self):
        for case in builder.CASES:
            with self.subTest(case=case["slug"]):
                reader = ReviewReader()
                reader.feed((ROOT / "projects" / (case["slug"] + ".html")).read_text(encoding="utf-8"))
                ident = case.get("docs_id", "code-and-docs")
                self.assertIn(("section", {"id": ident, "class": "case-docs"}), reader.elements)
                text = "".join(reader.text)
                for retired in ("Read the source too", "A guide for reviewers", "Implementation and verification map"):
                    self.assertNotIn(retired, text)
                self.assertFalse(any("case-proof" in attrs.get("class", "") for _, attrs in reader.elements))
                limits = [section for section in case["sections"] if section["heading"] == "Limits"]
                self.assertEqual(len(limits), 1, "One limits section per case study")

if __name__ == "__main__":
    unittest.main(verbosity=2)
