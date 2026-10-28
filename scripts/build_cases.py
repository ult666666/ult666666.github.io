#!/usr/bin/env python3
"""Deterministic, stdlib-only renderer for portfolio case-study pages."""
from __future__ import annotations
import argparse
from html import escape as e
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
CASES = [
    {'slug': 'lineageguard',
     'number': '01',
     'kind': 'Developer tools',
     'title': 'LineageGuard Studio',
     'hero': 'A workbench for reviewing database schema changes. Each check runs as a step in a small '
             'workflow, every verdict keeps the evidence it was based on, and a run that crashes can resume '
             'where it stopped.',
     'tags': ['Workflow orchestration', 'Offline review verification', 'SQLite recovery', 'Read-only MCP'],
     'repo': 'https://github.com/ult666666/lineageguard-datahub-agent',
     'live': 'https://lineageguard-datahub-agent.vercel.app/',
     'live_label': 'Open Studio',
     'image': '/assets/lineageguard-studio-v2.png',
     'image_width': 1440,
     'image_height': 1669,
     'alt': 'LineageGuard Studio with an executable review graph, explicit evidence readiness and a live '
            'event trace',
     'caption': 'The working Studio 2.0 browser-session preview, using synthetic catalog evidence. The '
                'separate local runtime adds durable SQLite checkpoints.',
     'sections': [('The problem',
                   ['A data-change review has to coordinate more than a risk score: which source was read, '
                    'whether its evidence is complete, which tasks finished, and what remains trustworthy '
                    'after interruption.',
                    'I expanded the original LineageGuard demo into a source-bound workflow system. The '
                    'visible graph represents compiled execution dependencies, rather than a predefined '
                    'narrative attached to a final result.']),
                  ('The orchestration system',
                   ['The typed composer rejects unknown capabilities, cycles, missing dependencies and '
                    'invalid budgets before a read begins. A shared browser/Node interpreter runs '
                    'independent evidence reads concurrently, tracks attempts and deadlines, and '
                    'checkpoints actual state transitions.',
                    'Compatibility risk and evidence readiness remain separate. Unknown usage is not zero, '
                    'truncated lineage is not complete, and BIGINT to SMALLINT is not treated as safe '
                    'simply because both types are numeric. Deterministic policy—not an LLM confidence '
                    'score—determines the review outcome.']),
                  ('Failure and recovery evidence',
                   ['The local SQLite coordinator uses revision compare-and-swap, expiring writer leases '
                    'and admission reservations. Tests interrupt a test-owned process after a committed '
                    'checkpoint, reopen the database, refuse an obsolete writer and resume the same run '
                    'identity in a new generation.',
                    'Complete, current outputs are reused only under an unchanged source and request '
                    'binding. Changed input invalidates previous results and local acknowledgements. The '
                    'browser exposes pause, reload, resume, cancellation, source-outage recovery, exact '
                    'exports and comparisons between alternative plans.',
                    'The saved-comparison revision 5d7df02 verified on 26 October 2026 has 135 Node tests, '
                    '41 browser journeys across both storage modes and 19 evaluation assertions. These are separate, overlapping checks, not '
                    'independent evidence of catalog truth. The original v2.0.0 release keeps its '
                    'historical verification record; later launcher and Inspector changes are identified '
                    'by their own commits.']),
                  ('Verify the exported review',
                   ['Review Inspector checks the current review or an exported JSON file without uploading '
                    'it, writing run history, opening a catalog connection or resuming a workflow. A '
                    'recipient can inspect a review after it leaves the application instead of trusting a '
                    'screenshot or a claimed checksum.',
                    'I reproduced an export inconsistency that survived a recomputed outer checksum: the '
                    'final SQL draft no longer matched the completed step output. The added semantic guard '
                    'checks result-to-step agreement, validates the embedded evidence, reproduces '
                    'deterministic compatibility and policy, and regenerates the draft. The same guard now '
                    'runs before JSON, Markdown and SQL exports.',
                    'The panel separates the recorded decision from the assessment of embedded evidence at '
                    'inspection time. A previously valid review may now need fresh evidence. It shows '
                    'source authentication as false: internal consistency is not authentication, a digital '
                    'signature, independently observed execution or permission to migrate. The Inspector '
                    'shares the same policy functions with the runtime; it is a replay check, not an '
                    'independent policy implementation.',
                    'A local file remains local. The file-only CLI and browser panel reject malformed or '
                    'ambiguous JSON and oversized inputs, clear stale success after refusal, and do not '
                    'restore imported packages as runnable state. Browser tests disable networking during '
                    'inspection and check that no request or checkpoint write occurs.']),
                  ('Compare two saved reviews',
                   ['Open the Compare tab and choose two completed exported reviews. Both files pass the '
                    'same semantic inspection before any difference appears. The report distinguishes '
                    'recorded decisions from current evidence freshness and identifies alternative '
                    'requests explicitly. No current run is needed.',
                    'The browser and file-only command share one comparison implementation and report '
                    'schema. Selecting another file or clearing the panel invalidates an unfinished read '
                    'and removes stale success. The comparison neither uploads files nor imports them '
                    'into run history; existing run state remains unchanged.',
                    'Try the synthetic standard and strict reviews from the comparison guide, then '
                    'download the report. Its zero new tool calls and false authorization flags remain '
                    'visible. An internally consistent export does not authenticate its source or '
                    'authorize a migration.']),
                  ('Try a three-minute engineering review',
                   ['Compose and run. Open Studio, choose Revenue field rename, and run the review. '
                    'Inspect a completed node: the graph, outputs and event trace describe actual '
                    'execution. The decision remains a review result, not permission to execute SQL.',
                    'Break and recover. Choose Evidence-source outage and run it. The lineage step must '
                    'fail rather than produce a favorable result. Select Restore synthetic source, then '
                    'Resume run. Inspect the same run identity in a new generation and the completed '
                    'evidence reused under its unchanged binding.',
                    'Carry and challenge the result. Open Review package and select Inspect current '
                    'review. Export the verified run JSON, then select that file in Review Inspector. '
                    'Compare the recorded conclusion with current freshness. A modified draft without '
                    'consistent evidence must be refused. Finally, execute the evaluation suite and '
                    'inspect expected-versus-observed outcomes.']),
                  ('My role, runtime modes and limits',
                   ['I set the product scope, budget and safety boundaries and used AI-assisted '
                    'implementation and regression design to build the compiler, runtime, evidence policy '
                    'and review experience. The components are labeled honestly: deterministic stages are '
                    'not presented as an autonomous LLM team.',
                    'The public browser-session preview executes against same-origin synthetic tools and '
                    'stores checkpoints in the current browser. The local Node service adds durable SQLite '
                    'state. Neither is advertised as an authenticated multi-tenant or distributed '
                    'execution platform.',
                    'No SQL execution, catalog mutation or paid inference is enabled. A local review note '
                    'is not organizational authorization. The optional DataHub capture is read-only and '
                    'conservatively profiled; the release does not claim real-tenant validation.'])],
     'section_links': {'The orchestration system': [('DAG compiler',
                                                     'https://github.com/ult666666/lineageguard-datahub-agent/blob/main/public/studio/core/recipe.js'),
                                                    ('Execution interpreter',
                                                     'https://github.com/ult666666/lineageguard-datahub-agent/blob/main/public/studio/core/runtime.js'),
                                                    ('Architecture',
                                                     'https://github.com/ult666666/lineageguard-datahub-agent/blob/main/docs/ARCHITECTURE.md')],
                       'Failure and recovery evidence': [('Interrupted-process recovery test',
                                                          'https://github.com/ult666666/lineageguard-datahub-agent/blob/main/test/studio/process-recovery.test.mjs'),
                                                         ('Release verification',
                                                          'https://github.com/ult666666/lineageguard-datahub-agent/blob/main/docs/VERIFICATION.md'),
                                                         ('Five-minute walkthrough',
                                                          'https://github.com/ult666666/lineageguard-datahub-agent/blob/main/docs/DEMO_WALKTHROUGH.md')],
                       'My role, runtime modes and limits': [('Threat model',
                                                              'https://github.com/ult666666/lineageguard-datahub-agent/blob/main/docs/THREAT_MODEL.md'),
                                                             ('Original demo history',
                                                              'https://github.com/ult666666/lineageguard-datahub-agent/blob/main/docs/CLASSIC_HISTORY.md')],
                       'Verify the exported review': [('Inspector and trust boundaries',
                                                       'https://github.com/ult666666/lineageguard-datahub-agent/blob/6ed607b5c9ff6f46f2bb3214b04d040b04c02c52/docs/REVIEW_INSPECTOR.md'),
                                                      ('Semantic verification code',
                                                       'https://github.com/ult666666/lineageguard-datahub-agent/blob/6ed607b5c9ff6f46f2bb3214b04d040b04c02c52/public/studio/core/inspection.js'),
                                                      ('Adversarial inspection tests',
                                                       'https://github.com/ult666666/lineageguard-datahub-agent/blob/6ed607b5c9ff6f46f2bb3214b04d040b04c02c52/test/studio/inspection.test.mjs'),
                                                      ('Offline browser checks',
                                                       'https://github.com/ult666666/lineageguard-datahub-agent/blob/6ed607b5c9ff6f46f2bb3214b04d040b04c02c52/scripts/inspection-browser.cjs')],
                       'Compare two saved reviews': [('Saved comparison walkthrough',
                                                       'https://github.com/ult666666/lineageguard-datahub-agent/blob/5d7df021056b9eaa0f913f637cdf0d455f29951d/docs/REVIEW_COMPARISON.md'),
                                                      ('Shared comparison implementation',
                                                       'https://github.com/ult666666/lineageguard-datahub-agent/blob/5d7df021056b9eaa0f913f637cdf0d455f29951d/public/studio/core/review-comparison.js'),
                                                      ('Offline browser and lifecycle checks',
                                                       'https://github.com/ult666666/lineageguard-datahub-agent/blob/5d7df021056b9eaa0f913f637cdf0d455f29951d/scripts/saved-comparison-browser.cjs')],
                       'Try a three-minute engineering review': [('Open the working Studio',
                                                                  'https://lineageguard-datahub-agent.vercel.app/'),
                                                                 ('Walkthrough and interview framing',
                                                                  'https://github.com/ult666666/lineageguard-datahub-agent/blob/6ed607b5c9ff6f46f2bb3214b04d040b04c02c52/docs/DEMO_WALKTHROUGH.md'),
                                                                 ('Current verification record',
                                                                  'https://github.com/ult666666/lineageguard-datahub-agent/blob/main/docs/VERIFICATION.md')]},
     'lineageguard_showcase': True,
     'section_ids': {'The problem': 'section-1',
                     'The orchestration system': 'section-2',
                     'Failure and recovery evidence': 'section-3',
                     'Verify the exported review': 'review-inspector',
                     'Compare two saved reviews': 'saved-comparison',
                     'Try a three-minute engineering review': 'try-workflow',
                     'My role, runtime modes and limits': 'section-4'},
     'section_media': {'Compare two saved reviews': {'image': '/assets/lineageguard-saved-comparison.png',
                                                      'alt': 'Saved standard and strict synthetic reviews compared locally: internally consistent, not authenticated',
                                                      'width': 1170,
                                                      'height': 1073,
                                                      'caption': 'Actual public Compare panel at source 5d7df02, captured on 26 October 2026. Synthetic standard and strict reviews share a request but record different decisions. Internal consistency does not authenticate evidence or approval.',
                                                      'href': 'https://github.com/ult666666/lineageguard-datahub-agent/blob/5d7df021056b9eaa0f913f637cdf0d455f29951d/docs/REVIEW_COMPARISON.md'},
                       'Verify the exported review': {'image': '/assets/lineageguard-review-inspector.png',
                                                      'alt': 'Review Inspector showing the recorded '
                                                             'decision, current evidence freshness and the '
                                                             'explicit boundary: internally consistent, '
                                                             'not authenticated',
                                                      'width': 1170,
                                                      'height': 987,
                                                      'caption': 'Actual Inspector interface from the '
                                                                 'public source at 6ed607b5. Synthetic '
                                                                 'review data; the pass describes internal '
                                                                 'consistency, not authenticated evidence '
                                                                 'or execution approval.',
                                                      'href': 'https://github.com/ult666666/lineageguard-datahub-agent/blob/6ed607b5c9ff6f46f2bb3214b04d040b04c02c52/docs/REVIEW_INSPECTOR.md'}}},
    dict(slug="motionx", number="02", kind="Website",
         title="MOTIONX", hero="The website for MOTIONX, the motion-design studio I run. It is built with Next.js and TypeScript, "
              "and a separate Python workflow checks outreach drafts and waits for a person to approve them.",
         tags=["Next.js", "TypeScript", "Tailwind CSS", "Python", "Playwright"],
         repo="https://github.com/ult666666/motionx-studio",
         live="https://madebymotionx.com/", live_label="Visit live website",
         image="/assets/motionx-site.jpg", image_width=1440, image_height=900,
         alt="The MOTIONX website's opening screen: a glossy 3-D X character standing in a dim cinema beside the headline From first frame to final click",
         caption="The studio site's opening screen, captured on 25 October 2026.",
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
    dict(slug="trading-research", number="03", kind="Research system",
         title="Agentic Trading Research", hero="A research-only system for short-term stock research. Language models gather evidence and "
              "propose ideas, and plain Python checks decide what passes. It cannot place orders.",
         tags=["Python", "Deterministic validation", "Provenance", "Agent workflows"],
         repo="https://github.com/ult666666/agentic-trading-research",
         live=None, live_label=None, image=None, alt=None,
         secondary_links=[
             ("Run synthetic gate", "https://github.com/ult666666/agentic-trading-research/tree/main/examples"),
         ],
         proof_links=[
             ("Runnable gate", "Six fixed synthetic scenarios, no broker or market data", "https://github.com/ult666666/agentic-trading-research/blob/main/examples/fail_closed_gate.py"),
             ("Negative-case tests", "Inspect deterministic HOLD and input validation tests", "https://github.com/ult666666/agentic-trading-research/blob/main/examples/test_fail_closed_gate.py"),
             ("GitHub Actions", "Offline checks of the teaching example, the public test suite and every Markdown link", "https://github.com/ult666666/agentic-trading-research/actions/workflows/research-demo.yml"),
         ],
         section_links={
             "Engineering principles": [
                 ("Try the six synthetic scenarios", "https://github.com/ult666666/agentic-trading-research/tree/main/examples")
             ],
         },
         sections=[
             ("The problem", [
                 "An AI-generated market thesis can sound convincing while relying on stale prices, weak sources or incompatible risk assumptions.",
                 "The engineering challenge is to make uncertainty visible and to keep a persuasive narrative from becoming execution authority."
             ]),
             ("The architecture", [
                 "The research architecture separates model-generated proposals from deterministic Python checks for source freshness, provenance, risk and decision boundaries.",
                 "Structured outputs and explicit failure states let the system withhold a result when necessary instead of quietly inventing confidence.",
                 "A separate, runnable public teaching example shows six synthetic outcomes: one reviewable research case and five HOLD cases, with automated negative tests. It cannot query real markets or place orders."
             ]),
             ("Engineering principles", [
                 "I prioritize reproducible tests, machine-readable evidence, conservative release gates, and reviewable control-plane changes.",
                 "This pattern also applies outside finance: AI can help generate options, while clear policy and traceable evidence decide what is actually allowed."
             ]),
             ("Status and limitations", [
                 "The public repository is a curated research and architecture snapshot, not the complete runnable production system. Its self-contained synthetic demo is independently runnable and deliberately cannot access accounts, market feeds or private runtime.",
                 "It makes no claim of live profitability or autonomous order execution. A human retains responsibility for any real financial action."
             ])]),
    dict(slug="frontier-ai-valuation-lab", number="FEATURED", kind="Fintech",
         title="Frontier AI Valuation Lab", hero="A valuation and financing model for frontier AI labs. Set a capital goal, compare financing plans "
              "across explicit scenarios, and keep a record of the decision and the math behind it.",
         tags=["Capital Strategy 4.0", "Financing & ownership", "Scenario analysis", "Node.js API", "Python verification"],
         repo="https://github.com/ult666666/frontier-ai-valuation-lab",
         live="https://frontier-ai-valuation-lab.vercel.app/capital.html#worked-decision", live_label="Try Capital Strategy Studio",
         secondary_links=[
             ("Worked decision PDF", "https://frontier-ai-valuation-lab.vercel.app/downloads/Frontier_AI_Capital_Decision.pdf"),
             ("Capital method", "https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/CAPITAL_STRATEGY.md"),
             ("Try Ownership Frontier", "https://frontier-ai-valuation-lab.vercel.app/index.html#ownership-example")
         ],
         image="/assets/frontier-ai-capital-visual-20261020.png", image_width=1440, image_height=1271, alt="Capital Strategy Studio showing hypothetical financing plans against the capital objective and retained ownership floor",
         caption="The working Capital Strategy Studio: explicit objectives, separate plan markers and a complete decision workflow. All financing terms are hypothetical.",
         fintech_showcase=True,
         showcase=dict(label="A switching value you can reproduce", question="When does the modeled existing-cohort allocation favor the smaller round over the larger one?", value="$635bn", footnote="Modeled pre-money equity residual where Plans A and B tie at a $600bn cohort allocation. The threshold follows the entered round terms; it is neither an operating EV target nor a company financing price."),
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
             intro="Preview objective changes against your current plans before applying them. In the worked three-plan example, $25bn and 88% leave A and B eligible; 90% leaves A. Raising the objective to $30bn with 90% leaves none; returning to 88% leaves B. Previewing does not change your draft.",
             steps=[
                 ("Preview, then apply", "Open the optional objective preview. Review a pair's result for your current plans, then choose Apply to change only the capital objective and retention floor. Plan terms and decision notes stay intact.", "Preview objective changes", "https://frontier-ai-valuation-lab.vercel.app/capital.html#capital-explore"),
                 ("Inspect the rule", "To compare A and B in the worked example, explicitly apply $25bn and 88% again. Compare signed residual allocations and switching values; the minimax rule never replaces the analyst's choice.", "Inspect code and checks", "#engineering-evidence"),
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
                 "A pure JavaScript capital module composes the preserved financial engines. Browser ES modules and the stateless Node.js API use the same validated snapshot. The browser compares their complete analyses, distinguishing exact agreement from qualified rounding differences. The capital endpoint keeps the existing 16 KiB request limit and does not receive analyst prose. No API key, database or paid market-data service is required to run the demo.",
                 "The browser invalidates verification when financial inputs change and rejects stale responses. Invalid drafts suppress dependent results. Exported records and UTF-8 share links retain the submitted numeric precision and reasoning; imported analysis is recalculated instead of trusted. Import preview, bounded payloads and inert text rendering protect the decision state without pretending that an export is an authenticated financial document.",
                 "Independent Python calculations and hand-derived fixtures challenge financial arithmetic separately from browser/API agreement. Browser workflows exercise edits, portability, explicit failure states and responsive use. Current verification receipts identify the reviewed source by hash; production and release checks are reported with their own scope.",
                 "Earlier workflows remain usable: the Model, Value Horizon, exact grouped attribution in Thesis Lab, contextual evidence and the Research Casebook. Its local persistence still handles corrupt data, unavailable storage and pending-save edits. The portfolio's publication allowlist and staged-byte verification preserve the newer engineering safeguards alongside this project expansion."
             ]),
             ("My role and the project boundaries", [
                 "I built Frontier AI Valuation Lab as an independent, AI-assisted portfolio project under my own name, Charles Dai. My work connects financial-model review, product and business framing, quantitative method design, full stack implementation and reproducible verification. This case study presents inspectable work rather than a claimed client engagement or investment track record.",
                 "Application 4.0.0 adds capital method 1.0.0 while retaining financial engine 3.0.0 and the frozen 18 October 2026 research snapshot. The formula-based Excel workbook and original financial-review PDF remain the version 3.0 baseline. New company evidence is not silently substituted for the reviewed assumptions.",
                 "The outputs depend on illustrative assumptions and incomplete public disclosures. The simplified financing excludes fees, preference waterfalls, option-pool changes, conversions, secondary sales, investment-driven operating benefits and future rounds. It does not determine actual funding need, availability of financing, a security-specific price target or investment returns. The documented boundaries are part of the decision product."
             ])]),
    dict(slug="crossbook", number="04", kind="Fintech infrastructure",
         title="crossbook",
         hero="An order-matching engine in Rust. It applies price-time priority with the order types real venues use, "
              "emits an exact event stream, and gives the same answer, event for event, on Linux, macOS, Windows and in the browser.",
         tags=["Rust", "WebAssembly", "Differential testing", "Mutation testing", "Deterministic replay"],
         repo="https://github.com/ult666666/crossbook",
         live="https://ult666666.github.io/crossbook/", live_label="Open the playground",
         image="/assets/crossbook-playground.png", image_width=1800, image_height=1125,
         alt="The crossbook playground: an order ticket, the order book with the queue at each price level, and the event log",
         caption="The browser playground runs the same engine compiled to WebAssembly. Every order in it is synthetic.",
         sections=[
             ("The problem", [
                 "A matching engine fails quietly. A wrong queue order or an off-by-one quantity still produces trades that look plausible, and nothing crashes.",
                 "I wanted an engine where every rule is written down, every command produces an exact list of events, and a second implementation checks the first after every command."
             ]),
             ("The engine", [
                 "Orders trade by price-time priority: the best price first, then the oldest order at that price. The engine supports limit and market orders, immediate-or-cancel, fill-or-kill, post-only, cancel, modify with explicit queue-priority rules, and four self-trade prevention modes.",
                 "Each side of the book keeps its price levels in a BTreeMap, so the best price is the first or last key. Each level is a first-in, first-out queue threaded through one slab of 48-byte order nodes with 32-bit links. A cancel is constant-time after the ID lookup, and the slab reuses memory as orders come and go.",
                 "The engine never reads a clock or a random number generator and never iterates a hash map. That rule is why a replay of the same commands produces the same events on every platform."
             ]),
             ("How it is checked", [
                 "A second, deliberately naive engine implements the same rules with linear scans. Property tests feed random command streams to both engines and require identical events and identical books after every command, plus structural invariants and quantity conservation: 1,024 random streams per local run and 4,096 in CI.",
                 "A 64-bit fingerprint of a 100,000-command session is pinned in the tests. CI checks it on x86-64 Linux, ARM64 macOS and x86-64 Windows, and a separate check compiles the engine to WebAssembly, replays one million commands under Node.js and requires the same digests.",
                 "Mutation testing with cargo-mutants changed the code 168 ways. The tests caught 140 of the 148 versions that compiled. Of the 8 survivors, 4 exposed real gaps that now have assertions, 2 pointed at redundant code that I deleted, and 2 only removed a capacity hint."
             ]),
             ("Results", [
                 "On one core of a 2.1 GHz Intel Xeon cloud VM, the engine processes 15 to 16 million commands per second of synthetic order flow. Latency per command is 64 ns at the median, 196 ns at p99 and 477 ns at p99.9.",
                 "The same session compiled to WebAssembly runs at about 8.3 million commands per second under Node.js, with the same event digest and state hash as the native build. The figures cover the matching core only, with no network, parsing or persistence on the timed path."
             ]),
             ("Tradeoffs and boundaries", [
                 "A BTreeMap costs a logarithmic lookup per price level. A dense price ladder would be constant-time but needs a bounded price band. The fast integer hasher is not resistant to hostile IDs, so a gateway facing untrusted clients would assign IDs itself.",
                 "crossbook is a learning and benchmarking project, not an exchange. It handles one instrument in memory, has no network gateway and runs only on synthetic data. I built it with AI assistance; the tests, CI checks and benchmark commands in the repository are the evidence for each claim."
             ])],
         section_links={
             "The engine": [("Design notes", "https://github.com/ult666666/crossbook/blob/main/docs/DESIGN.md"),
                            ("Order semantics", "https://github.com/ult666666/crossbook/blob/main/docs/SEMANTICS.md")],
             "How it is checked": [("Testing approach", "https://github.com/ult666666/crossbook/blob/main/docs/TESTING.md"),
                                   ("Reference engine", "https://github.com/ult666666/crossbook/blob/main/crates/crossbook/src/reference.rs")],
             "Results": [("Benchmark method", "https://github.com/ult666666/crossbook/blob/main/docs/BENCHMARKS.md")],
         },
         proof_links=[
             ("Differential tests", "Random command streams through the fast engine and the reference engine, compared after every command.", "https://github.com/ult666666/crossbook/blob/main/crates/crossbook/tests/differential.rs"),
             ("Golden digests", "The pinned 100,000-command fingerprint that CI checks on three operating systems.", "https://github.com/ult666666/crossbook/blob/main/crates/crossbook/tests/flow.rs"),
             ("CI workflow", "Tests, the WebAssembly digest check and the browser smoke test on every push.", "https://github.com/ult666666/crossbook/blob/main/.github/workflows/ci.yml")
         ]),
]


