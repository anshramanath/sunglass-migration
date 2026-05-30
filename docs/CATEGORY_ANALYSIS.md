# Category Analysis

68 unique categories across 647 products. Every slug maps to exactly one display name and one link — no conflicts.

---

## Site Nav Hierarchy (reversed from links)

Indentation = depth in the URL path.

```
accessories/                                    (24 products)
  cases/                                        (17)
  extra-lenses/         "Sunglass Parts"        (5)
  return-labels/                                (5)
  safety-protection/                            (3)
    face-shields-accessories/                   (1)
  strings/                                      (6)
  tools/                                        (9)

all-products/                                   (22)

bifocal-motorcycle-glasses/   "BIFOCALS"        (53)
  bifocal-type/         ← placeholder           (3)
  bifocals-motorcycle-sport/  "Sport Bifocals"  (31)
  full-lens-reader-bifocal-type/                (41)
  lined-bifocals-bifocal-type/                  (53)
  multifocal-reader/                            (9)
  polarized-bifocals/                           (13)

got-frames/                                     (2)

motorcycle-sunglasses/    "SHOP SHADES"         (46)
  brands/
    7eye/                                       (20)
    bikerarmour-motorcycle-riding-glasses/      (70)
    chopper/                                    (1)
    locs/                                       (17)
    prosport-sunglasses/                        (98)
    see-all-brands/                             (88)
    wiley-x-sunglasses/                         (20)
    xloop/                                      (5)
  cover-overs/                                  (9)
  ladies-motorcycle-sunglasses/                 (22)
    rhinestones/                                (3)
  lens-type/                                    (11)
    brown-lens-type/                            (2)
    clear/                                      (61)
    computer-blue-block-lenses/                 (8)
    hd-copper/                                  (47)
    mirror/                                     (6)
    mirrored/               ← duplicate of mirror (10)
    polarized/                                  (57)
    smoke-grey/                                 (84)
    yellow/                                     (41)
    z87-safety/                                 (14)
  motorcycle-goggles/                           (15)
  shop-by-head-size/                            (12)
    large-xlarge/                               (24)
    long-eyelashes/   "Low Nose Bridge/Long Lashes" (30)
    low-nose-bridge-long-lashes-shades/  ← duplicate (2)
    medium-large/                               (58)
    one-size-fits-all/                          (5)
    small-medium/                               (22)
    small-medium-shop-by-head-size/  ← duplicate (4)
    xsmall-small/                               (9)

prescription-motorcycle-glasses/  "PRESCRIPTION" (98)
  high-power-rx/                                (15)
  rx-brands/                                    (4)
    7eye-rx-prescription-motorcycle-sunglasses-frames/ (26)
    bikerarmour-rx-frames/                      (31)
    see-all-rx-frames/                          (94)
    wileyx-rx-frames/                           (36)
  ziena-dry-eye-glasses/                        (6)

sales/                "SALE"                    (18)

see-all-combo-sets/                             (13)

transitions-motorcycle-sunglasses/
  eclipse-photochromics-motorcycle-sunglasses/
    bikerarmour-eclipse-photochromic-sunglasses/ (15)
  transition-motorcycle-sunglasses-eclipse-xt/  (8)
    bikerarmour-eclipse-xt/                     (27)
    eclipse_xt_transition_motorcycle_sunglasses_7eye/ (19)
    eclipse_xt_transition_motorcycle_sunglasses_wileyx/ (27)
    see-all-eclipse-xt-frames/                  (70)

try-before-you-buy/                             (7)
  see-all-try-before-you-buy/                   (7)
```

---

## Full Table (slug → display name → path → count)

