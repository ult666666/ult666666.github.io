#!/usr/bin/env python3
"""Deterministic, stdlib-only renderer for portfolio case-study pages.

Each case is plain data. A section has a heading, an id that stays stable for
inbound links, paragraphs, an optional list and an optional line of links.
Text is a string or a sequence of strings and (label, url) links, and every
piece is escaped when it is rendered.
"""
from __future__ import annotations
import argparse
from html import escape as e
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

GITHUB = 'https://github.com/ult666666/'
CROSSBOOK = GITHUB + 'crossbook/blob/main/'
LINEAGE = GITHUB + 'lineageguard-datahub-agent/blob/main/'
# The Inspector and comparison material is pinned to the commit the screenshots come from.
LINEAGE_INSPECTOR = GITHUB + 'lineageguard-datahub-agent/blob/ed48eea4370d28c52f3268fadcd3b82a3632a691/'
LINEAGE_COMPARE = LINEAGE_INSPECTOR
FRONTIER = GITHUB + 'frontier-ai-valuation-lab/blob/main/'
APP = 'https://frontier-ai-valuation-lab.vercel.app/'
TRADING = GITHUB + 'agentic-trading-research/'
MOTIONX = GITHUB + 'motionx-studio/'

CASES = [
    dict(
        slug='lineageguard', kind='Developer tools', title='LineageGuard Studio',
        hero='A workbench for reviewing a database schema change against the lineage it affects. Each check '
             'runs as a step in a small workflow, every verdict keeps the evidence behind it, and a run that '
             'crashes resumes where it stopped.',
        stack=['Node.js', 'SQLite', 'dbt'],
        repo=GITHUB + 'lineageguard-datahub-agent',
        live='https://lineageguard-datahub-agent.vercel.app/', live_label='Open Studio',
        image='/assets/lineageguard-studio-review.png', image_width=1440, image_height=1404,
        alt='LineageGuard Studio’s Review tab after a rename review, with the change request on the left '
            'and the workflow graph, decision and run trace on the right',
        caption='The hosted browser-session preview after a rename review, on synthetic catalog data. The '
                'local version adds SQLite checkpoints.',
        body_class='case-lineageguard',
        sections=[
            dict(id='section-1', heading='The problem', body=[
                'Renaming a column looks harmless in one file. A revenue table, the dashboard built on it and '
                'a month-end job may all read that column. A useful review has to say which sources it read, '
                'whether that evidence was complete, and what still holds after a crash.',
                'I rebuilt my earlier LineageGuard demo around those questions. The graph on screen is the '
                'program that runs, and every result stays bound to the source it was read from.',
            ]),
            dict(id='section-2', heading='How a review runs', body=[
                'A typed composer rejects unknown capabilities, cycles, missing dependencies and invalid '
                'budgets before anything is read. One interpreter, shared by the browser and Node, runs '
                'independent evidence reads in parallel with attempt limits and deadlines, and checkpoints '
                'each state change.',
                'Compatibility risk and evidence readiness are judged separately. Unknown usage is not zero, '
                'truncated lineage is not complete, and BIGINT to SMALLINT is not safe just because both '
                'types are numeric. The outcome comes from deterministic rules, and no language model runs in '
                'a review.',
            ], links=[('DAG compiler', LINEAGE + 'public/studio/core/recipe.js'),
                      ('Interpreter', LINEAGE + 'public/studio/core/runtime.js')]),
            dict(id='policy-benchmark', heading='Measuring the policy', body=[
                'I wrote the labelling rules and the labels before the first benchmark run. That run found '
                'five decisions more permissive than their labels. One cleared a new ORDER_ID column next to '
                'an existing order_id, because names were compared with exact case.',
                'After the fixes no decision is more permissive than its label, and CI fails if one becomes '
                'so. The benchmark now has 105 labelled cases, and 101 decisions match. The other four are '
                'stricter than their labels: lossless conversions that the policy does not try to prove safe.',
            ], links=[('Evaluation method', LINEAGE + 'docs/EVALUATION.md'),
                      ('Labelled cases', LINEAGE + 'evals/policy-cases.json')]),
            dict(id='dbt-manifest', heading='Reading a dbt project', body=[
                'Most data teams keep lineage in dbt, so Studio can read a manifest.json, plus the '
                'catalog.json from dbt docs generate, as an offline evidence source. The same interpreter '
                'and policy then review the change.',
                'Renaming fct_mrr.mrr_usd in a trimmed manifest from saas-analytics-warehouse, my synthetic '
                'dbt project, lists five downstream models and two exposures with their owners. It also '
                'finds the 12 dbt tests that read the model. The decision is needs-evidence: a manifest '
                'records what a project declares, not what the warehouse observes.',
                'A manifest has no column lineage, query history or nullability, so evidence from it can '
                'block a change or ask for more, but never clear one. Studio reads manifest schema v12 and '
                'catalog v1 only, and refuses a manifest whose parent_map, child_map and depends_on disagree '
                'or whose graph has a cycle. A seeded property test compares the adapter’s lineage with an '
                'independent walk of depends_on.',
            ], links=[('dbt manifest review', LINEAGE + 'README.md#review-against-a-dbt-manifest'),
                      ('dbt property tests', LINEAGE + 'test/studio/dbt-properties.test.mjs')]),
            dict(id='section-3', heading='Crashes and recovery', body=[
                'The local SQLite coordinator uses revision compare-and-swap and expiring writer leases. A '
                'test kills the review process after a committed checkpoint, reopens the database, refuses '
                'the stale writer and resumes the same run in a new generation.',
                'Finished outputs are reused only while the source and the request are unchanged. A changed '
                'input invalidates earlier results and review notes.',
                'The tests found two more bugs, both fixed: a type parser that let part of a blocked SQL '
                'statement escape its comment, and a summary that could add a fake decision line to the '
                'review brief. Catalog text that looks like instructions is treated as data.',
            ], links=[('Process recovery test', LINEAGE + 'test/studio/process-recovery.test.mjs'),
                      ('Verification record', LINEAGE + 'docs/VERIFICATION.md')]),
            dict(id='review-inspector', heading='Checking an exported review', body=[
                'Review Inspector checks the current review, or an exported JSON file, without uploading it, '
                'writing run history or calling a catalog. Whoever receives a review can check it instead of '
                'trusting a screenshot.',
                'I found an export bug that a recomputed checksum missed: the final SQL draft no longer '
                'matched the step that produced it. The Inspector now checks each result against its step, '
                'replays the policy and regenerates the draft, and the same check runs before every JSON, '
                'Markdown and SQL export.',
                'The recorded decision stays separate from how fresh the evidence is at inspection time. A '
                'pass means the file is internally consistent, which is not authentication or approval. The '
                'Inspector uses the same policy functions as the runtime, so it is a replay check, not an '
                'independent implementation.',
            ], media=dict(
                image='/assets/lineageguard-review-inspector.png', width=1272, height=793,
                alt='Review Inspector showing the recorded decision, the current evidence freshness and the '
                    'result: internally consistent, not authenticated',
                caption='Review Inspector on a synthetic review. A pass means the file is internally '
                        'consistent, not that it is authentic.',
                href=LINEAGE_INSPECTOR + 'docs/REVIEW_INSPECTOR.md'),
                links=[('Inspector guide', LINEAGE_INSPECTOR + 'docs/REVIEW_INSPECTOR.md'),
                       ('Inspection code', LINEAGE_INSPECTOR + 'public/studio/core/inspection.js'),
                       ('Inspection tests', LINEAGE_INSPECTOR + 'test/studio/inspection.test.mjs'),
                       ('Browser checks', LINEAGE_INSPECTOR + 'scripts/inspection-browser.cjs')]),
            dict(id='saved-comparison', heading='Comparing two saved reviews', body=[
                'The Compare tab takes two exported reviews. Both must pass the Inspector before any '
                'difference appears, and the report keeps recorded decisions apart from current evidence '
                'freshness.',
                'The browser and the command line share one comparison module. Nothing is uploaded or '
                'imported into run history, and choosing another file cancels an unfinished read.',
            ], media=dict(
                image='/assets/lineageguard-saved-comparison.png', width=1272, height=803,
                alt='Synthetic standard and strict reviews compared locally: internally consistent, not '
                    'authenticated',
                caption='The Compare panel with synthetic standard and strict reviews of the same request, '
                        'which record different decisions.',
                href=LINEAGE_COMPARE + 'docs/REVIEW_COMPARISON.md'),
                links=[('Comparison walkthrough', LINEAGE_COMPARE + 'docs/REVIEW_COMPARISON.md'),
                       ('Comparison module', LINEAGE_COMPARE + 'public/studio/core/review-comparison.js'),
                       ('Browser checks', LINEAGE_COMPARE + 'scripts/saved-comparison-browser.cjs')]),
            dict(id='try-workflow', heading='Try it', ordered=True, items=[
                [('Open Studio', 'https://lineageguard-datahub-agent.vercel.app/'),
                 ', choose Revenue field rename and run the review. Select a finished step to see its output '
                 'and the event trace.'],
                'Choose Evidence-source outage and run it. The lineage step fails instead of returning a '
                'favorable result. Select Restore synthetic source, then Resume run: the same run continues '
                'in a new generation and reuses the evidence it already had.',
                'Open Review package, select Inspect current review and export the run. Load the file in '
                'Review Inspector and compare the recorded decision with the current freshness. If you edit '
                'the SQL draft in the file, the Inspector refuses it.',
                'Run the evaluation suite and compare the expected and observed outcomes.',
            ], links=[('Demo walkthrough', LINEAGE_INSPECTOR + 'docs/DEMO_WALKTHROUGH.md')]),
            dict(id='section-4', heading='Limits', items=[
                'The hosted demo is a browser-session preview against synthetic tools, with checkpoints kept '
                'in your browser. The local Node service adds SQLite. Neither is a multi-user or distributed '
                'system.',
                'No SQL execution, catalog changes or paid model calls are possible, and a review note is '
                'not an approval.',
                'The optional DataHub capture is read-only and has not been validated against a live '
                'DataHub instance.',
            ], after=['I set the scope and the safety rules, and built Studio with AI coding assistants.']),
        ],
        docs=[
            [('Source and quick start', GITHUB + 'lineageguard-datahub-agent')],
            [('Architecture', LINEAGE + 'docs/ARCHITECTURE.md'), ', including both runtimes and recovery'],
            [('What Studio refuses to approve', LINEAGE + 'docs/ENGINEERING_REVIEW.md')],
            [('Threat model', LINEAGE + 'docs/THREAT_MODEL.md')],
            [('History of the original demo', LINEAGE + 'docs/CLASSIC_HISTORY.md')],
        ]),
    dict(
        slug='motionx', kind='Website', title='MOTIONX',
        hero='The website for MOTIONX, the motion-design studio I run, built with Next.js and TypeScript. '
             'The same repository holds a Python tool that drafts outreach emails and leaves sending to a '
             'person.',
        stack=['Next.js', 'TypeScript', 'Tailwind CSS', 'Python', 'Playwright'],
        repo=MOTIONX[:-1], live='https://madebymotionx.com/', live_label='Visit the site',
        image='/assets/motionx-site.jpg', image_width=1440, image_height=900,
        alt="The MOTIONX website’s opening screen: a glossy 3-D X character standing in a dim cinema beside "
            'the headline From first frame to final click',
        caption="The studio site’s opening screen, captured on 25 October 2026.",
        sections=[
            dict(id='section-1', heading='The site', body=[
                'MOTIONX makes product films and the websites around them, so the studio’s own site has to '
                'move without getting in the way of reading. The homepage is edited for a quick read, and '
                'the detail lives on separate pages.',
            ]),
            dict(id='section-2', heading='The frontend', body=[
                'It uses the Next.js App Router, TypeScript and Tailwind CSS v4. All animation is CSS, with '
                'no animation library, and visitors who prefer reduced motion or save data get still posters '
                'instead of autoplaying video.',
                'The contact form has no backend. It prepares the message and opens it in Gmail or the '
                'default mail app, and never claims that anything was sent. Playwright tests cover '
                'navigation, the contact flow, reduced motion and layouts down to 375 px wide.',
            ]),
            dict(id='section-3', heading='The outreach tool', body=[
                'A separate Python tool researches a prospect and drafts one email. Every draft must pass a '
                'validator that returns PASS or FAIL with reasons, checking length, a single offer, links '
                'and regulated claims.',
                'The drafting code cannot mark a prospect as contacted; sending is a separate step that a '
                'person takes. The public tests run on fictional companies on the reserved .example domain.',
            ]),
            dict(id='section-4', heading='Limits', items=[
                'The films on the site are self-initiated concept work, not client commissions.',
                'The outreach tool drafts email; it does not send any on its own.',
                'The public repository is a curated snapshot of a private one.',
            ], after=['I built both parts with AI coding assistants.']),
        ],
        docs=[
            [('Site source', MOTIONX[:-1]), ' and its ', ('README', MOTIONX + 'blob/main/README.md')],
            [('End-to-end tests', MOTIONX + 'tree/main/e2e')],
            [('Outreach tests', MOTIONX + 'tree/main/outreach/tests')],
        ]),
    dict(
        slug='trading-research', kind='Research system', title='Agentic Trading Research',
        hero='A research-only system for short-term stock research. Language models gather evidence and '
             'propose ideas, and plain Python checks decide what passes. It cannot place orders.',
        stack=['Python'],
        repo=TRADING[:-1], live=None, live_label=None, image=None,
        secondary_links=[('Run the synthetic gate', TRADING + 'tree/main/examples'),
                         ('Overfitting diagnostics',
                          TRADING + 'blob/main/examples/README.md#backtest-overfitting-diagnostics')],
        sections=[
            dict(id='section-1', heading='The problem', body=[
                'A model-written market thesis can sound convincing while it rests on stale prices, weak '
                'sources or risk assumptions that do not fit together. The hard part is keeping a persuasive '
                'story from turning into permission to trade.',
            ]),
            dict(id='section-2', heading='How it works', body=[
                'Proposals from the models pass through deterministic Python checks for source freshness, '
                'provenance, risk limits and decision rules. Every claim needs a source, and a check that '
                'cannot pass returns HOLD with machine-readable reasons instead of a guess.',
                'Broker access is read-only and order tools are blocked, so a person places any real order '
                'by hand. The public repository includes a small runnable gate with six synthetic '
                'scenarios: one reaches human review and five return HOLD.',
            ]),
            dict(id='overfitting-diagnostics', heading='Checking a backtest for overfitting', body=[
                'Try enough strategies and the best one looks skilled by chance. A standard-library package '
                'in the examples applies four checks that quant reviewers use: the probabilistic and '
                'deflated Sharpe ratios (PSR and DSR), the probability of backtest overfitting (PBO), and '
                'White’s Reality Check with Hansen’s SPA test.',
                'In the demo, the best of 100 no-skill strategies has a naive PSR of 0.9989, and all four '
                'checks flag it. A strategy with injected skill passes all four.',
                'The tests reproduce the numerical example in Bailey and López de Prado’s DSR paper, '
                'compare PBO with a brute-force version, and show that each of nine planted bugs makes a '
                'test fail.',
            ]),
            dict(id='section-3', heading='Try it', body=[
                'The examples need Python 3.11 or newer and only the standard library. Run '
                'examples/overfitting_demo.py for the diagnostics, or examples/fail_closed_gate.py --all for the six gate scenarios. Neither '
                'touches the network.',
            ]),
            dict(id='section-4', heading='Limits', items=[
                'The repository is a curated snapshot for reading. Many modules import private code and do '
                'not run here; the examples do.',
                'There is no automated order execution, and nothing here is investment advice or evidence '
                'of profit.',
                'The diagnostics demo uses independent Student-t returns without trading costs.',
            ], after=['I built the system with AI coding assistants, and its research pipeline calls '
                      'language models.']),
        ],
        docs=[
            [('Synthetic review gate', TRADING + 'blob/main/examples/fail_closed_gate.py'),
             ' with six fixed scenarios and no broker or market data'],
            [('Gate tests', TRADING + 'blob/main/examples/test_fail_closed_gate.py')],
            [('Overfitting diagnostics', TRADING + 'tree/main/examples/backtest_diagnostics'), ' and their ',
             ('method and limits', TRADING + 'blob/main/examples/README.md#backtest-overfitting-diagnostics')],
            [('Offline CI checks', TRADING + 'actions/workflows/research-demo.yml')],
        ]),
    dict(
        slug='frontier-ai-valuation-lab', kind='Fintech', title='Frontier AI Valuation Lab',
        hero='A valuation and financing model for frontier AI labs. Set a capital goal, compare financing '
             'plans across scenarios, and keep a record of the decision and the math behind it.',
        stack=['JavaScript', 'Node.js', 'Python'],
        repo=GITHUB + 'frontier-ai-valuation-lab',
        live=APP + 'capital.html#worked-decision', live_label='Try Capital Strategy Studio',
        secondary_links=[('More on the fintech work', '/fintech.html')],
        image='/assets/frontier-ai-capital-visual-20261020.png', image_width=1440, image_height=1271,
        alt='Capital Strategy Studio showing hypothetical financing plans against the capital objective and '
            'retained ownership floor',
        caption='Capital Strategy Studio with the worked example. All financing terms are hypothetical.',
        body_class='case-fintech', docs_id='engineering-evidence',
        sections=[
            dict(id='section-1', heading='The decision', body=[
                'A valuation is useful when it helps someone decide. Capital Strategy Studio asks which '
                'financing plans meet a capital goal and an ownership floor, how they compare across named '
                'scenarios, and what would change the choice.',
                'The worked example tests three hypothetical rounds against two goals: raise at least $25bn, '
                'and let existing holders keep at least 88% of their stake. Plans A and B meet both; at a '
                '90% floor only A does.',
                'The result is a decision record: the goals, the alternatives, the assumptions, the '
                'comparison rule, the analyst’s choice and reasoning, and what would trigger a review. The '
                'ranking the tool computes stays separate from the person’s judgment.',
            ]),
            dict(id='section-financing', heading='Capital and ownership', body=[
                'Capital and ownership are separate goals. A plan qualifies only if it raises enough and '
                'leaves existing holders enough of their stake; keeping 90% of a 10% stake means holding at '
                'least 9% of the company.',
                'The capital goal is an input. It is never inferred from the model’s cash-flow deficits, '
                'which include modeling conventions such as the treatment of stock compensation and '
                'cannot say how much cash a company needs.',
                'Ownership Frontier, an earlier tool in the same app, works out the largest round a quoted '
                'price allows before holders fall below the floor.',
            ], media=dict(
                image='/assets/frontier-ai-ownership-3-6.png', width=975, height=612,
                alt='Ownership Frontier in the Financing Lens: an assumed $250 billion pre-money quote, a $25 '
                    'billion primary round and a 90 percent minimum retention, with a $27.78 billion capital '
                    'limit',
                caption='Ownership Frontier with an assumed $250bn pre-money price and a 90% floor. The '
                        'round can raise up to about $27.78bn.',
                href=APP + 'index.html#ownership-example'),
                links=[('Try Ownership Frontier', APP + 'index.html#ownership-example'),
                       ('Financing method', FRONTIER + 'docs/FINANCING_LENS.md')]),
            dict(id='section-2', heading='Scenarios', body=[
                'Each operating scenario sets all thirteen valuation assumptions, and every scenario is '
                'applied to every plan. The tool never drops an inconvenient case.',
                'For a modeled pre-money equity value M, a raise R and a retained fraction r, the comparison '
                'metric is r × (M + R): the modeled value that ends up with existing holders. It can be '
                'negative, and it is not an investment return.',
                'The tool reports each plan’s regret against the best eligible plan in each scenario, and '
                'the switching values where rankings flip. For Plans A and B the lines cross at M = $635bn. '
                'Below that value B leaves existing holders more; above it, A does.',
            ]),
            dict(id='section-uncertainty', heading='Monte Carlo', body=[
                'Three cases hide the spread between and around them. A seeded Monte Carlo panel puts ranges '
                'on up to five drivers, such as revenue growth, terminal margin and the discount rate, joins '
                'them with a Gaussian copula, and reruns the same DCF engine for every draw.',
                'With the default ranges around the Anthropic Base case, the median value is $364.2B, and '
                'nine draws in ten fall between $197.2B and $694.6B. These figures describe the ranges '
                'entered, not a forecast.',
                'The browser and the API return byte-identical JSON for the same request, and an independent '
                'Python script checks the random numbers, the copula, the percentiles and the tornado chart.',
            ], links=[('Open the Monte Carlo panel', APP + 'index.html#uncertainty')]),
            dict(id='section-3', heading='How it is built', body=[
                'The financial math lives in plain JavaScript modules. The browser and a stateless Node.js '
                'API run the same modules on the same validated input, and the browser compares their '
                'complete results.',
                'Editing any financial input invalidates the last API result, and a revision token stops a '
                'late response from confirming an edited decision. Exports and share links keep the inputs '
                'as entered; an import is recalculated, not trusted.',
                'Separate Python scripts redo the arithmetic, the capital one with Decimal cash flows and '
                'Fraction shares, so a formula bug shows up as a disagreement. Running it needs no API key, '
                'database or paid data feed.',
            ]),
            dict(id='review-guide', heading_id='review-heading', heading='Try it', body=[
                'The objective preview tests new goals against your current plans before you apply them. In '
                'the worked three-plan example:',
            ], ordered=True, items=[
                ['Open the ', ('worked decision', APP + 'capital.html#worked-decision'),
                 '. With a $25bn goal and an 88% floor, Plans A and B are eligible.'],
                [('Preview objective changes', APP + 'capital.html#capital-explore'),
                 ' and try a 90% floor: only A remains. Previewing does not change your draft.'],
                'Preview $30bn with 90%: no plan qualifies. Return the floor to 88% and B qualifies.',
                'Choose Apply to change only the capital objective and retention floor. Plan terms and '
                'decision notes stay intact.',
                'To compare A and B, explicitly apply $25bn and 88% again, then read their allocations and '
                'the switching value.',
                ['Record a preference, its trade-off, a review trigger and what you still need to know, then '
                 'export the decision or read the ',
                 ('worked brief', APP + 'downloads/Frontier_AI_Capital_Decision.html'), '.'],
            ]),
            dict(id='section-4', heading='Limits', items=[
                'The company figures rest on illustrative assumptions and incomplete public disclosures. '
                'They are not valuations of Anthropic or OpenAI or investment advice, and the project is not '
                'affiliated with either company.',
                'Scenario counts are not probabilities, and three presets cannot show that a choice is robust.',
                'The round model keeps the proceeds as cash and leaves out fees, preferences, option pools, '
                'conversions, secondary sales and later rounds. It does not estimate how much a company '
                'needs to raise.',
                'Monte Carlo draws are equally weighted, the copula has no tail dependence, and the tornado '
                'chart varies one driver at a time.',
            ], after=[
                'Application 4.0.0 added the capital method; the financial engine (3.0.0) and the research '
                'snapshot of 18 October 2026 are unchanged.',
                'This is an independent project, and I built it with AI coding assistants.',
            ]),
        ],
        docs=[
            [('Capital method', FRONTIER + 'docs/CAPITAL_STRATEGY.md'), ' for eligibility, regret, switching '
             'values and price intervals'],
            [('Capital calculation', FRONTIER + 'public/lib/capital-strategy.js'), ' and its ',
             ('independent Python reference', FRONTIER + 'scripts/check_capital_reference.py')],
            [('API contract', FRONTIER + 'docs/API.md'), ' and the ',
             ('HTTP tests', FRONTIER + 'tests/capital-api.test.js')],
            [('Browser workflow tests', FRONTIER + 'tests/capital-browser.mjs'), ' for edits, late responses '
             'and keyboard use'],
            [('Decision record tests', FRONTIER + 'tests/capital-record.test.js'), ' and ',
             ('share link tests', FRONTIER + 'tests/capital-share.test.js')],
            [('Uncertainty method', FRONTIER + 'docs/UNCERTAINTY.md'), ' and its ',
             ('Python check', FRONTIER + 'scripts/check_uncertainty_reference.py')],
            [('Architecture', FRONTIER + 'docs/ARCHITECTURE.md'), ' and the ',
             ('verification record', FRONTIER + 'docs/VERIFICATION.md')],
            [('Worked decision PDF', APP + 'downloads/Frontier_AI_Capital_Decision.pdf'), ' and the ',
             ('dated source register', APP + 'index.html#sources')],
        ]),
    dict(
        slug='crossbook', kind='Fintech infrastructure', title='crossbook',
        hero='An order-matching engine in Rust with opening and closing call auctions, crash recovery and a '
             'market-data feed. The same commands produce the same events on Linux, macOS, Windows, in the '
             'browser and on any number of threads.',
        stack=['Rust', 'WebAssembly'],
        repo=GITHUB + 'crossbook',
        live='https://ult666666.github.io/crossbook/', live_label='Open the playground',
        image='/assets/crossbook-playground.png', image_width=1800, image_height=1125,
        alt='The crossbook playground: an order ticket, the order book with the queue at each price level, '
            'and the event log',
        caption='The playground runs the same engine compiled to WebAssembly. Every order in it is synthetic.',
        sections=[
            dict(id='section-1', heading='The problem', body=[
                'A matching engine fails quietly. A wrong queue order or an off-by-one quantity still '
                'produces trades that look plausible, and nothing crashes.',
                'So I wrote every rule down, made each command produce a fixed list of events, and had a '
                'second implementation check the first after every command.',
            ]),
            dict(id='section-2', heading='The engine', body=[
                'Orders trade by price-time priority: the best price first, then the oldest order at that '
                'price. The engine supports limit and market orders, immediate-or-cancel, fill-or-kill, '
                'post-only, cancel, modify and four self-trade prevention modes.',
                'Each side of the book keeps its price levels in a BTreeMap, and each level is a first-in, '
                'first-out queue threaded through one slab of 48-byte order nodes. A cancel is constant-time '
                'after the ID lookup. A dense price ladder would make level lookups constant-time too, but '
                'it needs a bounded price band.',
                'The engine never reads a clock or a random number generator and never iterates a hash map, '
                'so replaying the same commands gives the same events everywhere.',
            ], links=[('Design notes', CROSSBOOK + 'docs/DESIGN.md'),
                      ('Order semantics', CROSSBOOK + 'docs/SEMANTICS.md')]),
            dict(id='section-3', heading='How it is checked', body=[
                'A second, naive engine implements the same rules with linear scans. Property tests feed '
                'random command streams to both and require the same events and the same book after every '
                'command, along with structural invariants and conserved quantities.',
                'CI pins the fingerprint of a 100,000-command session on Linux, macOS and Windows, and '
                'checks that the WebAssembly build replays one million commands to the same digest.',
                'Mutation testing with cargo-mutants found untested behavior in the engine, the recovery '
                'code and the auctions. Each gap now has an assertion, and the testing notes explain the '
                'mutants that survive.',
            ], links=[('Testing approach', CROSSBOOK + 'docs/TESTING.md'),
                      ('Reference engine', CROSSBOOK + 'crates/crossbook/src/reference.rs')]),
            dict(id='section-4', heading='Recovery, market data and sharding', body=[
                'Crash recovery follows the write-ahead rule: a command is journaled before the engine '
                'applies it, and a checksummed snapshot records how much of the journal it covers. Recovery '
                'loads the newest snapshot and replays the rest, ignoring a half-written last command. A '
                'property test cuts the journal at a random byte and requires the uninterrupted run’s book '
                'and events.',
                'The market-data feed builds trades and price-level updates from events alone. Subscribers '
                'use sequence numbers and heartbeats to notice a lost message and resynchronize from a '
                'snapshot.',
                'A sequencer, worker shards and an ordered merge spread instruments across threads, and '
                'random streams must give the single-thread output for any shard count. On a four-core '
                'machine, sharding ran 2.6 to 3.4 times faster than one thread.',
            ], links=[('Recovery design', CROSSBOOK + 'docs/DESIGN.md#snapshots-and-recovery'),
                      ('Sharding design', CROSSBOOK + 'docs/DESIGN.md#many-instruments-sequencer-shards-and-merger')]),
            dict(id='call-auctions', heading='Call auctions', body=[
                'Version 0.3 adds the call auctions that exchanges use to open and close the day. During a '
                'call, limit and market orders rest without matching. Immediate-or-cancel, fill-or-kill and '
                'post-only orders are rejected, because nothing can execute yet.',
                'The uncross picks one clearing price by the rules Xetra and Euronext publish: the most '
                'executable volume, then the smallest surplus, then market pressure, then the price closest '
                'to the reference, then the lowest price. Every crossing order fills at that price in '
                'price-time priority, market orders first.',
                'A brute-force uncross that tries every price agrees with the engine on 20,000 random books, '
                'including ties at each rule. After every uncross, allocation invariants must hold, among '
                'them one price, no fill beyond a limit and an uncrossed book.',
                'The engine finds the price in one pass over cached level totals, so the indicative uncross '
                'is cheap enough to refresh after every command: about 0.34 µs on a closing book of 8,452 '
                'orders. Journal and snapshot files moved to format version 2 and still read version 1.',
            ], links=[('Auction rules and sources', CROSSBOOK + 'docs/DESIGN.md#call-auctions'),
                      ('Auction tests', CROSSBOOK + 'docs/TESTING.md#call-auctions')]),
            dict(id='section-5', heading='Results', body=[
                'On one core of a 2.1 GHz Xeon cloud VM, the engine processes 15 to 16 million commands per '
                'second. Median latency is 64 ns per command.',
                'Compiled to WebAssembly, the same session runs about half as fast under Node.js and '
                'produces the same event digest and state hash. These figures cover the matching core only, '
                'with no network, parsing or persistence on the timed path.',
            ], links=[('Benchmark method', CROSSBOOK + 'docs/BENCHMARKS.md')]),
            dict(id='section-6', heading='Limits', items=[
                'Books live in memory in one process, journals are written without fsync, and there is no '
                'network gateway or connection to a market.',
                'The clearing price is always one of the orders’ limits, while Xetra uses the reference '
                'price when it falls between two candidates. There are no volatility interruptions, and the '
                'feed does not publish the indicative price.',
                'The fast integer hasher is not resistant to hostile order IDs, so a gateway facing '
                'untrusted clients would assign IDs itself.',
                'The exchange rules are summarized from public documents and cited without section numbers.',
            ], after=['I built crossbook with AI coding assistants.']),
        ],
        docs=[
            [('Reference engine', CROSSBOOK + 'crates/crossbook/src/reference.rs'), ' and the ',
             ('differential tests', CROSSBOOK + 'crates/crossbook/tests/differential.rs'),
             ' that compare it with the fast engine'],
            [('Pinned session fingerprints', CROSSBOOK + 'crates/crossbook/tests/flow.rs'),
             ' checked on three operating systems'],
            [('Crash recovery tests', CROSSBOOK + 'crates/crossbook/tests/recovery.rs'),
             ', which cut the journal at a random byte'],
            [('Sharding tests', CROSSBOOK + 'crates/crossbook/tests/exchange.rs'),
             ' against the single-thread output'],
            [('Auction tests', CROSSBOOK + 'crates/crossbook/tests/auction.rs'), ' against a brute-force uncross'],
            [('Benchmarks', CROSSBOOK + 'docs/BENCHMARKS.md'), ' and the commands that produce them'],
            [('CI workflow', CROSSBOOK + '.github/workflows/ci.yml')],
        ]),
]