def render_review(review: dict | None) -> str:
    if not review:
        return ""

    def link(label: str, url: str) -> str:
        external = ' target="_blank" rel="noopener noreferrer"' if url.startswith("https://") else ""
        return f'<a href="{e(url, quote=True)}"{external}>{e(label)}</a>'

    steps = "".join(
        f'<li><span class="review-step-index" aria-hidden="true">Step {i}</span><h3>{e(title)}</h3><p>{e(body)}</p>{link(label, url)}</li>'
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
        '<p class="section-index">A guide for reviewers</p><h2 id="review-heading">Review the engineering</h2>'
        f'<p>{e(review["intro"])}</p><ol class="review-steps">{steps}</ol>'
        '<table class="evidence-table" id="engineering-evidence"><caption>Implementation and verification map</caption>'
        '<thead><tr><th scope="col">Engineering concern</th><th scope="col">Implementation</th><th scope="col">Verification</th></tr></thead>'
        f'<tbody>{rows}</tbody></table>'
        '<p class="review-scope">The <a href="https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/VERIFICATION.md" target="_blank" rel="noopener noreferrer">verification record</a> separates local release checks, historical results and their limits. Numerical agreement does not establish forecast accuracy or investment returns.</p></aside>'
    )


def render(case: dict) -> str:
    title, intro = e(case["title"]), e(case["hero"])
    tags = "".join(f"<span>{e(x)}</span>" for x in case["tags"])
    links = '<a class="button button-quiet" href="' + e(case["repo"], quote=True) + '" target="_blank" rel="noopener noreferrer">Source on GitHub</a>'
    if case["live"]:
        links = '<a class="button button-primary" href="' + e(case["live"], quote=True) + '" target="_blank" rel="noopener noreferrer">' + e(case["live_label"]) + '</a>' + links
    links += "".join('<a class="button button-quiet" href="' + e(url, quote=True) + '" target="_blank" rel="noopener noreferrer">' + e(label) + '</a>' for label, url in case.get("secondary_links", []))
    image_size = (' width="' + e(str(case["image_width"]), quote=True) + '" height="' + e(str(case["image_height"]), quote=True) + '"') if case.get("image_width") and case.get("image_height") else ""
    media = ('<figure class="case-hero-media"><img src="' + e(case["image"]) + '" alt="' + e(case["alt"]) + '"' + image_size + ' loading="eager"><figcaption>' + e(case.get("caption", "Visual from the public project repository.")) + '</figcaption></figure>') if case["image"] else ""
    extra_styles = '<link rel="stylesheet" href="/fintech.css">' if case.get("fintech_showcase") else ""
    body_attributes = ' class="case-fintech"' if case.get("fintech_showcase") else ' class="case-lineageguard"' if case.get("lineageguard_showcase") else ""
    fintech_nav = '<a href="/fintech.html">Fintech</a>' if case.get("fintech_showcase") else ""
    example = case.get("showcase")
    showcase = (f'<div class="case-capital-example"><div><span class="case-example-label">{e(example["label"])}</span><p>{e(example["question"])}</p><a class="fintech-text-link" href="/fintech.html">More on the fintech work</a></div><div><p class="case-example-value">{e(example["value"])}</p><p class="case-example-footnote">{e(example["footnote"])}</p></div></div>') if example else ""
    proof = '<div class="case-proof-grid">' + ''.join('<a class="case-proof-link" href="' + e(url, quote=True) + '" target="_blank" rel="noopener noreferrer"><strong>' + e(label) + '</strong><span>' + e(description) + '</span></a>' for label, description, url in case.get("proof_links", [])) + '</div>' if case.get("proof_links") else ""
    review = render_review(case.get("review"))
    sections, toc = [], (['<a href="#review-guide">Review the engineering</a>'] if review else [])
    for i, (heading, paragraphs) in enumerate(case["sections"], 1):
        ident = case.get("section_ids", {}).get(heading, "section-" + str(i))
        toc.append(f'<a href="#{e(ident, quote=True)}">{e(heading)}</a>')
        section_links = case.get("section_links", {}).get(heading, [])
        resources = '<div class="case-section-links">' + ''.join(
            '<a href="' + e(url, quote=True) + '" target="_blank" rel="noopener noreferrer">' + e(label) + '</a>'
            for label, url in section_links
        ) + '</div>' if section_links else ''
        figure = case.get("section_media", {}).get(heading)
        detail_media = (
            '<figure class="case-detail-media"><a href="' + e(figure["href"], quote=True) + '" target="_blank" rel="noopener noreferrer">'
            '<img src="' + e(figure["image"], quote=True) + '" alt="' + e(figure["alt"], quote=True) + '" width="' + e(str(figure["width"]), quote=True) + '" height="' + e(str(figure["height"]), quote=True) + '" loading="lazy" decoding="async"></a>'
            '<figcaption>' + e(figure["caption"]) + '</figcaption></figure>'
        ) if figure else ''
        sections.append(f'<section id="{e(ident, quote=True)}"><h2>{e(heading)}</h2>' +
                        "".join(f"<p>{e(p)}</p>" for p in paragraphs) + detail_media + resources + "</section>")
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light"><meta name="theme-color" content="#f6f3ec">
  <meta name="description" content="{intro}">
  <meta property="og:type" content="article"><meta property="og:title" content="{title}, a case study by Charles Dai">
  <meta property="og:description" content="{intro}">
  <link rel="canonical" href="https://ult666666.github.io/projects/{case["slug"]}.html">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="stylesheet" href="/styles.css">{extra_styles}
  <title>{title}: case study | Charles Dai</title>
