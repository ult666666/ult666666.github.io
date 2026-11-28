#!/usr/bin/env python3
"""Render the reviewed project inventory without requiring a browser runtime."""
import argparse
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
AREAS = {'finance': 'Finance', 'data': 'Data & analytics', 'ai': 'AI & search',
         'backend': 'Backend systems', 'product': 'Product & HCI'}
FORMS = {'web': 'Web application', 'desktop': 'Desktop application', 'library': 'Library / CLI',
         'service': 'Local API service', 'research': 'Research demonstration', 'coursework': 'Coursework', 'platform': 'Platform game'}
HOSTS = {'github.com', 'ult666666.github.io', 'frontier-ai-valuation-lab.vercel.app',
         'lineageguard-datahub-agent.vercel.app', 'madebymotionx.com', 'teen-budgeting-hw3.vercel.app'}
OVERVIEW_FIELDS = {'id', 'name', 'areas', 'form', 'stack', 'summary'}
WALKTHROUGH_FIELDS = {'scenario', 'inspect', 'limits', 'command', 'links'}


def valid_url(value):
    if not isinstance(value, str) or any(c.isspace() or ord(c) < 32 for c in value) or '\\' in value:
        return False
    if value.startswith('/projects/'):
        return bool(re.fullmatch(r'/projects/[a-z0-9-]+\.html(?:#[a-z0-9-]+)?', value))
    try:
        url = urlsplit(value)
        return (url.scheme == 'https' and url.hostname in HOSTS and not url.username
                and not url.password and url.port is None)
    except ValueError:
        return False


def validate(catalog):
    if (not isinstance(catalog, dict) or set(catalog) != {'version', 'projects'}
            or type(catalog['version']) is not int or catalog['version'] != 1
            or not isinstance(catalog['projects'], list) or not 1 <= len(catalog['projects']) <= 100):
        raise ValueError('Invalid catalog document')
    ids = set()
    for project in catalog['projects']:
        if not isinstance(project, dict):
            raise ValueError('Invalid project fields')
        overview_only = project.get('form') == 'coursework' and set(project) == OVERVIEW_FIELDS
        if not overview_only and set(project) != OVERVIEW_FIELDS | WALKTHROUGH_FIELDS:
            raise ValueError('Invalid project fields')
        for key in ('id', 'name', 'summary'):
            if not isinstance(project[key], str) or not project[key].strip():
                raise ValueError('Missing project review information: ' + key)
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', project['id']) or project['id'] in ids:
            raise ValueError('Invalid or duplicate project id')
        ids.add(project['id'])
        if not isinstance(project['form'], str) or project['form'] not in FORMS:
            raise ValueError('Unknown project form')
        if (not isinstance(project['areas'], list) or not project['areas']
                or any(not isinstance(area, str) or area not in AREAS for area in project['areas'])
                or len(project['areas']) != len(set(project['areas']))):
            raise ValueError('Invalid project areas')
        if (not isinstance(project['stack'], list) or not project['stack']
                or any(not isinstance(item, str) or not item.strip() for item in project['stack'])):
            raise ValueError('Invalid project stack')
        if overview_only:
            continue
        for key in ('scenario', 'inspect', 'limits', 'command'):
            if not isinstance(project[key], str) or not project[key].strip():
                raise ValueError('Missing project review information: ' + key)
        if not isinstance(project['links'], list) or not project['links']:
            raise ValueError('Project requires an inspection link')
        for link in project['links']:
            if (not isinstance(link, dict) or set(link) != {'label', 'url'}
                    or not isinstance(link['label'], str) or not link['label'].strip()
                    or not valid_url(link['url'])):
                raise ValueError('Invalid project link')


