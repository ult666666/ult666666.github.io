"""The optional review guide must display authored text without interpreting HTML."""
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

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


class CaseReviewTests(unittest.TestCase):
    def test_review_text_and_link_labels_cannot_inject_elements_or_attributes(self):
        # Removing escaping from the new renderer would turn this visible text
        # into an image, a script, or a second link attribute.
        unsafe = '<img src=x onerror="alert(1)">'
        label = 'Read "the model" <script>alert(2)</script>'
        case = dict(builder.CASES[0], image=None, section_media={})
        case["review"] = {
            "intro": unsafe,
            "steps": [(unsafe, "Inspect the result.", label, "https://example.org/source?a=1&b=2")],
            "evidence": [
                (unsafe, "Shared calculation.", [(label, "https://example.org/model")],
                 unsafe, [(label, "https://example.org/checks")])
            ],
        }
        reader = ReviewReader()
        reader.feed(builder.render(case))
        rendered_text = "".join(reader.text)
        self.assertIn(unsafe, rendered_text)
        self.assertIn(label, rendered_text)
        self.assertFalse(any(tag == "img" for tag, _ in reader.elements))
        self.assertFalse(any("onerror" in attrs for _, attrs in reader.elements))
        scripts = [attrs for tag, attrs in reader.elements if tag == "script"]
        self.assertEqual(scripts, [{"defer": None, "src": "/script.js"}])
        links = [attrs["href"] for tag, attrs in reader.elements if tag == "a"]
        self.assertIn("https://example.org/source?a=1&b=2", links)


if __name__ == "__main__":
    unittest.main(verbosity=2)
