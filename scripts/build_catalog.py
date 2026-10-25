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
    for number, project in enumerate(catalog['projects'], 1):
        p = {key: escape(project[key], quote=True) for key in ('id', 'name', 'summary', 'scenario', 'inspect', 'limits', 'command')}
        areas = ' '.join(project['areas'])
        tags = ''.join('<li>' + escape(item) + '</li>' for item in project['stack'])
        links = ''.join('<a href="' + escape(link['url'], quote=True) + '">' + escape(link['label'])
                        + ' <span aria-hidden="true">↗</span></a>' for link in project['links'])
        labels = ' / '.join(AREAS[area] for area in project['areas'])
        cards.append(f'''<article class="catalog-card" id="{p['id']}" data-areas="{areas}">
<div class="catalog-card-top"><span>{number:02d} / {escape(labels)}</span><span class="catalog-form">{FORMS[project['form']]}</span></div>
<h2>{p['name']}</h2><p class="catalog-summary">{p['summary']}</p>
<ul class="catalog-stack" aria-label="Technology">{tags}</ul>
<dl><dt>A scenario to explore</dt><dd>{p['scenario']}</dd><dt>Follow the implementation</dt><dd>{p['inspect']}</dd><dt>Project scope</dt><dd>{p['limits']}</dd></dl>
<div class="catalog-command"><h3>Local review command</h3><pre><code>{p['command']}</code></pre></div>
<nav class="catalog-links" aria-label="{p['name']} links">{links}</nav></article>''')
    options = ''.join('<option value="' + key + '">' + escape(label) + '</option>' for key, label in AREAS.items())
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Explore Charles Dai's software projects by problem, technology and runnable scenario, with source, demos and scope statements.">
<meta name="theme-color" content="#0b1012"><title>Project explorer — Charles Dai</title>
<link rel="canonical" href="https://ult666666.github.io/projects/catalog.html"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/project-catalog.css"><script defer src="/project-catalog.js"></script></head>
<body><a class="skip-link" href="#main">Skip to projects</a>
<header class="catalog-header"><div class="container"><a class="brand" href="/"><span class="brand-mark">CD<span class="brand-dot">.</span></span><span class="brand-sub">CHARLES DAI / SOFTWARE</span></a><nav aria-label="Portfolio navigation"><a href="/">Selected work</a><a href="/projects/engineering-lab.html">Engineering lab</a><a href="https://github.com/ult666666">GitHub ↗</a></nav></div></header>
<main class="container" id="main"><section class="catalog-intro" aria-labelledby="title"><p class="section-index">PROJECT EXPLORER / PROBLEMS INTO SOFTWARE</p>
<h1 id="title">Find the problem.<br><span>Follow the build.</span></h1><p class="catalog-lead">Finance tools, data products, AI systems and interfaces. Choose a project, try a concrete scenario, then inspect the decisions and code behind it.</p>
<div class="catalog-routes"><a href="/projects/frontier-ai-valuation-lab.html">A financing decision ↗</a><a href="/projects/engineering-lab.html#operations-handoff">An end-to-end operations handoff ↗</a><a href="/projects/foundations.html">Reference-checked foundations ↗</a></div>
<p class="catalog-note">Public projects include web apps, local tools, research demonstrations and coursework built with AI assistance. Each entry explains its scope; links lead to the current source and documented checks. Run commands from a repository checkout after its README setup; requirements differ. Demo database seed commands require a fresh path.</p></section>
<form class="catalog-controls" role="search" hidden><div><label for="catalog-query">Search projects</label><input id="catalog-query" type="search" placeholder="Try Python, SQLite, accessibility…" autocomplete="off"></div><div><label for="catalog-area">Focus area</label><select id="catalog-area"><option value="all">All areas</option>{options}</select></div><button type="reset">Clear filters</button></form>
<div class="catalog-results"><p id="catalog-count" role="status" aria-live="polite">{len(cards)} projects</p><span>SCENARIO → IMPLEMENTATION → SCOPE</span></div>
<p id="catalog-empty" hidden>No projects match those filters. Try a broader search or clear the filters.</p>
<div class="catalog-grid">{''.join(cards)}</div>
<footer class="catalog-footer"><p>Interested in how these pieces fit together?</p><a href="/#contact">Get in touch ↗</a><a href="/">Back to selected work ↗</a></footer></main></body></html>
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
