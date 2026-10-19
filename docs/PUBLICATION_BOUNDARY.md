# Publishing a public portfolio without publishing the workspace

This is the release boundary for Charles Dai's static portfolio, not a trading-system release or an application-security certification.

## The failure worth preventing

An earlier build explicitly selected the `assets/` and `projects/` directories, then recursively copied everything inside them. Selecting a directory is not the same as reviewing every file inside it. A local note, a hidden configuration file or a newly added image would have reached the output just by being placed there.

Regression tests reproduce the problem with synthetic marker files only. They do not establish that a real secret was exposed. The repaired build refuses unexpected entries before creating the deployment directory.

## The boundary now

`public-files.json` lists the exact reviewed source paths. New assets require a deliberate inventory change in the same reviewed pull request. The root HTML, CSS, JavaScript, crawler files, images and generated case-study pages are the only source payload. The source inventory, Git metadata, dependencies, local results, tests and repository documents do not ship.

The builder checks paths and ancestors, regular-file type, link count and size. It rejects symlinks, hardlinked source files, special files, unexpected subdirectories, duplicate inventory paths and missing approved assets. It snapshots the validated bytes once, rather than rereading arbitrary workspace paths during copy. Existing deployment directories are never overwritten.

A deterministic `release-manifest.json` records the SHA-256, count and total size of the emitted files, including the generated empty `.nojekyll` file. The build reads the staged payload back and checks every listed byte, as well as extra or missing entries. The manifest does not hash itself. Identical source bytes produce identical output bytes; no machine paths, current timestamps or private operational records are embedded.

## Inspect or reproduce

- [Exact publication inventory](../public-files.json)
- [Builder and independent output verifier](../scripts/build_site.py)
- [Negative-case regression tests](../tests/test_publication_guard.py)
- [Continuous-integration workflow](../.github/workflows/portfolio.yml)
- [Published release inventory](https://ult666666.github.io/release-manifest.json)

```sh
python3 -B -m unittest discover -s tests -v
npm ci --ignore-scripts --no-audit --no-fund
npx playwright install chromium
npm run build
PORTFOLIO_TEST_ROOT=_site npm run test:browser
python3 -B scripts/build_site.py --verify _site
```

Use a fresh checkout for the build. The output directory is intentionally create-once; the build does not erase a prior release to make the check pass.

## CI and disclosure

Pull requests run the tests and build the public-only payload. Deployment is restricted to main after the verification job succeeds. Checkout credentials are not persisted; the verification job uses read-only repository permissions. The Pages deployment job receives only the specific deployment permissions it needs. Third-party action references are pinned to full commit identities. Repository settings are separate controls, not facts inferred from this file.

Report sensitive findings privately using the route in [SECURITY.md](../SECURITY.md). Do not post credentials, account details, private trading logs or unpublished source in a public issue.

## Limits

An allowlist prevents accidental inclusion, not malicious content inside an approved file. Secret scanning, content review, dependency maintenance and account security remain separate requirements. SHA-256 inventory agreement detects byte differences; it is not an independent signature and does not protect against an attacker who can change both the files and their manifest. This is a cooperative build boundary, not a claim of race-proof isolation from hostile processes with the same operating-system permissions.

The website collects no application accounts, portfolio balances or trading credentials. Linked live demos have their own implementations and boundaries. The financial examples are illustrative; the trading project remains a curated public research snapshot. Neither the website nor this release check establishes investment performance or production-trading readiness.