| Count | Slug | Display Name | Path |
|---|---|---|---|
| 24 | `accessories` | ACCESSORIES | `accessories` |
| 17 | `cases` | CASES | `accessories/cases` |
| 5 | `extra-lenses` | Sunglass Parts | `accessories/extra-lenses` |
| 5 | `return-labels` | Return Labels | `accessories/return-labels` |
| 3 | `safety-protection` | Safety & Protection | `accessories/safety-protection` |
| 1 | `face-shields-accessories` | Face Shields | `accessories/safety-protection/face-shields-accessories` |
| 6 | `strings` | STRINGS | `accessories/strings` |
| 9 | `tools` | TOOLS | `accessories/tools` |
| 22 | `all-products` | All Products | `all-products` |
| 53 | `bifocal-motorcycle-glasses` | BIFOCALS | `bifocal-motorcycle-glasses` |
| 3 | `bifocal-type` | BIFOCAL TYPE placeholder | `bifocal-motorcycle-glasses/bifocal-type` |
| 31 | `bifocals-motorcycle-sport` | Sport Bifocals | `bifocal-motorcycle-glasses/bifocals-motorcycle-sport` |
| 41 | `full-lens-reader-bifocal-type` | Full Lens Reader | `bifocal-motorcycle-glasses/full-lens-reader-bifocal-type` |
| 53 | `lined-bifocals-bifocal-type` | Lined Bifocals | `bifocal-motorcycle-glasses/lined-bifocals-bifocal-type` |
| 9 | `multifocal-reader` | Multifocal Reader | `bifocal-motorcycle-glasses/multifocal-reader` |
| 13 | `polarized-bifocals` | Polarized Bifocals | `bifocal-motorcycle-glasses/polarized-bifocals` |
| 2 | `got-frames` | GOT FRAMES | `got-frames` |
| 46 | `motorcycle-sunglasses` | SHOP SHADES | `motorcycle-sunglasses` |
| 20 | `7eye` | 7eye | `motorcycle-sunglasses/brands/7eye` |
| 70 | `bikerarmour-motorcycle-riding-glasses` | BikerArmour | `motorcycle-sunglasses/brands/bikerarmour-motorcycle-riding-glasses` |
| 1 | `chopper` | Chopper | `motorcycle-sunglasses/brands/chopper` |
| 17 | `locs` | Locs | `motorcycle-sunglasses/brands/locs` |
| 98 | `prosport-sunglasses` | ProSport | `motorcycle-sunglasses/brands/prosport-sunglasses` |
| 88 | `see-all-brands` | See All | `motorcycle-sunglasses/brands/see-all-brands` |
| 20 | `wiley-x-sunglasses` | Wiley X | `motorcycle-sunglasses/brands/wiley-x-sunglasses` |
| 5 | `xloop` | X-Loop | `motorcycle-sunglasses/brands/xloop` |
| 9 | `cover-overs` | Cover Overs | `motorcycle-sunglasses/cover-overs` |
| 22 | `ladies-motorcycle-sunglasses` | LADIES | `motorcycle-sunglasses/ladies-motorcycle-sunglasses` |
| 3 | `rhinestones` | Rhinestones | `motorcycle-sunglasses/ladies-motorcycle-sunglasses/rhinestones` |
| 11 | `lens-type` | LENS TYPE | `motorcycle-sunglasses/lens-type` |
| 2 | `brown-lens-type` | Brown | `motorcycle-sunglasses/lens-type/brown-lens-type` |
| 61 | `clear` | Clear | `motorcycle-sunglasses/lens-type/clear` |
| 8 | `computer-blue-block-lenses` | Computer Blue Block Lenses | `motorcycle-sunglasses/lens-type/computer-blue-block-lenses` |
| 47 | `hd-copper` | HD Copper | `motorcycle-sunglasses/lens-type/hd-copper` |
| 6 | `mirror` | Mirror | `motorcycle-sunglasses/lens-type/mirror` |
| 10 | `mirrored` | Mirrored | `motorcycle-sunglasses/lens-type/mirrored` |
| 57 | `polarized` | Polarized | `motorcycle-sunglasses/lens-type/polarized` |
| 84 | `smoke-grey` | Smoke - Grey | `motorcycle-sunglasses/lens-type/smoke-grey` |
| 41 | `yellow` | Yellow | `motorcycle-sunglasses/lens-type/yellow` |
| 14 | `z87-safety` | Z87 Safety | `motorcycle-sunglasses/lens-type/z87-safety` |
| 15 | `motorcycle-goggles` | Motorcycle Goggles | `motorcycle-sunglasses/motorcycle-goggles` |
| 12 | `shop-by-head-size` | Shop By Head Size | `motorcycle-sunglasses/shop-by-head-size` |
| 24 | `large-xlarge` | Large - XLarge | `motorcycle-sunglasses/shop-by-head-size/large-xlarge` |
| 30 | `long-eyelashes` | Low Nose Bridge/Long Lashes | `motorcycle-sunglasses/shop-by-head-size/long-eyelashes` |
| 2 | `low-nose-bridge-long-lashes-shades` | Low Nose Bridge/Long Lashes. SHADES | `motorcycle-sunglasses/shop-by-head-size/low-nose-bridge-long-lashes-shades` |
| 58 | `medium-large` | Medium - Large | `motorcycle-sunglasses/shop-by-head-size/medium-large` |
| 5 | `one-size-fits-all` | One Size Fits All | `motorcycle-sunglasses/shop-by-head-size/one-size-fits-all` |
| 22 | `small-medium` | Small - Medium | `motorcycle-sunglasses/shop-by-head-size/small-medium` |
| 4 | `small-medium-shop-by-head-size` | Small -Medium | `motorcycle-sunglasses/shop-by-head-size/small-medium-shop-by-head-size` |
| 9 | `xsmall-small` | XSmall - Small | `motorcycle-sunglasses/shop-by-head-size/xsmall-small` |
| 98 | `prescription-motorcycle-glasses` | PRESCRIPTION | `prescription-motorcycle-glasses` |
| 15 | `high-power-rx` | HIGH POWER Rx | `prescription-motorcycle-glasses/high-power-rx` |
| 4 | `rx-brands` | Rx BRANDS | `prescription-motorcycle-glasses/rx-brands` |
| 26 | `7eye-rx-prescription-motorcycle-sunglasses-frames` | 7Eye Rx Frames | `prescription-motorcycle-glasses/rx-brands/7eye-rx-prescription-motorcycle-sunglasses-frames` |
| 31 | `bikerarmour-rx-frames` | BikerArmour Rx Frames | `prescription-motorcycle-glasses/rx-brands/bikerarmour-rx-frames` |
| 94 | `see-all-rx-frames` | See All Rx Frames | `prescription-motorcycle-glasses/rx-brands/see-all-rx-frames` |
| 36 | `wileyx-rx-frames` | WileyX Rx Frames | `prescription-motorcycle-glasses/rx-brands/wileyx-rx-frames` |
| 6 | `ziena-dry-eye-glasses` | Ziena Dry Eye | `prescription-motorcycle-glasses/ziena-dry-eye-glasses` |
| 18 | `sales` | SALE | `sales` |
| 13 | `see-all-combo-sets` | See All Combo Sets | `see-all-combo-sets` |
| 15 | `bikerarmour-eclipse-photochromic-sunglasses` | BikerArmour Eclipse | `transitions-motorcycle-sunglasses/eclipse-photochromics-motorcycle-sunglasses/bikerarmour-eclipse-photochromic-sunglasses` |
| 8 | `transition-motorcycle-sunglasses-eclipse-xt` | Eclipse XT Transitions (Best) | `transitions-motorcycle-sunglasses/transition-motorcycle-sunglasses-eclipse-xt` |
| 27 | `bikerarmour-eclipse-xt` | BikerArmour – Eclipse XT | `transitions-motorcycle-sunglasses/transition-motorcycle-sunglasses-eclipse-xt/bikerarmour-eclipse-xt` |
| 19 | `eclipse_xt_transition_motorcycle_sunglasses_7eye` | 7eye - Eclipse XT | `transitions-motorcycle-sunglasses/transition-motorcycle-sunglasses-eclipse-xt/eclipse_xt_transition_motorcycle_sunglasses_7eye` |
| 27 | `eclipse_xt_transition_motorcycle_sunglasses_wileyx` | WileyX - Eclipse XT | `transitions-motorcycle-sunglasses/transition-motorcycle-sunglasses-eclipse-xt/eclipse_xt_transition_motorcycle_sunglasses_wileyx` |
| 70 | `see-all-eclipse-xt-frames` | See All Eclipse XT Frames | `transitions-motorcycle-sunglasses/transition-motorcycle-sunglasses-eclipse-xt/see-all-eclipse-xt-frames` |
| 7 | `try-before-you-buy` | TRY BEFORE YOU BUY | `try-before-you-buy` |
| 7 | `see-all-try-before-you-buy` | See All | `try-before-you-buy/see-all-try-before-you-buy` |

