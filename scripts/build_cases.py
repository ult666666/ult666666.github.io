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
         title="Frontier AI Valuation Lab", hero="Explain a change in enterprise value, then test the assumptions a target would require.",
         tags=["Thesis Lab", "Exact grouped attribution", "Sensitivity landscape", "Node.js API", "Python verification"],
         repo="https://github.com/ult666666/frontier-ai-valuation-lab",
         live="https://frontier-ai-valuation-lab.vercel.app/thesis.html", live_label="Explore Thesis Lab",
         image="/assets/frontier-ai-thesis-3-2.png", alt="Frontier AI Thesis Lab comparing Anthropic Base and Bull cases with signed valuation attribution",
         sections=[
             ("From a headline to a testable thesis", [
                 "A private AI company's headline valuation says little about which growth, margin or capital assumptions support it. A scenario calculator can return a precise number while leaving those dependencies hard to inspect.",
                 "I built Thesis Lab to make that reasoning visible. It opens with Anthropic's Base and Bull cases, then lets viewers compare any two preset or edited cases for the same company. OpenAI is also available. The product connects an explanation of the valuation gap to a concrete test of what a chosen target would require."
             ]),
             ("Explain the gap, then test a target", [
                 "A signed waterfall allocates the change in modeled enterprise value across six assumption groups. Exact grouped Shapley attribution evaluates all 64 combinations of reference and alternative groups, equivalent to averaging their marginal contributions over all 720 orders. This includes interactions without making the result depend on which slider was changed first.",
                 "The target landscape varies the cost of capital and the 2036 operating margin while holding the alternative case's other eleven inputs fixed. At each discount rate, it solves the margin needed to support a selected enterprise value within the displayed range, or explains why no supported solution is available. These are conditional model results; the map assigns no scenario probabilities.",
                 "A comparison link preserves the numeric precision of both complete cases, their optional hypothetical equity bridges, and the selected landscape and target. A standalone printable HTML brief carries the assumptions, attribution, forecasts and source context. Presenter view keeps the analysis clear during a walkthrough, and either case can be opened in the full model."
             ]),
             ("Shared calculations, independent checks", [
                 "The browser and stateless Node.js API share deterministic financial and thesis modules, including attribution and landscape operations. Bounded inputs and explicit invalid states give the interface and API the same calculation contract.",
                 "Reproducible verification uses a separate Python financial model and a different attribution algorithm: it enumerates all 720 orders to check JavaScript's weighted coalition calculation. Independent piecewise-linear margin solutions check the target frontier's bisection solver. The committed verification report covers 28 case comparisons, 390 grid cells and 80 frontier points, with numerical tolerances and hashes binding the evidence to the source files.",
                 "The original workbench remains accessible alongside the paired Anthropic and OpenAI story through revenue, annual free cash flow and value beyond 2036. Bear, Base and Bull comparisons, paired stress controls and the complete thirteen-input model remain available for exploring the financial mechanics."
             ]),
             ("My role and the project boundaries", [
                 "I built Frontier AI Valuation Lab as an independent, AI-assisted portfolio project under my own name, Charles Dai. My work combines financial-model review, interaction design, full-stack implementation and reproducible verification. The economic model makes reinvestment, discount dates, terminal returns on capital and the equity bridge explicit.",
                 "Application 3.2.0 retains financial engine 3.0.0 and the frozen 18 October 2026 research snapshot. The formula-based Excel workbook and existing PDF report remain the version 3.0 model and review snapshot; the comparison brief reflects the two selected cases.",
                 "The outputs are scenario enterprise values derived from analyst assumptions and incomplete public disclosures. Attribution depends on the selected reference and the fixed group definitions; it describes the model's arithmetic and cannot establish business causality. Negative enterprise value is preserved, and invalid calculations are identified. Hypothetical equity bridges are labeled separately. The project makes no claim of a security-specific price target, a financing valuation or investment returns."
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