def link(label: str, url: str) -> str:
    external = ' target="_blank" rel="noopener noreferrer"' if url.startswith('https://') else ''
    return f'<a href="{e(url, quote=True)}"{external}>{e(label)}</a>'


def rich(text) -> str:
    """Render a string, or a sequence of strings and (label, url) links, as escaped HTML."""
    if isinstance(text, str):
        return e(text)
    return ''.join(e(part) if isinstance(part, str) else link(*part) for part in text)


def render_figure(figure: dict) -> str:
    return ('<figure class="case-detail-media"><a href="' + e(figure['href'], quote=True)
            + '" target="_blank" rel="noopener noreferrer"><img src="' + e(figure['image'], quote=True)
            + '" alt="' + e(figure['alt'], quote=True) + '" width="' + e(str(figure['width']), quote=True)
            + '" height="' + e(str(figure['height']), quote=True) + '" loading="lazy" decoding="async"></a>'
            + '<figcaption>' + e(figure['caption']) + '</figcaption></figure>')


def render_section(section: dict) -> str:
    heading_id = f' id="{e(section["heading_id"], quote=True)}"' if section.get('heading_id') else ''
    parts = [f'<section id="{e(section["id"], quote=True)}"><h2{heading_id}>{e(section["heading"])}</h2>']
    parts += [f'<p>{rich(text)}</p>' for text in section.get('body', [])]
    if section.get('items'):
        tag = 'ol' if section.get('ordered') else 'ul'
        parts.append(f'<{tag} class="case-list">' + ''.join(f'<li>{rich(item)}</li>' for item in section['items'])
                     + f'</{tag}>')
    parts += [f'<p>{rich(text)}</p>' for text in section.get('after', [])]
    if section.get('media'):
        parts.append(render_figure(section['media']))
    if section.get('links'):
        parts.append('<div class="case-section-links">' + ''.join(link(*item) for item in section['links']) + '</div>')
    return ''.join(parts) + '</section>'


