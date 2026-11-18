"""A moved heading can break a link even when its file still returns HTTP 200."""
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_github_headings.py'
spec = importlib.util.spec_from_file_location('check_github_headings', SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class HeadingTests(unittest.TestCase):
    def test_repeated_links_share_one_file_request_and_keep_the_ref(self):
        href = 'https://github.com/ult666666/ledgerline/blob/abc123/docs/README.md#hold%2Dstate'
        html = f'<a href="{href}">Hold state</a>'
        targets = checker.collect([('index.html', html), ('projects/catalog.html', html)])
        self.assertEqual(dict(targets), {
            'repos/ult666666/ledgerline/contents/docs/README.md?ref=abc123': {
                'hold-state': {('index.html', href), ('projects/catalog.html', href)}
            }
        })

    def test_current_heading_and_explicit_anchor_pass_after_another_is_renamed(self):
        rendered = '<a id="user-content-hold-state"></a><a name="replay"></a>'
        self.assertEqual(checker.missing_headings(rendered, ['hold-state', 'old-hold-state', 'replay']),
                         ['old-hold-state'])

    def test_other_owners_code_lines_and_demo_routes_are_outside_the_check(self):
        for href in ['https://github.com/other/repo/blob/main/docs.md#title',
                     'https://github.com/ult666666/ledgerline/blob/main/docs.md#L10-L12',
                     '/projects/ledgerline.html#wallet-balances',
                     'https://github.com/ult666666/ledgerline/blob/main/src/ledgerline/service.py#L520']:
            with self.subTest(href=href):
                self.assertIsNone(checker.markdown_heading(href))
