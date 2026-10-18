#!/usr/bin/env python3
"""Deterministic, stdlib-only renderer for portfolio case-study pages."""
from __future__ import annotations
import argparse
from html import escape as e
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
CASES = [
    dict(slug="lineageguard", number="01", kind="AI SYSTEMS / DEVELOPER TOOLS",
         title="LineageGuard", hero="Know the downstream impact before a schema change ships.",
         tags=["JavaScript", "DataHub MCP", "Metadata", "Developer tooling"],
         repo="https://github.com/ult666666/lineageguard-datahub-agent",
         live="https://lineageguard-datahub-agent.vercel.app/", live_label="Explore live demo",
         image="/assets/lineageguard.jpg", alt="LineageGuard schema change analysis interface",
         sections=[
             ("The problem", [
                 "A schema edit may look local but change the behavior of downstream dashboards, datasets, pipelines or ML models. Reviewers need more than the SQL diff: they need the dependency context.",
                 "The goal was to make an invisible blast radius understandable before the change is applied."
             ]),
             ("The engineering approach", [
                 "LineageGuard brings lineage, ownership, usage and quality signals from DataHub into a structured schema-change review. It generates an impact assessment, staged migration guidance and review notes.",
                 "The workflow returns a block, conditional or proceed decision, with supporting context rather than an unexamined AI assertion."
             ]),
             ("Implementation and verification", [
                 "The public repository contains a DataHub MCP integration, a portable Codex skill, example review artifacts and a runnable demo. Its documented local checks include npm test, npm run mcp:smoke and npm run demo.",
                 "The system emphasizes explainable review artifacts and approval-gated write-back instead of immediately changing the metadata store."
             ]),
             ("Tradeoffs and boundaries", [
                 "Metadata quality affects any automated impact analysis. A generated migration still needs its owning team to validate correctness and deployment sequencing.",
                 "The hosted demo demonstrates the interface and workflow; it is not a guarantee of compatibility with every organization's live DataHub environment."
             ])]),
    dict(slug="motionx", number="02", kind="FRONTEND / PRODUCT ENGINEERING",
         title="MOTIONX", hero="A visual studio experience with deliberate frontend engineering.",
         tags=["Next.js", "TypeScript", "Tailwind CSS", "Python", "Playwright"],
         repo="https://github.com/ult666666/motionx-studio",
         live="https://madebymotionx.com/", live_label="Visit live website",
         image="/assets/motionx.jpg", alt="MOTIONX cinematic studio website visual",
         sections=[
             ("The problem", [
                 "A motion-first product website should communicate a point of view without sacrificing clarity, responsive design or a straightforward contact flow.",
                 "I wanted the same attention to detail in the implementation that appeared in the final visual direction."
             ]),
             ("The frontend", [
                 "The public site uses Next.js App Router, TypeScript and Tailwind CSS. Its interface emphasizes typography, paced motion and adaptable layouts, with CSS carrying much of the animation.",
                 "The public repository includes Playwright coverage and the site is accessible online."
             ]),
             ("The system behind it", [
                 "A separate Python outreach workflow demonstrates the complementary backend discipline: a language model can draft a message, but deterministic checks and a human authorization boundary prevent a draft from silently becoming a sent email.",
                 "The two systems are intentionally separate, so the presentation layer is not coupled to operational mailing logic."
             ]),
             ("Tradeoffs and boundaries", [
                 "The visual studies on the site are explicitly self-initiated concepts, not claimed client engagements or financial results.",
                 "The outreach code is a reviewed drafting workflow, not an autonomous mass sender. The public source uses fictional test fixtures rather than real prospect data."
             ])]),
    dict(slug="trading-research", number="03", kind="PYTHON / RELIABLE SYSTEMS",
         title="Agentic Trading Research", hero="When AI can propose ideas, software must still verify the evidence.",
         tags=["Python", "Deterministic validation", "Provenance", "Agent workflows"],
         repo="https://github.com/ult666666/agentic-trading-research",
         live=None, live_label=None, image=None, alt=None,
         sections=[
             ("The problem", [
                 "An AI-generated market thesis can sound convincing while relying on stale prices, weak sources or incompatible risk assumptions.",
                 "The engineering challenge is to make uncertainty visible and to keep a persuasive narrative from becoming execution authority."
             ]),
             ("The architecture", [
                 "The research architecture separates model-generated proposals from deterministic Python checks for source freshness, provenance, risk and decision boundaries.",
                 "Structured outputs and explicit failure states let the system withhold a result when necessary instead of quietly inventing confidence."
             ]),
             ("Engineering principles", [
                 "I prioritize reproducible tests, machine-readable evidence, conservative release gates, and reviewable control-plane changes.",
                 "This pattern also applies outside finance: AI can help generate options, while clear policy and traceable evidence decide what is actually allowed."
             ]),
             ("Status and limitations", [
                 "The public repository is a curated research and architecture snapshot, not an automatically trading product. Production Morning delivery and deployment gates remain separate from the public portfolio.",
                 "It makes no claim of live profitability or autonomous order execution. A human retains responsibility for any real financial action."
             ])]),
    dict(slug="frontier-ai-valuation-lab", number="08", kind="FINTECH / FULL-STACK ENGINEERING",
         title="Frontier AI Valuation Lab", hero="Make a valuation's assumptions as reviewable as its code.",
         tags=["Financial modeling", "JavaScript", "Node.js API", "Source provenance", "Excel / PDF"],
         repo="https://github.com/ult666666/frontier-ai-valuation-lab",
         live="https://frontier-ai-valuation-lab.vercel.app/", live_label="Explore interactive demo",
         image=None, alt=None,
         sections=[
             ("The problem", [
                 "A private AI company's headline valuation can combine a dated funding round, an annualized revenue figure and a forecast built on very different assumptions. A calculator can perform the arithmetic correctly while leaving those differences hidden.",
                 "I wanted an interactive research tool that makes the chain from evidence to assumptions to enterprise value visible. Anthropic and OpenAI provide a demanding case: rapid revenue growth, substantial investment needs and incomplete public financial disclosures."
             ]),
             ("Reviewing the economics", [
                 "The AI-assisted review examined remaining-year cash flow, discount dates, tax policy, working capital, terminal reinvestment and the enterprise-to-equity bridge. The resulting economic FCFF model funds perpetual growth through an explicit growth-to-ROIC relationship and keeps unknown balance-sheet items unavailable.",
                 "A useful discovery was that higher early growth does not always produce a higher valuation: it can require more investment before operating profits arrive. The reverse-DCF solver now checks derivative turning points to find multiple admissible growth rates and targets that touch the value curve without crossing it."
             ]),
             ("Building a reviewable application", [
                 "The browser and Node.js API share the same deterministic JavaScript calculation engine. Input validation, explicit failure states, scenario analysis and sensitivity calculations are exercised through model and API tests, including multiple-root, tangent-root and invalid-input cases.",
                 "Dated source records distinguish reported observations from analyst assumptions. The interactive model is accompanied by a formula-based Excel workbook and a PDF report, so the investment policy and calculations can be inspected outside the interface. Structured exports preserve the scenario being reviewed."
             ]),
             ("My role and the project boundaries", [
                 "I built Frontier AI Valuation Lab as an independent, AI-assisted portfolio project under my own name, Charles Dai. The work combines financial-model review, full-stack implementation, source organization and reproducible verification. The repository makes that process inspectable.",
                 "This is a financial modeling and software engineering demo. Its outputs are scenario enterprise values derived from analyst assumptions and incomplete public disclosures. A hypothetical equity bridge is labeled separately; the project does not establish a security-specific price target or a trading performance record."
             ])]),
]


