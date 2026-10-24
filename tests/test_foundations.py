"""Foundations review route: exact sources, runnable checks, stated scope and publication wiring."""
from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'projects' / 'foundations.html'
REPOS = ('quantkit', 'powerlift', 'ledgerline', 'saas-analytics-warehouse', 'searchlite', 'contrastkit',
         'citecheck')
LIVE = ('https://ult666666.github.io/saas-analytics-warehouse/', 'https://ult666666.github.io/searchlite/',
        'https://ult666666.github.io/contrastkit/')
# Each command was run against the published repositories; the page states its observed result.
COMMANDS = (
    'uv run pytest tests/test_backtest_engine.py -k lookahead -v',
    'uv run pytest tests/test_sequential.py -k "jennison_turnbull or published_bounds or five_looks" -v',
    'uv run pytest tests/test_concurrency.py -v',
    'make data build',
    'npx vitest run test/engine/highlight.test.ts test/engine/scoring.test.ts -t "hostile|exactly the score"',
    'npx contrastkit check 777 fff',
    'uv run citecheck index examples/handbook\n'
    'uv run citecheck ask "What is the deadline for submitting an expense?"',
)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs, self.commands, self.headings = [], [], []
        self._capture, self._buffer = None, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a' and 'href' in a:
            self.hrefs.append(a['href'])
        if tag in ('h2', 'code'):
            self._capture, self._buffer = tag, []

    def handle_data(self, data):
        if self._capture:
            self._buffer.append(data)

    def handle_endtag(self, tag):
        if tag == self._capture:
            text = ''.join(self._buffer).strip()
            (self.headings if tag == 'h2' else self.commands).append(text)
            self._capture = None


def parse() -> Page:
    page = Page()
    page.feed(PAGE.read_text(encoding='utf-8'))
    return page


class FoundationsTests(unittest.TestCase):
    def test_projects_in_order(self):
        self.assertEqual(parse().headings[:len(REPOS)], list(REPOS))

    def test_each_project_links_source_design_and_proving_code(self):
        hrefs = parse().hrefs
        for repo in REPOS:
            with self.subTest(repo=repo):
                base = 'https://github.com/ult666666/' + repo
                self.assertIn(base + '/blob/main/docs/DESIGN.md', hrefs)
                self.assertTrue(any(h == base or h.startswith(base + '/') for h in hrefs))
                self.assertTrue(any(h.startswith(base + '/blob/main/') and '/test' in h for h in hrefs),
                                'A walkthrough must link the proving test')
        for url in LIVE:
            self.assertIn(url, hrefs)

    def test_walkthrough_commands_are_exact(self):
        commands = parse().commands
        for command in COMMANDS:
            self.assertIn(command, commands)

    def test_scope_and_limits_are_stated(self):
        text = PAGE.read_text(encoding='utf-8')
        for phrase in ('Synthetic and fictional data', 'not investment advice', 'it is not a benchmark',
                       'All data is synthetic', 'no claims of production use or adoption',
                       'hand-written synthetic responses'):
            self.assertIn(phrase, text)

    def test_homepage_sitemap_and_inventory_include_the_page(self):
        self.assertEqual((ROOT / 'index.html').read_text().count('href="/projects/foundations.html"'), 1)
        self.assertIn('https://ult666666.github.io/projects/foundations.html', (ROOT / 'sitemap.xml').read_text())
        inventory = json.loads((ROOT / 'public-files.json').read_text())['files']
        self.assertIn('projects/foundations.html', inventory)


if __name__ == '__main__':
    unittest.main(verbosity=2)
