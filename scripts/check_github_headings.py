#!/usr/bin/env python3
"""Check links to headings against GitHub's current rendering of the target Markdown."""

import json
import re
import subprocess
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = set()
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.anchors.add(attrs['id'])
        if tag == 'a':
            if attrs.get('href'):
                self.hrefs.add(attrs['href'])
            if attrs.get('name'):
                self.anchors.add(attrs['name'])


def markdown_heading(href):
    url = urlsplit(href)
    if url.scheme != 'https' or url.netloc != 'github.com' or not url.fragment:
        return None
    path = re.fullmatch(r'/ult666666/([\w.-]+)/blob/([^/]+)/(.+\.md)', url.path, flags=re.I)
    if not path or re.fullmatch(r'L\d+(?:-L\d+)?', url.fragment):
        return None
    repo, ref, filename = path.groups()
    endpoint = f'repos/ult666666/{repo}/contents/{filename}?ref={quote(unquote(ref), safe="")}'
    return endpoint, unquote(url.fragment)


def collect(pages):
    targets = defaultdict(lambda: defaultdict(set))
    for name, html in pages:
        document = Anchors()
        document.feed(html)
        document.close()
        for href in document.hrefs:
            target = markdown_heading(href)
            if target:
                endpoint, heading = target
                targets[endpoint][heading].add((name, href))
    return targets


def missing_headings(rendered_html, headings):
    document = Anchors()
    document.feed(rendered_html)
    document.close()
    return sorted(heading for heading in headings
                  if heading not in document.anchors and 'user-content-' + heading not in document.anchors)


def main():
    public = json.loads((ROOT / 'public-files.json').read_text(encoding='utf-8'))['files']
    targets = collect((name, (ROOT / name).read_text(encoding='utf-8'))
                      for name in public if name.endswith('.html'))
    problems = []
    for endpoint, headings in sorted(targets.items()):
        try:
            rendered = subprocess.run(
                ['gh', 'api', '-H', 'Accept: application/vnd.github.html+json', endpoint],
                capture_output=True, text=True, timeout=30, check=True,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            problems.append(f'Could not read {endpoint}: {exc}')
            continue
        for heading in missing_headings(rendered.stdout, headings):
            for page, href in sorted(headings[heading]):
                problems.append(f'{page} links to missing heading: {href}')
    for problem in problems:
        print(problem, file=sys.stderr)
    print(f'Checked {sum(map(len, targets.values()))} headings in {len(targets)} GitHub files.')
    return int(bool(problems))


if __name__ == '__main__':
    sys.exit(main())
