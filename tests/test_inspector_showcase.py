"""Keep the public Inspector showcase tied to shipped implementation and its limits."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://github.com/ult666666/lineageguard-datahub-agent/blob/6ed607b5c9ff6f46f2bb3214b04d040b04c02c52/'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.words = []
    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))
    def handle_data(self, data):
        self.words.append(data)

class InspectorShowcaseTests(unittest.TestCase):
    def setUp(self):
        self.raw = (ROOT / 'projects/lineageguard.html').read_text()
        self.page = Page()
        self.page.feed(self.raw)
        self.text = ' '.join(self.page.words)
        self.hrefs = [attrs.get('href') for tag, attrs in self.page.elements if tag == 'a']

    def test_inspector_and_demonstration_have_accessible_stable_destinations(self):
        ids = [attrs.get('id') for _, attrs in self.page.elements if attrs.get('id')]
        for target in ('review-inspector', 'try-workflow', 'section-1', 'section-2', 'section-3', 'section-4'):
            self.assertIn(target, ids)
            self.assertIn('#' + target, self.hrefs)
        self.assertEqual(len(ids), len(set(ids)))
        for text in ('Review Inspector', 'Evidence-source outage', 'Restore synthetic source', 'Inspect current review'):
            self.assertIn(text, self.text)

    def test_inspection_claims_explain_local_processing_and_authenticity_limit(self):
        for phrase in ('without uploading', 'not authentication', 'same policy functions', 'recorded decision', 'inspection time', 'No SQL execution'):
            self.assertIn(phrase, self.text)
        for relative in ('docs/REVIEW_INSPECTOR.md', 'public/studio/core/inspection.js', 'test/studio/inspection.test.mjs', 'scripts/inspection-browser.cjs'):
            self.assertIn(SOURCE + relative, self.hrefs)
        self.assertNotIn('enterprise-certified', self.text.lower())

    def test_test_counts_are_identified_as_the_inspector_revision_not_the_original_release(self):
        for phrase in ('20 October 2026', '120 Node tests', '31 browser journeys', '19 evaluation assertions', 'not independent evidence of catalog truth'):
            self.assertIn(phrase, self.text)
        self.assertIn('v2.0.0', self.text)
        self.assertNotIn('separates the 84-test Node suite, 24 browser journeys', self.text)

    def test_screenshot_is_exact_public_source_with_size_and_publication_inventory(self):
        name = 'assets/lineageguard-review-inspector.png'
        self.assertTrue((ROOT / name).is_file(), 'public Inspector screenshot must exist')
        data = (ROOT / name).read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), '53afbb9e409fc1e94e3fdf024c4ed90ba0bc9a14695a5422893c110c12efc266')
        image = next((attrs for tag, attrs in self.page.elements if tag == 'img' and attrs.get('src') == '/' + name), None)
        self.assertIsNotNone(image, 'case study must display the source screenshot')
        self.assertEqual((int(image['width']), int(image['height'])), struct.unpack('>II', data[16:24]))
        self.assertIn('not authenticated', image['alt'].lower())
        inventory = json.loads((ROOT / 'public-files.json').read_text())['files']
        self.assertIn(name, inventory)
        self.assertIn('styles.css', inventory)
        self.assertIn('/styles.css', [attrs.get('href') for tag, attrs in self.page.elements if tag == 'link'])
        self.assertIn(('body', {'class': 'case-lineageguard'}), self.page.elements)
        self.assertIn('.case-lineageguard .case-detail-media', (ROOT / 'styles.css').read_text())

if __name__ == '__main__':
    unittest.main()