def render(case: dict) -> str:
    title, intro = e(case["title"]), e(case["hero"])
    tags = "".join(f"<span>{e(x)}</span>" for x in case["tags"])
    links = '<a class="button button-quiet" href="' + e(case["repo"], quote=True) + '" target="_blank" rel="noopener noreferrer">Explore source ↗</a>'
    if case["live"]:
        links = '<a class="button button-primary" href="' + e(case["live"], quote=True) + '" target="_blank" rel="noopener noreferrer">' + e(case["live_label"]) + ' ↗</a>' + links
    media = ('<figure class="case-hero-media"><img src="' + e(case["image"]) + '" alt="' + e(case["alt"]) + '" loading="eager"><figcaption>Visual from the public project repository.</figcaption></figure>') if case["image"] else ""
    sections, toc = [], []
    for i, (heading, paragraphs) in enumerate(case["sections"], 1):
        ident = "section-" + str(i)
        toc.append(f'<a href="#{ident}">{e(heading)}</a>')
        sections.append(f'<section id="{ident}"><h2>{e(heading)}<span class="punctuation">.</span></h2>' +
                        "".join(f"<p>{e(p)}</p>" for p in paragraphs) + "</section>")
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0b1012">
  <meta name="description" content="{intro}">
  <meta property="og:type" content="article"><meta property="og:title" content="{title} — Charles Dai">
  <meta property="og:description" content="{intro}">
  <link rel="canonical" href="https://ult666666.github.io/projects/{case["slug"]}.html">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="stylesheet" href="/styles.css">
  <script defer src="/script.js"></script><title>{title} — Engineering Case Study | Charles Dai</title>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header" id="top"><div class="container header-inner">
  <a class="brand" href="/" aria-label="Charles Dai, home"><span class="brand-mark">CD<span class="brand-dot">.</span></span><span class="brand-sub">CHARLES DAI<span> / </span>SOFTWARE</span></a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav">Menu <span aria-hidden="true">☰</span></button>
  <nav class="primary-nav" id="primary-nav" aria-label="Primary navigation">
    <a href="/#work">Work</a><a href="/#approach">Approach</a><a href="/#about">About</a>
    <a href="/#contact" class="nav-contact">Let's connect ↗</a>
  </nav>
