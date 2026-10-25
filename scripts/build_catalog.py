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
FIELDS = {'id', 'name', 'areas', 'form', 'stack', 'summary', 'scenario', 'inspect', 'limits', 'command', 'links'}


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
        if not isinstance(project, dict) or set(project) != FIELDS:
            raise ValueError('Invalid project fields')
        for key in ('id', 'name', 'summary', 'scenario', 'inspect', 'limits', 'command'):
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
        if not isinstance(project['links'], list) or not project['links']:
            raise ValueError('Project requires an inspection link')
        for link in project['links']:
            if (not isinstance(link, dict) or set(link) != {'label', 'url'}
                    or not isinstance(link['label'], str) or not link['label'].strip()
                    or not valid_url(link['url'])):
                raise ValueError('Invalid project link')


def render(catalog):
    validate(catalog)
    cards = []
    for project in catalog['projects']:
        p = {key: escape(project[key], quote=True) for key in ('id', 'name', 'summary', 'scenario', 'inspect', 'limits', 'command')}
        areas = ' '.join(project['areas'])
        tags = ''.join('<li>' + escape(item) + '</li>' for item in project['stack'])
        links = ''.join('<a href="' + escape(link['url'], quote=True) + '">' + escape(link['label']) + '</a>'
                        for link in project['links'])
        labels = ' · '.join(AREAS[area] for area in project['areas'])
        cards.append(f'''<article class="catalog-card" id="{p['id']}" data-areas="{areas}">
<div class="catalog-card-top"><span>{escape(labels)}</span><span class="catalog-form">{FORMS[project['form']]}</span></div>
<h2>{p['name']}</h2><p class="catalog-summary">{p['summary']}</p>
<ul class="catalog-stack" aria-label="Technology">{tags}</ul>
<dl><dt>A scenario to explore</dt><dd>{p['scenario']}</dd><dt>Follow the implementation</dt><dd>{p['inspect']}</dd><dt>Project scope</dt><dd>{p['limits']}</dd></dl>
<div class="catalog-command"><h3>Local review command</h3><pre><code>{p['command']}</code></pre></div>
<nav class="catalog-links" aria-label="{p['name']} links">{links}</nav></article>''')
    options = ''.join('<option value="' + key + '">' + escape(label) + '</option>' for key, label in AREAS.items())
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light"><meta name="theme-color" content="#f6f3ec">
<meta name="description" content="Explore Charles Dai's software projects by problem, technology and runnable scenario, with source, demos and scope statements.">
<title>Project explorer | Charles Dai</title>
<link rel="canonical" href="https://ult666666.github.io/projects/catalog.html"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/project-catalog.css"><script defer src="/project-catalog.js"></script></head>
<body class="catalog-page"><a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header" id="top"><div class="wrap header-inner">
  <a class="site-name" href="/">Charles Dai</a>
  <nav class="primary-nav" id="primary-nav" aria-label="Primary">
    <a href="/#work">Work</a><a href="/#index">Index</a><a href="/#about">About</a><a href="/#contact">Contact</a>
  </nav>
</div></header>
<main class="wrap" id="main"><section class="catalog-intro" aria-labelledby="title">
<a class="case-back" href="/#index">← All work</a>
<p class="eyebrow">Project explorer</p>
<h1 id="title">Every project, with a way to try it</h1>
<p class="catalog-lead">Search by problem or technology. Each entry has a scenario to try, a command to run locally, where to look in the code, and what the project does not do.</p>
<p class="catalog-note">These include web apps, local tools, research demonstrations and coursework, built with AI assistance. Run a command from a checkout of its repository after following that README; requirements differ, and demo database seed commands need a fresh path.</p></section>
<form class="catalog-controls" role="search" hidden><div><label for="catalog-query">Search projects</label><input id="catalog-query" type="search" placeholder="Try Python, SQLite, accessibility…" autocomplete="off"></div><div><label for="catalog-area">Focus area</label><select id="catalog-area"><option value="all">All areas</option>{options}</select></div><button class="button" type="reset">Clear filters</button></form>
<div class="catalog-results"><p id="catalog-count" role="status" aria-live="polite">{len(cards)} projects</p></div>
<p id="catalog-empty" hidden>No projects match those filters. Try a broader search, or clear the filters.</p>
<div class="catalog-grid">{''.join(cards)}</div>
</main>
<footer class="site-footer wrap"><p>© 2026 Charles Dai</p><p>No cookies or tracking.</p><p class="footer-links"><a href="https://github.com/ult666666">GitHub</a><a href="#top">Back to top</a></p></footer>
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