def render_docs(case: dict) -> str:
    ident = case.get('docs_id', 'code-and-docs')
    items = ''.join(f'<li>{rich(item)}</li>' for item in case['docs'])
    return (f'<section id="{e(ident, quote=True)}" class="case-docs"><h2>Code and docs</h2>'
            f'<ul class="case-doc-list">{items}</ul></section>')


def render(case: dict) -> str:
    title, intro = e(case['title']), e(case['hero'])
    stack = ''.join(f'<span>{e(item)}</span>' for item in case['stack'])
    actions = link('Source on GitHub', case['repo']).replace('<a ', '<a class="button button-quiet" ', 1)
    if case['live']:
        actions = link(case['live_label'], case['live']).replace('<a ', '<a class="button button-primary" ', 1) + actions
    actions += ''.join(link(label, url).replace('<a ', '<a class="button button-quiet" ', 1)
                       for label, url in case.get('secondary_links', []))
    size = (' width="' + e(str(case['image_width']), quote=True) + '" height="' + e(str(case['image_height']), quote=True)
            + '"') if case.get('image_width') and case.get('image_height') else ''
    media = ('<figure class="case-hero-media"><img src="' + e(case['image'], quote=True) + '" alt="'
             + e(case['alt'], quote=True) + '"' + size + ' loading="eager"><figcaption>' + e(case['caption'])
             + '</figcaption></figure>') if case.get('image') else ''
    body_attributes = f' class="{e(case["body_class"], quote=True)}"' if case.get('body_class') else ''
    sections = [render_section(section) for section in case['sections']]
    toc = [f'<a href="#{e(section["id"], quote=True)}">{e(section["heading"])}</a>' for section in case['sections']]
    toc.append(f'<a href="#{e(case.get("docs_id", "code-and-docs"), quote=True)}">Code and docs</a>')
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light"><meta name="theme-color" content="#f6f3ec">
  <meta name="description" content="{intro}">
  <meta property="og:type" content="article"><meta property="og:title" content="{title}, a case study by Charles Dai">
  <meta property="og:description" content="{intro}">
  <link rel="canonical" href="https://ult666666.github.io/projects/{case["slug"]}.html">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="stylesheet" href="/styles.css">
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
  <div class="case-metadata">{stack}</div>
  <div class="hero-actions">{actions}</div>
  {media}
</section>
<div class="case-main container">
  <nav class="case-sidebar" aria-label="On this page"><span class="sidebar-heading">On this page</span>{''.join(toc)}</nav>
  <article class="case-article">{''.join(sections)}{render_docs(case)}
    <a class="button" href="/#work">Back to all projects</a>
  </article>
</div>
</main>
<footer class="site-footer container"><p>© 2026 Charles Dai</p><p>No cookies or tracking.</p><p class="footer-links"><a href="https://github.com/ult666666/ult666666.github.io" target="_blank" rel="noopener noreferrer">Source</a><a href="#top">Back to top</a></p></footer>
</body>
</html>
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for case in CASES:
        destination = ROOT / 'projects' / f"{case['slug']}.html"
        content = '\n'.join(line.rstrip() for line in render(case).splitlines()) + '\n'
        if args.check:
            if not destination.is_file() or destination.read_text(encoding='utf-8') != content:
                print('CASE_STUDY_OUTDATED:' + case['slug'], file=sys.stderr)
                return 1
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding='utf-8')
            print('CASE_GENERATED', destination.name)
    if args.check:
        print('CASE_STUDIES_VERIFIED', len(CASES))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