</div></header>
<main id="main">
<section class="case-hero container">
  <a class="case-back" href="/#work">← ALL PROJECTS</a>
  <p class="eyebrow">{e(case["number"])} / {e(case["kind"])}</p>
  <h1>{title}<span class="punctuation">.</span></h1>
  <p class="case-lead">{intro}</p>
  <div class="case-metadata">{tags}</div>
  <div class="hero-actions">{links}</div>
  {media}
</section>
<div class="case-main container">
  <nav class="case-sidebar" aria-label="On this page"><span class="sidebar-heading">CASE STUDY CONTENTS</span>{''.join(toc)}</nav>
  <article class="case-article">{''.join(sections)}
    <div class="case-callout"><strong>Source first.</strong><p>This page describes engineering choices documented in the public project repository. Follow the source link for code, runnable instructions, and scope limitations.</p></div>
    <a class="button button-primary" href="/#work">Back to all projects ↗</a>
  </article>
</div>
</main>
<footer class="site-footer container"><a href="/" class="footer-brand">CD<span>.</span></a><span>CHARLES DAI © <span id="year">2026</span></span><span><a href="https://github.com/ult666666" target="_blank" rel="noopener noreferrer">GITHUB ↗</a></span></footer>
</body>
</html>
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for case in CASES:
        destination = ROOT / "projects" / f"{case['slug']}.html"
        content = "\n".join(line.rstrip() for line in render(case).splitlines()) + "\n"
        if args.check:
            if not destination.is_file() or destination.read_text(encoding="utf-8") != content:
                print("CASE_STUDY_OUTDATED:" + case["slug"], file=sys.stderr)
                return 1
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
            print("CASE_GENERATED", destination.name)
    if args.check:
        print("CASE_STUDIES_VERIFIED", len(CASES))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
