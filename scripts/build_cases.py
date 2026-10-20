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
         title="Frontier AI Valuation Lab", hero="Connect a capital objective to scenario mathematics, an inspectable calculation and a documented business decision.",
         tags=["Capital Strategy 4.0", "Financing & ownership", "Scenario analysis", "Node.js API", "Python verification"],
         repo="https://github.com/ult666666/frontier-ai-valuation-lab",
         live="https://frontier-ai-valuation-lab.vercel.app/capital.html#worked-decision", live_label="Try Capital Strategy Studio",
         secondary_links=[
             ("Worked decision PDF", "https://frontier-ai-valuation-lab.vercel.app/downloads/Frontier_AI_Capital_Decision.pdf"),
             ("Capital method", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/CAPITAL_STRATEGY.md"),
             ("Try Ownership Frontier", "https://frontier-ai-valuation-lab.vercel.app/index.html#ownership-example")
         ],
         image="/assets/frontier-ai-capital-4-0.png", image_width=1440, image_height=1381, alt="Capital Strategy Studio showing hypothetical financing plans against the capital objective and retained ownership floor",
         caption="The working Capital Strategy Studio: explicit objectives, separate plan markers and a complete decision workflow. All financing terms are hypothetical.",
         fintech_showcase=True,
         showcase=dict(label="A SWITCHING VALUE YOU CAN REPRODUCE", question="When does the modeled existing-cohort allocation favor the smaller round over the larger one?", value="$635bn", footnote="Modeled pre-money equity residual where Plans A and B tie at a $600bn cohort allocation. The threshold follows the entered round terms; it is neither an operating EV target nor a company financing price."),
         section_ids={
             "Start with the business decision": "section-1",
             "Compare capital and ownership objectives": "section-financing",
             "Challenge the choice across explicit scenarios": "section-2",
             "Make the engineering inspectable": "section-3",
             "My role and the project boundaries": "section-4"
         },
         section_links={
             "Start with the business decision": [
                 ("Open the worked decision", "https://frontier-ai-valuation-lab.vercel.app/capital.html#worked-decision"),
                 ("Read the decision brief", "https://frontier-ai-valuation-lab.vercel.app/downloads/Frontier_AI_Capital_Decision.html")
             ],
             "Compare capital and ownership objectives": [
                 ("Explore the ownership limit", "https://frontier-ai-valuation-lab.vercel.app/index.html#ownership-example"),
                 ("Read the financing method", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/FINANCING_LENS.md")
             ],
             "Challenge the choice across explicit scenarios": [
                 ("Capital comparison method", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/CAPITAL_STRATEGY.md"),
                 ("Independent numerical reference", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/scripts/check_capital_reference.py"),
                 ("Explore Value Horizon", "https://frontier-ai-valuation-lab.vercel.app/horizon.html")
             ],
             "Make the engineering inspectable": [
                 ("Architecture and trust boundaries", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/ARCHITECTURE.md"),
                 ("Reproduce the demo", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/DEMO_WALKTHROUGH.md")
             ]
         },
         section_media={
             "Compare capital and ownership objectives": dict(
                 image="/assets/frontier-ai-ownership-3-6.png",
                 alt="Ownership Frontier in the working Financing Lens: an assumed $250 billion pre-money quote, $25 billion primary round and 90 percent minimum retention of a starting stake, with a $27.78 billion capital limit",
                 width=975, height=612,
                 caption="A supporting drill-down in the Model: at the assumed $250 billion pre-money quote, retaining at least 90% of a starting stake permits approximately $27.78 billion in primary capital. The new Capital Studio compares multiple submitted plans and scenarios around these same round definitions.",
                 href="https://frontier-ai-valuation-lab.vercel.app/index.html#ownership-example"
             )
         },
         proof_links=[
             ("Capital methodology", "Eligibility, signed residual allocations, regret, switching values and model-conditioned price intervals.", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/CAPITAL_STRATEGY.md"),
             ("API contract", "Exact submitted snapshots, complete results and explicit failure states.", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/API.md"),
             ("Verification record", "Independent calculations, browser journeys and the scope of each check.", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/VERIFICATION.md"),
             ("Dated source register", "Reported company evidence and analyst assumptions with separate meanings.", "https://frontier-ai-valuation-lab.vercel.app/index.html#sources")
         ],
         review=dict(
             intro="Start with the three-plan example. Tighten the retained-stake floor from 88% to 90%, then raise the capital objective from $25bn to $30bn. The first edit leaves one eligible plan; the second leaves none. Follow the same exact state through the code, calculation API and exported decision.",
             steps=[
                 ("Change the objective", "Try the two edits above, then restore 88% to recover the larger-capital plan. After observing B become eligible, restore the $25bn capital objective and 88% floor before comparing the scenario rankings.", "Open Capital Studio", "https://frontier-ai-valuation-lab.vercel.app/capital.html#worked-decision"),
                 ("Inspect the rule", "Compare signed residual allocations and read where the ranking changes. The declared minimax rule never replaces the analyst's choice.", "Inspect code and checks", "#engineering-evidence"),
                 ("Keep the reasoning", "Record a preference, tradeoff, review trigger and information needed. Export or reopen a versioned decision with exact numeric inputs.", "Read the worked brief", "https://frontier-ai-valuation-lab.vercel.app/downloads/Frontier_AI_Capital_Decision.html")
             ],
             evidence=[
                 ("Consistent financial meaning", "The capital engine composes the preserved operating, horizon, financing and ownership modules. The same calculation runs in browser and API.",
                  [("Capital calculation", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/public/lib/capital-strategy.js"), ("JSON handler", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/lib/http.js")],
                  "Independent arithmetic and hand fixtures check allocations, switching values, eligibility and price intervals. HTTP checks compare the complete response and bounded inputs.",
                  [("Independent reference", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/scripts/check_capital_reference.py"), ("Capital HTTP tests", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/tests/capital-api.test.js")]),
                 ("Current-state verification", "Every financial edit invalidates the prior API result. A revision token and request cancellation prevent a late response from verifying an edited decision.",
                  [("Studio controller", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/public/capital.js")],
                  "Browser checks exercise live edits, invalid drafts, objective conflicts, delayed verification, keyboard operation and responsive layouts.",
                  [("Capital browser workflow", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/tests/capital-browser.mjs")]),
                 ("Portable and inert decisions", "Versioned records carry exact inputs and plain-text reasoning. Imports recompute analysis; a preview precedes applying a new draft. Long decisions retain a JSON export path.",
                  [("Record validation", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/public/lib/capital-record.js"), ("Share codec", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/public/lib/capital-share.js")],
                  "Record and codec tests challenge incompatible versions, untrusted stored results, Unicode, markup-like notes, malformed tokens and size limits.",
                  [("Record tests", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/tests/capital-record.test.js"), ("Share tests", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/tests/capital-share.test.js")]),
                 ("Visible limits and dated evidence", "Unavailable bridges, signed negative residuals and an empty eligible set have different meanings. Company source records remain tied to the frozen research date.",
                  [("Capital method", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/CAPITAL_STRATEGY.md"), ("Evidence context", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/EVIDENCE_CONTEXT.md")],
                  "Boundary tests preserve those distinctions. The verification record binds reviewed files and artifacts by hash and separates numerical checks from forecast claims.",
                  [("Capital boundary tests", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/tests/capital-strategy.test.js"), ("Verification record", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/VERIFICATION.md")])
             ]),
         sections=[
             ("Start with the business decision", [
                 "A valuation becomes useful when it helps someone examine a decision. Capital Strategy Studio asks which submitted financing plans fit an explicit capital objective and ownership constraint, what their modeled consequences look like across named scenarios, and what would change an analyst's choice.",
                 "The workflow is Define, Compare, Challenge, Record. The output is a complete decision record: objectives, alternatives, exact operating assumptions, a declared comparison metric, an analyst preference, its tradeoff, the information still needed and a review trigger. A machine-generated ranking remains separate from the person's judgment.",
                 "The worked example uses three hypothetical plans. Plan A assumes a $250bn pre-money quote and $25bn primary raise; Plan B assumes $300bn and $35bn; Plan C assumes $300bn and $20bn. With a $25bn objective and 88% retained starting stake, A and B qualify. At 90%, only A qualifies. A $30bn objective and 90% floor leave none; returning the floor to 88% makes B eligible. These transitions are inspectable business tradeoffs, not a recommendation for either company."
             ]),
             ("Compare capital and ownership objectives", [
                 "Capital and ownership are separate inputs. A plan qualifies only if its primary proceeds meet the stated capital objective and its retained fraction meets the ownership floor. Retaining 90% of a starting stake means a holder beginning with 10% retains at least 9% of the company. The chart shows each submitted plan individually against those objectives, with an equivalent numerical table.",
                 "The capital objective is never inferred from cumulative economic FCFF deficits. That valuation measure includes modeling conventions such as the economic treatment of stock compensation and cannot establish a treasury cash requirement. Primary proceeds remain cash, operations stay fixed, fees are zero and economic rights are equal.",
                 "The existing Financing Lens and Ownership Frontier provide a detailed round-level drill-down. An entered pre-money or post-money quote defines the issuance arithmetic independently of modeled value. A hypothetical cash, debt and other-claims bridge connects operating value to a signed equity residual; no absent balance is silently treated as zero."
             ]),
             ("Challenge the choice across explicit scenarios", [
                 "Each submitted operating scenario has all thirteen valuation assumptions and either perpetual continuation or a finite number of years after 2036. The finite lens assigns zero residual after the selected cutoff. Every scenario is applied to every plan; the tool does not drop an inconvenient or unavailable case.",
                 "For a modeled pre-money equity residual M, a raise R and existing-cohort retention r, the selected allocation metric is r × (M + R). This is a conditional signed residual allocation under the stated simplified round assumptions. Negative results remain signed and are not presented as limited-liability share prices or investor returns.",
                 "The plan comparison reports regret relative to the best eligible submitted plan in each listed scenario, the maximum such regret per plan, and all ties under the minimax rule. Pairwise switching values make ranking sensitivity visible. For Plans A and B, the allocation lines meet at M = $635bn, with each allocating $600bn to the existing cohort. B allocates more below that residual; A allocates more above it.",
                 "A separate diagnostic combines a model-to-quote coverage floor with retained ownership. The resulting pre-money price interval must satisfy every submitted scenario. An empty interval, a nonpositive model-conditioned ceiling, a missing bridge and the no-finite-price case at 100% retention remain distinct. None of these analytical intervals establishes an available financing offer.",
                 "The method is a finite scenario comparison. Case counts are not probabilities, minimax is conditional on the listed cases and declared metric, and three presets cannot prove global robustness. The documentation connects the design to primary-source work on scenario analysis and decisions under uncertainty without importing unsupported probability distributions."
             ]),
             ("Make the engineering inspectable", [
                 "A pure JavaScript capital module composes the preserved financial engines. Browser ES modules and the stateless Node.js API use the same validated snapshot and return the same complete analysis. The capital endpoint keeps the existing 16 KiB request limit and does not receive analyst prose. No API key, database or paid market-data service is required to run the demo.",
                 "The browser invalidates verification when financial inputs change and rejects stale responses. Invalid drafts suppress dependent results. Exported records and UTF-8 share links retain the submitted numeric precision and reasoning; imported analysis is recalculated instead of trusted. Import preview, bounded payloads and inert text rendering protect the decision state without pretending that an export is an authenticated financial document.",
                 "Independent Python calculations and hand-derived fixtures challenge financial arithmetic separately from browser/API agreement. Browser workflows exercise edits, portability, explicit failure states and responsive use. Current verification receipts identify the reviewed source by hash; production and release checks are reported with their own scope.",
                 "Earlier workflows remain usable: the Model, Value Horizon, exact grouped attribution in Thesis Lab, contextual evidence and the Research Casebook. Its local persistence still handles corrupt data, unavailable storage and pending-save edits. The portfolio's publication allowlist and staged-byte verification preserve the newer engineering safeguards alongside this project expansion."
             ]),
             ("My role and the project boundaries", [
                 "I built Frontier AI Valuation Lab as an independent, AI-assisted portfolio project under my own name, Charles Dai. My work connects financial-model review, product and business framing, quantitative method design, full stack implementation and reproducible verification. This case study presents inspectable work rather than a claimed client engagement or investment track record.",
                 "Application 4.0.0 adds capital method 1.0.0 while retaining financial engine 3.0.0 and the frozen 18 October 2026 research snapshot. The formula-based Excel workbook and original financial-review PDF remain the version 3.0 baseline. New company evidence is not silently substituted for the reviewed assumptions.",
                 "The outputs depend on illustrative assumptions and incomplete public disclosures. The simplified financing excludes fees, preference waterfalls, option-pool changes, conversions, secondary sales, investment-driven operating benefits and future rounds. It does not determine actual funding need, availability of financing, a security-specific price target or investment returns. The documented boundaries are part of the decision product."
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
    image_size = (' width="' + e(str(case["image_width"]), quote=True) + '" height="' + e(str(case["image_height"]), quote=True) + '"') if case.get("image_width") and case.get("image_height") else ""
    media = ('<figure class="case-hero-media"><img src="' + e(case["image"]) + '" alt="' + e(case["alt"]) + '"' + image_size + ' loading="eager"><figcaption>' + e(case.get("caption", "Visual from the public project repository.")) + '</figcaption></figure>') if case["image"] else ""
    extra_styles = '<link rel="stylesheet" href="/fintech.css">' if case.get("fintech_showcase") else ""
    body_attributes = ' class="case-fintech"' if case.get("fintech_showcase") else ""
    fintech_nav = '<a href="/fintech.html">Fintech</a>' if case.get("fintech_showcase") else ""
    example = case.get("showcase")
    showcase = (f'<div class="case-capital-example"><div><span class="case-example-label">{e(example["label"])}</span><p>{e(example["question"])}</p><a class="fintech-text-link" href="/fintech.html">Explore the fintech portfolio →</a></div><div><p class="case-example-value">{e(example["value"])}</p><p class="case-example-footnote">{e(example["footnote"])}</p></div></div>') if example else ""
    proof = '<div class="case-proof-grid">' + ''.join('<a class="case-proof-link" href="' + e(url, quote=True) + '" target="_blank" rel="noopener noreferrer"><strong>' + e(label) + ' ↗</strong><span>' + e(description) + '</span></a>' for label, description, url in case.get("proof_links", [])) + '</div>' if case.get("proof_links") else ""
    review = render_review(case.get("review"))
    sections, toc = [], ['<a href="#review-guide">Review the engineering</a>'] if review else []
    for i, (heading, paragraphs) in enumerate(case["sections"], 1):
        ident = case.get("section_ids", {}).get(heading, "section-" + str(i))
        toc.append(f'<a href="#{e(ident, quote=True)}">{e(heading)}</a>')
        section_links = case.get("section_links", {}).get(heading, [])
        resources = '<div class="case-section-links">' + ''.join(
            '<a href="' + e(url, quote=True) + '" target="_blank" rel="noopener noreferrer">' + e(label) + ' <span aria-hidden="true">↗</span></a>'
            for label, url in section_links
        ) + '</div>' if section_links else ''
        figure = case.get("section_media", {}).get(heading)
        detail_media = (
            '<figure class="case-detail-media"><a href="' + e(figure["href"], quote=True) + '" target="_blank" rel="noopener noreferrer">'
            '<img src="' + e(figure["image"], quote=True) + '" alt="' + e(figure["alt"], quote=True) + '" width="' + e(str(figure["width"]), quote=True) + '" height="' + e(str(figure["height"]), quote=True) + '" loading="lazy" decoding="async"></a>'
            '<figcaption>' + e(figure["caption"]) + '</figcaption></figure>'
        ) if figure else ''
        sections.append(f'<section id="{e(ident, quote=True)}"><h2>{e(heading)}<span class="punctuation">.</span></h2>' +
                        "".join(f"<p>{e(p)}</p>" for p in paragraphs) + detail_media + resources + "</section>")
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