</head>
<body{body_attributes}>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header" id="top"><div class="wrap header-inner">
  <a class="site-name" href="/">Charles Dai</a>
  <nav class="primary-nav" id="primary-nav" aria-label="Primary">
    <a href="/#work">Work</a><a href="/#index">Index</a><a href="/#about">About</a><a href="/#contact">Contact</a>
  </nav>
</div></header>
<main id="main">
<section class="case-hero container">
  <a class="case-back" href="/#work">← All work</a>
  <p class="eyebrow">Case study: {e(case["kind"].lower())}</p>
  <h1>{title}</h1>
  <p class="case-lead">{intro}</p>
  <div class="case-metadata">{tags}</div>
  <div class="hero-actions">{links}</div>
  {showcase}{media}
</section>
<div class="case-main container">
  <nav class="case-sidebar" aria-label="On this page"><span class="sidebar-heading">On this page</span>{''.join(toc)}</nav>
  <article class="case-article">{review}{''.join(sections)}{proof}
    <div class="case-callout"><strong>Read the source too.</strong><p>This page describes choices documented in the public repository. The repository has the code, instructions for running it and the limits of what it does.</p></div>
    <a class="button" href="/#work">Back to all projects</a>
  </article>
</div>
</main>
<footer class="site-footer container"><p>© 2026 Charles Dai</p><p>Plain HTML and CSS, with no JavaScript, cookies or tracking.</p><p class="footer-links"><a href="https://github.com/ult666666" target="_blank" rel="noopener noreferrer">GitHub</a><a href="#top">Back to top</a></p></footer>
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
