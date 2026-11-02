# Where the images come from

Every image the site publishes is listed in `public-files.json`. Project screenshots were copied from the public repository of each project, and the case studies and the home page link back to those repositories. No screenshot shows personal or account data, and no private trading source, runtime, credentials or personal financial data is included.

The social preview `assets/portfolio-og.png` is rendered from the checked-in `assets/portfolio-og.svg`. To render it again, run the browser suite with `RENDER_SOCIAL_IMAGE=1`.

## Screenshots with recorded sources

| File | Source | SHA-256 |
| --- | --- | --- |
| `assets/motionx-site.jpg` | A 1440 × 900 screenshot of the opening screen of https://madebymotionx.com/, captured on 25 October 2026 and saved as JPEG. | `a37cabcb8db5be11f6923b770a2f77592d7f2eb587cfde7296552cb81c59e7fc` |
| `assets/luma-keys-practice.png` | `docs/screenshots/practice-hands.png` from Luma Keys commit `b5d41ea8804b0cd4d3a489436536e7f7f490f2ab`, downscaled to 1440 × 900 and reduced to a 256-color palette. It shows the app's development build on a public-domain Mutopia score. | `75ec4d8632c3e0c64886b3219ca6e7ac6880edeea5eac14afee5754bcd18a326` |
| `assets/crossbook-playground.png` | `docs/playground.png` from crossbook commit `9169d8ec1b1656186607191e247a000f80086ddc` (the plainer playground labels), copied unchanged: the browser playground at 1800 × 1125 with a synthetic book. | `c091862f109ea02d93cbd7fbce3caf548637dc429abcaf2b31aa919a716adabc` |
| `assets/lineageguard-studio-review.png` | `assets/studio-v2-desktop.png` from LineageGuard commit `ed48eea4370d28c52f3268fadcd3b82a3632a691` (the Studio redesign), copied unchanged: a 1440 × 1404 full-page capture of the Review tab after a rename review, on synthetic data. | `e6165a633dfcc07468849da0f610e49b0bf0a31211133dcff576bba342795b45` |
| `assets/lineageguard-review-inspector.png` | `assets/review-inspector.png` from LineageGuard commit `ed48eea4370d28c52f3268fadcd3b82a3632a691`, copied unchanged: the Review Inspector after checking the current synthetic review, 1272 × 793. | `9052d0781488221a976d6df4e3d189e2e4dd716066bc278d5032c8d15e902e39` |
| `assets/lineageguard-saved-comparison.png` | The Compare saved reviews panel at LineageGuard commit `ed48eea4370d28c52f3268fadcd3b82a3632a691`, captured on 2 November 2026 at a 1440 px viewport (1272 × 803) with standard and strict reviews of the synthetic `safe-add` scenario. | `5b40ae5ebcb25fbc0f69dcca03dcf05506530ed1ad13141b1e63bff930d92b61` |
| `assets/frontier-ai-capital-studio.png` | `docs/screenshots/capital-studio.png` from Frontier AI Valuation Lab commit `aab9fbf2e72987748b02144622b7f7a7cf67da96` (the plainer restyle), copied unchanged: Capital Strategy Studio with the worked example, 1440 × 1124. | `cfbec1da1e7305d6ab93f5d5cdda13f10c9352b1c1138ec38d1b32c319dbdd9d` |
| `assets/frontier-ai-ownership-limit.png` | `docs/screenshots/ownership-frontier.png` from the same commit, copied unchanged: the ownership limit panel with an assumed $250bn pre-money valuation and a 90% floor, 1023 × 511. | `2b9d5eb85493923ee2fcd0ccc0f1252517498e155773dbd166caaadd00d2ac72` |

The Studio, Inspector and comparison screenshots show the browser-session preview on synthetic data; no private local browser screenshot is published.

`tests/test_lineageguard_studio.py`, `tests/test_inspector_showcase.py` and `scripts/verify_deployment.py` check the hashes and sizes of the LineageGuard and Capital Strategy screenshots, so a changed file fails the build.

## Cropping

The home page and the case studies crop the Capital Strategy and LineageGuard Studio screenshots with CSS (`aspect-ratio`, `object-fit` and `object-position`): the Capital Strategy crop shows the working interface rather than the app's own headline, and the Studio crop shows the header, the change request, the workflow and the decision. The image files themselves are unchanged, and each `<img>` keeps the file's intrinsic `width` and `height`.