---

## Issues to Resolve

| Issue | Categories Affected |
|---|---|
| Duplicate concept | `mirror` + `mirrored` — same lens type, two slugs |
| Duplicate concept | `small-medium` + `small-medium-shop-by-head-size` — same head size, two slugs |
| Duplicate concept | `long-eyelashes` + `low-nose-bridge-long-lashes-shades` — same fit type |
| Placeholder | `bifocal-type` — only 3 products, described as "placeholder" in the name |
| Catch-alls | `all-products`, `see-all-brands`, `see-all-rx-frames`, `see-all-eclipse-xt-frames` — aggregator pages, probably not needed as nav categories |
| HTML entity | `Safety &amp; Protection` — display name has raw HTML, should be `Safety & Protection` |
| Inconsistent naming | `eclipse_xt_*` slugs use underscores, everything else uses hyphens |
| Shallow content | `chopper` — only 1 product |

---

## Key Observations

- **No slug has multiple display names** — every slug maps to exactly one name. Clean 1:1 relationship.
- **The link IS the hierarchy** — parent/child is encoded in the URL path, not in a `parent_id` column
- **Display names are the nav labels** — the `name` field is what users see (often ALL CAPS at top level, Title Case for sub-categories)
- **Slug ≠ name** — e.g. slug=`motorcycle-sunglasses` but name=`SHOP SHADES`. The slug is the URL identifier, the name is the display label.
- **Max depth is 3 levels** — e.g. `transitions/eclipse-xt/bikerarmour-eclipse-xt`
