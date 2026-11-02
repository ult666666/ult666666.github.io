"""Keep the public Inspector showcase tied to shipped implementation and its limits."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://github.com/ult666666/lineageguard-datahub-agent/blob/ed48eea4370d28c52f3268fadcd3b82a3632a691/'

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
        for target in ('review-inspector', 'saved-comparison', 'try-workflow', 'section-1', 'section-2', 'section-3', 'section-4'):
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

    def test_benchmark_figures_are_current_and_test_counts_stay_in_the_repository(self):
        # The benchmark result on main (105 cases, 101 matching, none more permissive) is the page's figure.
        for phrase in ('105 labelled cases', '101 decisions match', 'five decisions more permissive than their labels',
                       'no decision is more permissive than its label', 'which is not authentication or approval'):
            self.assertIn(phrase, self.text)
        # Suite sizes go stale; the repository's verification record carries them, not this page.
        self.assertIsNone(re.search(r'\d+ (Node tests|browser journey|evaluation assertions)', self.text))
        self.assertNotIn('separates the 84-test Node suite, 24 browser journeys', self.text)
        self.assertIn('https://github.com/ult666666/lineageguard-datahub-agent/blob/main/docs/VERIFICATION.md', self.hrefs)

    def test_dbt_manifest_section_states_what_a_manifest_cannot_clear(self):
        ids = [attrs.get('id') for _, attrs in self.page.elements if attrs.get('id')]
        self.assertIn('dbt-manifest', ids)
        self.assertIn('#dbt-manifest', self.hrefs)
        for phrase in ('needs-evidence', 'five downstream models and two exposures', '12 dbt tests',
                       'never clear one', 'manifest schema v12 and catalog v1', 'synthetic'):
            self.assertIn(phrase, self.text)
        self.assertIn('https://github.com/ult666666/lineageguard-datahub-agent/blob/main/test/studio/dbt-properties.test.mjs', self.hrefs)

    def test_screenshot_is_exact_public_source_with_size_and_publication_inventory(self):
        inventory = json.loads((ROOT / 'public-files.json').read_text())['files']
        for name, expected in (
            ('assets/lineageguard-review-inspector.png', '9052d0781488221a976d6df4e3d189e2e4dd716066bc278d5032c8d15e902e39'),
            ('assets/lineageguard-saved-comparison.png', '5b40ae5ebcb25fbc0f69dcca03dcf05506530ed1ad13141b1e63bff930d92b61'),
        ):
            with self.subTest(screenshot=name):
                self.assertTrue((ROOT / name).is_file(), 'public source screenshot must exist')
                data = (ROOT / name).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), expected)
                image = next((attrs for tag, attrs in self.page.elements if tag == 'img' and attrs.get('src') == '/' + name), None)
                self.assertIsNotNone(image, 'case study must display the source screenshot')
                self.assertEqual((int(image['width']), int(image['height'])), struct.unpack('>II', data[16:24]))
                self.assertIn('not authenticated', image['alt'].lower())
                self.assertIn(name, inventory)
        self.assertIn('styles.css', inventory)
        self.assertIn('/styles.css', [attrs.get('href') for tag, attrs in self.page.elements if tag == 'link'])
        self.assertIn(('body', {'class': 'case-lineageguard'}), self.page.elements)
        self.assertIn('.case-lineageguard .case-detail-media', (ROOT / 'styles.css').read_text())

if __name__ == '__main__':
    unittest.main()