def render_walkthrough(project):
    if 'command' not in project:
        return ''
    p = {key: escape(project[key], quote=True) for key in ('name', 'scenario', 'inspect', 'limits', 'command')}
    links = []
    for link in project['links']:
        url = escape(link['url'], quote=True)
        label = escape(link['label'], quote=True)
        links.append(f'<a href="{url}" aria-label="{label} ({p["name"]})">{label}</a>')
    return f'''<nav class="catalog-links" aria-label="{p['name']} links">{''.join(links)}</nav>
<details class="catalog-walkthrough"><summary>Walkthrough<span class="sr-only"> for {p['name']}</span></summary>
<dl><dt>Example</dt><dd>{p['scenario']}</dd><dt>In the code</dt><dd>{p['inspect']}</dd><dt>Limits</dt><dd>{p['limits']}</dd></dl>
<div class="catalog-command"><h3>Run from the project folder</h3><pre><code>{p['command']}</code></pre></div></details>'''


def render(catalog):
    validate(catalog)
    title = 'Project explorer | Charles Dai'
    canonical = 'https://ult666666.github.io/projects/catalog.html'
    description = 'Software by Charles Dai, with source code, demos and notes on how each project works.'
    cards = []
    for project in catalog['projects']:
        p = {key: escape(project[key], quote=True) for key in ('id', 'name', 'summary')}
        areas = ' '.join(project['areas'])
        tags = ''.join('<li>' + escape(item) + '</li>' for item in project['stack'])
        labels = ' · '.join(AREAS[area] for area in project['areas'])
        cards.append(f'''<article class="catalog-card" id="{p['id']}" data-areas="{areas}">
<header class="catalog-entry-heading"><h2>{p['name']}</h2>
<p class="catalog-kind"><span>{FORMS[project['form']]}</span> <span>{escape(labels)}</span></p></header>
<div class="catalog-entry-body"><p class="catalog-summary">{p['summary']}</p>
<ul class="catalog-stack" aria-label="Technology">{tags}</ul>
{render_walkthrough(project)}</div></article>''')
    options = ''.join('<option value="' + key + '">' + escape(label) + '</option>' for key, label in AREAS.items())
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light"><meta name="theme-color" content="#fbfbfa">
<meta name="description" content="{escape(description)}">
<title>{title}</title>
<meta property="og:type" content="website"><meta property="og:title" content="{title}">
<meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://ult666666.github.io/assets/portfolio-og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Charles Dai’s portfolio featuring crossbook, LineageGuard Studio and Luma Keys.">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{canonical}"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/project-catalog.css"><script defer src="/project-catalog.js"></script></head>
<body class="catalog-page"><a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header" id="top"><div class="wrap header-inner">
  <a class="site-name" href="/">Charles Dai</a>
  <nav class="primary-nav" id="primary-nav" aria-label="Primary">
    <a href="/#work">Work</a><a href="/#index">Index</a><a href="/#about">About</a><a href="/#contact">Contact</a>
  </nav>
</div></header>
<main class="wrap" id="main"><section class="catalog-intro" aria-labelledby="title">
<h1 id="title">Project explorer</h1></section>
<form class="catalog-controls" role="search" hidden><div><label for="catalog-query">Search projects</label><input id="catalog-query" type="search" placeholder="Name, topic or tool" autocomplete="off"></div><div><label for="catalog-area">Focus area</label><select id="catalog-area"><option value="all">All areas</option>{options}</select></div><button class="button" type="reset">Clear filters</button></form>
<div class="catalog-results"><p id="catalog-count" role="status" aria-live="polite">{len(cards)} projects</p></div>
<p id="catalog-empty" hidden>No matching projects. Try another term or clear the filters.</p>
<div class="catalog-grid">{''.join(cards)}</div>
</main>
<footer class="site-footer wrap"><p>© 2026 Charles Dai</p><p class="footer-links"><a href="https://github.com/ult666666/ult666666.github.io">Source</a><a href="#top">Back to top</a></p></footer>
</body></html>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=ROOT / 'docs/project-catalog.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'projects/catalog.html')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        output = render(json.loads(args.catalog.read_text(encoding='utf-8')))
        if args.check:
            if not args.output.exists() or args.output.read_text(encoding='utf-8') != output:
                parser.exit(1, 'Project catalog is stale; run python3 scripts/build_catalog.py\n')
            print('Project catalog is current')
        else:
            args.output.write_text(output, encoding='utf-8')
            print('Rendered project catalog')
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
