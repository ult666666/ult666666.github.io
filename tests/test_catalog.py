"""Exercise generation boundaries and stale-artifact detection on real files."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/build_catalog.py'


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.exists(), 'Project catalog generator has not been implemented')
        spec = importlib.util.spec_from_file_location('build_catalog', SCRIPT)
        self.catalog = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.catalog)
        self.fixture = {'version': 1, 'projects': [{
            'id': 'example', 'name': 'Example', 'areas': ['backend'], 'form': 'library',
            'stack': ['Python', 'SQLite'], 'summary': 'A local queue.',
            'scenario': 'Receive the same event twice.', 'inspect': 'Inspect deduplication tests.',
            'limits': 'Local demonstration.', 'command': 'python3 demo.py',
            'links': [{'label': 'Source', 'url': 'https://github.com/ult666666/relaybox'}],
        }]}

    def test_escapes_text_in_content_and_attributes(self):
        item = self.fixture['projects'][0]
        item['name'] = '<script>alert("x")</script>'
        item['scenario'] = 'A & B < C'
        rendered = self.catalog.render(self.fixture)
        self.assertIn('&lt;script&gt;', rendered)
        self.assertIn('A &amp; B &lt; C', rendered)
        self.assertNotIn('<script>alert', rendered)

    def test_rejects_duplicate_and_unsafe_project_ids(self):
        for value in ['example', '../private', 'x" onclick="alert(1)']:
            other = copy.deepcopy(self.fixture['projects'][0])
            other['id'] = value
            broken = copy.deepcopy(self.fixture)
            broken['projects'].append(other)
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.catalog.render(broken)

    def test_rejects_unsafe_or_unreviewed_links(self):
        for url in ['javascript:alert(1)', '//example.com', 'https://github.com@evil.test/',
                    'https://github.com:8443/', '/projects/../secret', 'https://evil.test/']:
            broken = copy.deepcopy(self.fixture)
            broken['projects'][0]['links'][0]['url'] = url
            with self.subTest(url=url), self.assertRaises(ValueError):
                self.catalog.render(broken)

    def test_rejects_missing_review_information_and_unknown_area(self):
        for key, value in [('scenario', ''), ('inspect', ''), ('limits', ''), ('areas', ['unknown'])]:
            broken = copy.deepcopy(self.fixture)
            broken['projects'][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.catalog.render(broken)

    def test_content_exists_without_javascript(self):
        rendered = self.catalog.render(self.fixture)
        for expected in ['Receive the same event twice.', 'Inspect deduplication tests.',
                         'Local demonstration.', 'https://github.com/ult666666/relaybox']:
            self.assertIn(expected, rendered)
        self.assertNotIn('class="catalog-card" hidden', rendered)

    def test_review_command_is_rendered_as_selectable_escaped_text(self):
        self.fixture['projects'][0]['command'] = 'python3 demo.py --value "<fixture>"'
        self.assertIn('python3 demo.py --value &quot;&lt;fixture&gt;&quot;', self.catalog.render(self.fixture))

    def test_cli_detects_stale_page_without_overwriting_it(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / 'data.json', Path(directory) / 'catalog.html'
            source.write_text(json.dumps(self.fixture))
            command = [sys.executable, '-B', str(SCRIPT), '--catalog', str(source), '--output', str(output)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(subprocess.run(command + ['--check'], capture_output=True).returncode, 0)
            output.write_text('stale page')
            self.assertNotEqual(subprocess.run(command + ['--check'], capture_output=True).returncode, 0)
            self.assertEqual(output.read_text(), 'stale page')

    def test_reviewed_page_is_current(self):
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--check'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
