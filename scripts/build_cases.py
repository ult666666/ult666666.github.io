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
                 "The public repository is a curated research and architecture snapshot for code review. It does not include the complete runnable system, market data, configuration or operational records.",
                 "It makes no claim of live profitability or autonomous order execution. A human retains responsibility for any real financial action."
             ])]),
    dict(slug="frontier-ai-valuation-lab", number="FEATURED", kind="FINTECH / FULL-STACK ENGINEERING",
         title="Frontier AI Valuation Lab", hero="Make the distant cash flows visible, then follow the assumptions into the valuation.",
         tags=["Value Horizon 3.4", "Financial modeling", "Node.js API", "Python verification", "Research Casebook"],
         repo="https://github.com/ult666666/frontier-ai-valuation-lab",
         live="https://frontier-ai-valuation-lab.vercel.app/horizon.html", live_label="Try Value Horizon",
         secondary_links=[
             ("Complete workspace", "https://frontier-ai-valuation-lab.vercel.app/"),
             ("Value Horizon method", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/VALUE_HORIZON.md")
         ],
         image="/assets/frontier-ai-horizon-3-4.png", alt="Value Horizon showing the selected terminal horizon and the resulting decomposition of operating enterprise value",
         caption="Value Horizon 3.4: the working research tool with illustrative model assumptions.",
         fintech_showcase=True,
         proof_links=[
             ("Financial methodology", "Reinvestment, dates, terminal returns and model boundaries.", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/METHODOLOGY.md"),
             ("API contract", "Submitted inputs, complete results and explicit failure states.", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/API.md"),
             ("Verification record", "Independent calculations, browser journeys and the limits of each check.", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/VERIFICATION.md"),
             ("Dated source register", "Reported evidence and analyst assumptions with separate meanings.", "https://frontier-ai-valuation-lab.vercel.app/index.html#sources")
         ],
         review=dict(
             intro="Start with one research question, then follow the implementation and the checks. The published 3.4 workspace connects an interactive model to reproducible code; its forecasts remain illustrative assumptions.",
             steps=[
                 ("Try a scenario", "Apply a stress in the Overview, then choose Explain this change to inspect the exact comparison.", "Open the workspace", "https://frontier-ai-valuation-lab.vercel.app/"),
                 ("Trace the result", "Follow the source and verification links below to see how arithmetic, navigation and failure states are checked.", "Inspect code and checks", "#engineering-evidence"),
                 ("Keep the reasoning", "Save a case from the Model or Thesis Lab, add a rationale and review trigger, then export the Casebook JSON.", "Open the Casebook", "https://frontier-ai-valuation-lab.vercel.app/casebook.html")
             ],
             evidence=[
                 ("Consistent calculations", "The browser and Node API import the same pure financial engine.",
                  [("FCFF engine", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/public/lib/model.js"), ("JSON handler", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/lib/http.js")],
                  "A separate Python implementation checks annual and terminal outputs. HTTP tests exercise real requests, invalid inputs and size limits.",
                  [("Python parity", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/tests/reference_parity.py"), ("HTTP tests", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/tests/api.test.js")]),
                 ("Exact workflow handoffs", "Model inspection carries the complete comparison, including separate bridges, the target and landscape axes.",
                  [("Journey module", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/public/lib/journey.js")],
                  "Unit and browser checks follow edits into either case and back, preserving the other case and full numerical precision.",
                  [("Journey tests", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/tests/journey.test.js"), ("Browser journey", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/tests/journey-browser.mjs")]),
                 ("Honest save failures", "Local persistence separates financial snapshots from editable notes and preserves earlier saved data when a write fails.",
                  [("Storage adapter", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/public/lib/casebook-store.js")],
                  "Checks cover corrupt JSON, blocked storage, quota failures and edits made while an earlier save is pending.",
                  [("Storage tests", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/tests/casebook-store.test.js"), ("Pending-save browser test", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/tests/save-race-browser.mjs")]),
                 ("Evidence with boundaries", "Dated records provide context for each model input. Editing a forecast never changes its status as an assumption.",
                  [("Evidence module", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/public/lib/evidence.js")],
                  "Checks cover company/input mappings and known source references; the method documents what each relationship can establish.",
                  [("Evidence tests", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/tests/evidence.test.js"), ("Evidence method", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/EVIDENCE_CONTEXT.md")])
             ]),
         sections=[
             ("Start with the cash flows beyond 2036", [
                 "A terminal-value total can hide how much of a valuation depends on cash flows far beyond the explicit forecast. I built Value Horizon to make that dependence visible within a working Anthropic and OpenAI research model.",
                 "The lens keeps the remaining-2026 cash flow and every 2027–2036 forecast year unchanged. A selected number of terminal years starts in 2037. The calculation retains those years' discounted cash flows and assigns zero cash flows and zero residual value after the cutoff. It separates the explicit forecast, included continuation and excluded continuation.",
                 "Under the frozen Anthropic Base assumptions, the perpetual operating enterprise value is $367.8 billion. Keeping ten terminal years, 2037–2046, with no residual produces $248.5 billion. The $119.3 billion difference is discounted continuation excluded by this lens. It is neither an investment loss nor a forecast of the company's closure. The same interaction is available for OpenAI and the other illustrative operating scenarios."
             ]),
             ("Connect the question to a complete research workflow", [
                 "Value Horizon gives a first-time visitor a concrete financial question to explore. The complete Model exposes all thirteen operating assumptions, annual cash-flow reconciliation, sensitivities, reverse DCF and an optional hypothetical equity bridge. Dated evidence is available beside every input.",
                 "Thesis Lab compares two complete cases and allocates their signed enterprise-value difference across six declared assumption groups. Exact grouped Shapley attribution includes the groups' interactions. A target landscape solves a required margin while holding the other eleven assumptions fixed. Either comparison case can be inspected in the Model and returned with its surrounding comparison intact.",
                 "The Research Casebook keeps saved operating cases or comparisons with a rationale, critical assumption, review trigger and selected sources. It supports exact reopening, import previews, conflict preservation and undoable deletion. Browser storage is local to the current origin and profile; explicit JSON export carries the research to another device. Printable briefs retain the calculation and analyst reasoning."
             ]),
             ("Make the engineering inspectable", [
                 "The browser and stateless Node.js API share deterministic financial calculations. Value Horizon adds a separate analytical module and API action around the preserved financial engine. Bounded inputs and explicit invalid states keep a numerical failure from becoming a plausible-looking output.",
                 "Agreement between the browser and API checks that the deployed calculations align. Separate Python calculations and hand-calculated fixtures provide independent arithmetic checks; recorded source hashes identify the inspected model. The repository also exercises full comparison handoffs, local persistence failures, keyboard interaction and responsive layouts. The verification record states what each check establishes and where its coverage ends.",
                 "Source records distinguish actual-period revenue, annualized run-rate, financing references and analyst assumptions. The evidence panels preserve publication, update and retrieval labels. They provide context for an input without certifying its forecast. Notes and source selections are not submitted to the calculation API."
             ]),
             ("My role and the project boundaries", [
                 "I built Frontier AI Valuation Lab as an independent, AI-assisted portfolio project under my own name, Charles Dai. My work combines financial-model review, interaction design, full stack implementation and reproducible verification. The fintech portfolio gateway connects the working demonstration with the decisions and evidence behind it.",
                 "Application 3.4.0 retains financial engine 3.0.0 and the frozen 18 October 2026 research snapshot. The formula-based Excel workbook and existing financial-review PDF remain the version 3.0 baseline. The application does not silently refresh company disclosures or re-underwrite the published operating assumptions.",
                 "The outputs are conditional operating enterprise values derived from illustrative assumptions and incomplete public disclosures. Value Horizon is a truncation lens, not a forecast of business life or an investor's holding-period return. Attribution depends on the selected comparison and groups. Target requirements carry no scenario probabilities. Negative operating value is preserved, invalid calculations are identified, and hypothetical equity bridges are separate. The project makes no claim of a security-specific price target or investment returns."
             ])]),
]


def render_review(review: dict | None) -> str:
    if not review:
        return ""

    def link(label: str, url: str) -> str:
        external = ' target="_blank" rel="noopener noreferrer"' if url.startswith("https://") else ""
        return f'<a href="{e(url, quote=True)}"{external}>{e(label)} <span aria-hidden="true">↗</span></a>'

    steps = "".join(
        f'<li><span class="review-step-index" aria-hidden="true">{i:02d}</span><h3>{e(title)}</h3><p>{e(body)}</p>{link(label, url)}</li>'
        for i, (title, body, label, url) in enumerate(review["steps"], 1)
    )
    rows = "".join(
        f'<tr><th scope="row">{e(question)}</th><td data-label="Implementation"><p>{e(decision)}</p><div class="evidence-links">'
        + "".join(link(label, url) for label, url in source)
        + f'</div></td><td data-label="Verification"><p>{e(verification)}</p><div class="evidence-links">'
        + "".join(link(label, url) for label, url in checks) + "</div></td></tr>"
        for question, decision, source, verification, checks in review["evidence"]
    )
    return (
        '<aside class="case-review" id="review-guide" aria-labelledby="review-heading">'
        '<p class="section-index">A GUIDE FOR REVIEWERS</p><h2 id="review-heading">Review the engineering<span class="punctuation">.</span></h2>'
        f'<p>{e(review["intro"])}</p><ol class="review-steps">{steps}</ol>'
        '<table class="evidence-table" id="engineering-evidence"><caption>Implementation and verification map</caption>'
        '<thead><tr><th scope="col">Engineering concern</th><th scope="col">Implementation</th><th scope="col">Verification</th></tr></thead>'
        f'<tbody>{rows}</tbody></table>'
        '<p class="review-scope">The <a href="https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/VERIFICATION.md" target="_blank" rel="noopener noreferrer">verification record</a> separates local release checks, historical results and their limits. Numerical agreement does not establish forecast accuracy or investment returns.</p></aside>'
    )


def render(case: dict) -> str:
    title, intro = e(case["title"]), e(case["hero"])
    tags = "".join(f"<span>{e(x)}</span>" for x in case["tags"])
    links = '<a class="button button-quiet" href="' + e(case["repo"], quote=True) + '" target="_blank" rel="noopener noreferrer">Explore source ↗</a>'
    if case["live"]:
        links = '<a class="button button-primary" href="' + e(case["live"], quote=True) + '" target="_blank" rel="noopener noreferrer">' + e(case["live_label"]) + ' ↗</a>' + links
    links += "".join('<a class="button button-quiet" href="' + e(url, quote=True) + '" target="_blank" rel="noopener noreferrer">' + e(label) + ' ↗</a>' for label, url in case.get("secondary_links", []))
    media = ('<figure class="case-hero-media"><img src="' + e(case["image"]) + '" alt="' + e(case["alt"]) + '" loading="eager"><figcaption>' + e(case.get("caption", "Visual from the public project repository.")) + '</figcaption></figure>') if case["image"] else ""
    extra_styles = '<link rel="stylesheet" href="/fintech.css">' if case.get("fintech_showcase") else ""
    body_attributes = ' class="case-fintech"' if case.get("fintech_showcase") else ""
    fintech_nav = '<a href="/fintech.html">Fintech</a>' if case.get("fintech_showcase") else ""
    showcase = '<div class="case-horizon-example"><div><span class="case-example-label">A CONCRETE RESEARCH QUESTION</span><p>How much of Anthropic Base value remains with ten terminal years and no residual after 2046?</p><a class="fintech-text-link" href="/fintech.html">Explore the fintech portfolio →</a></div><div><p class="case-example-value">$367.8bn <span>→ $248.5bn</span></p><p class="case-example-footnote">Operating EV · Illustrative Base assumptions · 18 Oct 2026 model date. The explicit forecast stays fixed; the selected continuation begins in 2037.</p></div></div>' if case.get("fintech_showcase") else ""
    proof = '<div class="case-proof-grid">' + ''.join('<a class="case-proof-link" href="' + e(url, quote=True) + '" target="_blank" rel="noopener noreferrer"><strong>' + e(label) + ' ↗</strong><span>' + e(description) + '</span></a>' for label, description, url in case.get("proof_links", [])) + '</div>' if case.get("proof_links") else ""
    review = render_review(case.get("review"))
    sections, toc = [], ['<a href="#review-guide">Review the engineering</a>'] if review else []
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
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="stylesheet" href="/styles.css">{extra_styles}
  <script defer src="/script.js"></script><title>{title} — Engineering Case Study | Charles Dai</title>
</head>
<body{body_attributes}>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header" id="top"><div class="container header-inner">
  <a class="brand" href="/" aria-label="Charles Dai, home"><span class="brand-mark">CD<span class="brand-dot">.</span></span><span class="brand-sub">CHARLES DAI<span> / </span>SOFTWARE</span></a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav">Menu <span aria-hidden="true">☰</span></button>
  <nav class="primary-nav" id="primary-nav" aria-label="Primary navigation">
    <a href="/#work">Work</a>{fintech_nav}<a href="/#approach">Approach</a><a href="/#about">About</a>
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
  {showcase}{media}
</section>
<div class="case-main container">
  <nav class="case-sidebar" aria-label="On this page"><span class="sidebar-heading">CASE STUDY CONTENTS</span>{''.join(toc)}</nav>
  <article class="case-article">{review}{''.join(sections)}{proof}
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
