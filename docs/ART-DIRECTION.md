# Visual identity — an editorial field guide

Funding Autopilot uses an **academic field-guide / Swiss editorial design** direction. The public README is English-only. The typography and illustrations must feel authored, human, quiet and legible, not like generic AI product advertising.

## Design intent

Think **research journal, printmaking, academic monograph and mid-century data graphics**. Use off-white pages, ample negative space, unusually strong typographic hierarchy, thin rules, restrained shapes and a limited warm palette. The art should imply **notes, plans, evidence, cycles and practice**, without simulating a finished application dashboard that has not been built.

The artwork in `assets/` is hand-composed as editable, independent SVG. It includes no remote images, proprietary fonts or third-party assets. The logo is typographic; the hero contains an abstract print illustration rather than a generated photograph or mascot.

## Palette

| Role | Color | Hex |
| --- | --- | --- |
| Paper | Warm ivory | `#F5F2EA` |
| Primary ink | Deep forest / black | `#21362D` |
| Secondary ink | Moss-gray | `#657164` |
| Editorial accent | Brick red | `#B65B43` |
| Supporting accents | Olive / muted sage / ochre | `#84998A` / `#A08057` |
| Hairline rules | Warm grey | `#B5B6A9` |

Typography: **Georgia or Times serif** for expressive headlines and numbers; **Arial/Helvetica system sans** for field labels, axes and supplementary information. GitHub can render both without any font bundles.

## Asset hierarchy

- **`hero.svg`** — editorial cover: large Funding Autopilot typography, complete English readiness motto and abstract ink print. The slogan is **aspirational**, not a guarantee of funding.
- **`workflow.svg`** — six-stage system: Setup → Search → Match → Prepare → Apply → Track. A single muted highlight identifies the separate Prepare gate.
- **`yearly-roadmap.svg`** — typographic Gantt-style *relative* months M01–M12, showing parallel research and application workstreams. Never imply the displayed month blocks are actual scheme deadlines.
- **`proposal-strategies.svg`** — five-column editorial comparison of fellowship, project, consortium, innovation and impact-award argument types. Each type should lead with its distinct evaluator question, not generic grant template advice.

## Never do this

- Neon/glowing gradients, futuristic circuit-brain backgrounds, robot mascots or chat bubbles.
- A fake web app/dashboard mockup described as a screenshot of implemented functionality.
- A stock photo or a generated person's face presented as a real researcher, host or applicant.
- Invented award-success rates, live grant numbers, platform features or application deadlines in illustrations.
- CJK text in the English README or public SVG assets, unless a future separate localized release is explicitly requested.
- Remote image dependencies, third-party font files or copying another project's visual assets.

Use [tests/test_readme_assets.py](../tests/test_readme_assets.py) to sanity-check SVG XML, README links, the English-only public presentation, and absence of GitHub Actions. Visual review at realistic README/mobile widths remains necessary and cannot be replaced by static tests.
