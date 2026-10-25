"""Catch lost handoff discovery, misstated numbers and moving evidence links."""
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REVIEWED = 'https://github.com/ult666666/ult666666.github.io/blob/0dd85f87a7cdcd46030ff81bbb4de456019385ce/'


class Node:
    def __init__(self, tag, attrs=()):
        self.tag, self.attrs = tag, dict(attrs)
        self.children, self.words = [], []

    @property
    def text(self):
        return ' '.join(' '.join(self.words).split())

    def find(self, tag=None, **attrs):
        return [node for child in self.children
                for node in [child, *child.find()]
                if (tag is None or node.tag == tag)
                and all(node.attrs.get(k) == v for k, v in attrs.items())]


class Document(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.root = Node('document')
        self.stack = [self.root]
        self.feed(raw)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
                       'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        for node in self.stack:
            node.words.append(data)


class HandoffShowcaseTests(unittest.TestCase):
    def setUp(self):
        self.page = Document((ROOT / 'projects/engineering-lab.html').read_text()).root

    def handoff(self):
        sections = self.page.find('section', id='operations-handoff')
        self.assertEqual(len(sections), 1, 'One stable visitor handoff destination is required')
        return sections[0]

    def test_discovery_and_reviewed_source_destinations(self):
        section = self.handoff()
        intro = self.page.find('section', **{'class': 'lab-intro container'})[0]
        self.assertEqual(len(intro.find('a', href='#operations-handoff')), 1)
        self.assertEqual(len(self.page.find('details', **{'class': 'lab-walkthrough'})), 3)
        for anchor in ('section-1', 'section-2', 'section-3', 'section-4'):
            self.assertEqual(len(self.page.find(id=anchor)), 1)
        links = [node.attrs['href'] for node in section.find('a')]
        for relative in ('README.md', 'release-lock.json', 'evidence/clean.html',
                         'evidence/synthetic-regression.html'):
            self.assertIn(REVIEWED + 'examples/operations_handoff/' + relative, links)
        for link in links:
            if 'examples/operations_handoff' in link:
                self.assertTrue(link.startswith(REVIEWED), 'Evidence must stay at the reviewed ancestor')
        self.assertIn('GitHub source', section.text)

    def test_comparison_has_caption_date_headers_explicit_units_and_exact_values(self):
        section = self.handoff()
        tables = section.find('table')
        self.assertEqual(len(tables), 1)
        table = tables[0]
        self.assertEqual(len(table.find('caption')), 1)
        self.assertIn('Learning Lab / 学习计划', table.find('caption')[0].text)
        columns = table.find('thead')[0].find('th')
        self.assertEqual([node.attrs.get('scope') for node in columns], ['col'] * 3)
        self.assertEqual([node.text for node in columns], [
            'Measure', 'Current: October 1–31, 2026',
            'Prior: August 31–September 30, 2026'])
        rows = table.find('tbody')[0].find('tr')
        # Hand-derived: current visits 2*1.5 + 2*2 = 7; prior 2*1.25 + .75 = 3.25.
        expected = [
            ['Distinct people', '3', '2'], ['Attendance', '4', '3'],
            ['Participant-hours', '7', '3.25'], ['Session-hours', '3.5', '2'],
            ['Actual spend (USD)', '130.25', '131.00']]
        self.assertEqual([[node.text for node in row.children] for row in rows], expected)
        self.assertTrue(all(row.find('th')[0].attrs.get('scope') == 'row' for row in rows))

    def test_recorded_gate_is_explicitly_synthetic_with_prepared_local_command(self):
        section = self.handoff()
        for phrase in ('AI-assisted', 'educational', 'English/Mandarin',
                       'receipt effect', 'CSV import', 'inbox acknowledgment',
                       'separate transactions', 'advisory', 'no provider calls',
                       '13025 → 13024', '9/9', '8/9', 'exit 0', 'exit 3', 'exit 2'):
            self.assertIn(phrase, section.text)
        self.assertIn('synthetic', section.text.lower())
        self.assertIn('recorded contract', section.text)
        commands = section.find('pre')
        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0].text,
                         'python3 -B scripts/verify_handoff.py --wheel-dir "$WHEEL_DIR" --output "$OUTPUT_DIR"')
        for prerequisite in ('Python 3.11+', 'repository root', 'local paths',
                             'trusted', 'must not exist', 'download', 'offline'):
            self.assertIn(prerequisite, section.text)
        self.assertNotIn('/Users/', section.text)

    def test_release_routes_stay_on_shipped_versions_and_preserve_live_report(self):
        hrefs = [node.attrs.get('href') for node in self.page.find('a')]
        for repo, tag in [('relaybox', '0.4.0'), ('relaybox', '0.3.0'),
                          ('tracebench', '0.3.0'), ('impact-ledger', '1.2.0')]:
            self.assertIn(f'https://github.com/ult666666/{repo}/releases/tag/v{tag}', hrefs)
        self.assertIn('https://ult666666.github.io/tracebench/', hrefs)
        for repo, tag in [('tracebench', '0.4.0'), ('impact-ledger', '1.2.1')]:
            self.assertNotIn(f'https://github.com/ult666666/{repo}/releases/tag/v{tag}', hrefs)

    def test_handoff_uses_existing_public_inventory(self):
        self.handoff()
        inventory = json.loads((ROOT / 'public-files.json').read_text())['files']
        visuals = json.loads((ROOT / 'docs/RECENT_VISUALS.json').read_text())['assets']
        allowed_extra = {record['asset'] for record in visuals}
        self.assertEqual(len(allowed_extra), 4)
        self.assertEqual({name for name in inventory if name.startswith('assets/recent-')},
                         allowed_extra, 'Only reviewed gallery images may extend the inventory')
        self.assertEqual(len(inventory) + 1, 36 + len(allowed_extra),
                         'Payload includes .nojekyll, four reviewed images and three catalog files')
        self.assertFalse(any(name.startswith(('examples/', 'scripts/', 'docs/', 'tests/'))
                             for name in inventory))
        articles = Document((ROOT / 'index.html').read_text()).root.find('article')
        self.assertEqual(sum('project-card' in node.attrs.get('class', '').split()
                             for node in articles), 9)
        self.assertEqual({name for name in inventory if name.startswith('projects/')}, {
            'projects/lineageguard.html', 'projects/motionx.html',
            'projects/trading-research.html', 'projects/frontier-ai-valuation-lab.html',
            'projects/engineering-lab.html', 'projects/foundations.html', 'projects/catalog.html'})


if __name__ == '__main__':
    unittest.main()
