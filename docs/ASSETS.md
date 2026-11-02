# Where the images come from

Every image the site publishes is listed in `public-files.json`. Project screenshots were copied from the public repository of each project, and the case studies and the home page link back to those repositories. No screenshot shows personal or account data, and no private trading source, runtime, credentials or personal financial data is included.

The social preview `assets/portfolio-og.png` is rendered from the checked-in `assets/portfolio-og.svg`. To render it again, run the browser suite with `RENDER_SOCIAL_IMAGE=1`.

## Screenshots with recorded sources

| File | Source | SHA-256 |
| --- | --- | --- |
| `assets/motionx-site.jpg` | A 1440 × 900 screenshot of the opening screen of https://madebymotionx.com/, captured on 25 October 2026 and saved as JPEG. | `a37cabcb8db5be11f6923b770a2f77592d7f2eb587cfde7296552cb81c59e7fc` |
| `assets/luma-keys-practice.png` | `docs/screenshots/practice-hands.png` from Luma Keys commit `b5d41ea8804b0cd4d3a489436536e7f7f490f2ab`, downscaled to 1440 × 900 and reduced to a 256-color palette. It shows the app's development build on a public-domain Mutopia score. | `75ec4d8632c3e0c64886b3219ca6e7ac6880edeea5eac14afee5754bcd18a326` |
| `assets/lineageguard-studio-review.png` | `assets/studio-v2-desktop.png` from LineageGuard commit `ed48eea4370d28c52f3268fadcd3b82a3632a691` (the Studio redesign), copied unchanged: a 1440 × 1404 full-page capture of the Review tab after a rename review, on synthetic data. | `e6165a633dfcc07468849da0f610e49b0bf0a31211133dcff576bba342795b45` |
| `assets/lineageguard-review-inspector.png` | `assets/review-inspector.png` from LineageGuard commit `6ed607b5c9ff6f46f2bb3214b04d040b04c02c52`, copied unchanged. It shows synthetic source data. | `53afbb9e409fc1e94e3fdf024c4ed90ba0bc9a14695a5422893c110c12efc266` |
| `assets/lineageguard-saved-comparison.png` | The Compare panel at LineageGuard commit `5d7df021056b9eaa0f913f637cdf0d455f29951d`, captured on 26 October 2026 with synthetic standard and strict reviews. | `6a4e0f2e714940e13984aed384a29d16be3145d5ca5ce6c12660b82f255e7af3` |
| `assets/frontier-ai-capital-visual-20261020.png` | Capital Strategy Studio in Frontier AI Valuation Lab, 1440 × 1271. | `db7919bc1165558535d70eb82295791e800b14885450516f0ce716ee5c34fc9d` |

The Studio, Inspector and comparison screenshots show the browser-session preview on synthetic data; no private local browser screenshot is published. The Inspector and comparison captures predate the Studio redesign, so they show the earlier dark interface.

`tests/test_lineageguard_studio.py`, `tests/test_inspector_showcase.py` and `scripts/verify_deployment.py` check the hashes and sizes of the LineageGuard and Capital Strategy screenshots, so a changed file fails the build.

## Cropping

The home page and the case studies crop the Capital Strategy and LineageGuard Studio screenshots with CSS (`aspect-ratio`, `object-fit` and `object-position`): the Capital Strategy crop shows the working interface rather than the app's own headline, and the Studio crop shows the header, the change request, the workflow and the decision. The image files themselves are unchanged, and each `<img>` keeps the file's intrinsic `width` and `height`.
