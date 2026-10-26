"""Pin the separately generated executable artifact without loosening page policy."""
from pathlib import Path
import base64
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('blast_site_guard', ROOT / 'scripts/build_site.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class Resources(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.scripts, self.styles, self.meta = [], [], {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script': self.scripts.append(attrs)
        if tag == 'link' and attrs.get('rel') == 'stylesheet': self.styles.append(attrs['href'])
        if tag == 'meta': self.meta[attrs.get('name') or attrs.get('http-equiv')] = attrs.get('content')


class BlastDemoTests(unittest.TestCase):
    def test_source_identity_and_changed_bytes_are_rejected(self):
        raw = b'<meta name="blast-source-commit" content="' + b'a' * 40 + b'" />'
        lock = {'schema': 'blast-offline-demo/1',
                'repository': 'https://github.com/ult666666/blast-radius-daily',
                'sourceCommit': 'a' * 40, 'sourceDirty': False,
                'artifact': 'projects/blast-radius-demo.html',
                'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
        guard.validate_blast_demo(raw, lock)
        for changed in (raw + b'changed', raw[:-1]):
            with self.subTest(changed=changed[-8:]), self.assertRaises(ValueError):
                guard.validate_blast_demo(changed, lock)
        for field, value in [('sourceCommit', 'b' * 40), ('sourceCommit', 'unversioned'),
                             ('sourceDirty', True), ('bytes', True),
                             ('repository', 'https://example.com/other'), ('sha256', '0' * 64)]:
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                guard.validate_blast_demo(raw, {**lock, field: value})

    def test_vendored_build_has_exact_source_and_embedded_runtime(self):
        lock = json.loads((ROOT / 'docs/blast-demo-lock.json').read_text())
        raw = (ROOT / 'projects/blast-radius-demo.html').read_bytes()
        guard.validate_blast_demo(raw, lock)
        html = raw.decode('utf-8')
        doc = Resources(); doc.feed(html)
        self.assertEqual(doc.meta['blast-source-commit'], lock['sourceCommit'])
        self.assertIn("connect-src 'none'", doc.meta['Content-Security-Policy'])
        self.assertIn("script-src data:", doc.meta['Content-Security-Policy'])
        self.assertEqual(len(doc.scripts), 1)
        self.assertEqual(len(doc.styles), 1)
        self.assertEqual(set(doc.scripts[0]), {'defer', 'src'})
        self.assertTrue(doc.scripts[0]['src'].startswith('data:text/javascript;base64,'))
        runtime = base64.b64decode(doc.scripts[0]['src'].split(',', 1)[1], validate=True).decode()
        self.assertNotIn('_rvfcpolyfillmap', runtime)
        self.assertNotIn('/api/share', runtime)
        self.assertTrue(doc.styles[0].startswith('data:text/css;base64,'))
        self.assertGreater(len(base64.b64decode(doc.styles[0].split(',', 1)[1], validate=True)), 1000)
        for text in ('ISC License', 'Mapbox', 'Vladimir Agafonkin', 'Arnout Kazemier',
                     'Liam Brummitt', 'Angry Bytes', 'Matt DesLauriers',
                     'Synthetic', 'Incident day (UTC)', 'Source and bundled licenses'):
            self.assertIn(text.lower(), html.lower())
        catalog = json.loads((ROOT / 'docs/project-catalog.json').read_text())
        blast = next(p for p in catalog['projects'] if p['id'] == 'blast-radius-daily')
        self.assertIn('/projects/blast-radius-demo.html', [link['url'] for link in blast['links']])
        self.assertIn('npm run build:demo', blast['command'])
        self.assertIn('npm run test:demo', blast['command'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
