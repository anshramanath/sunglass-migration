# Category Link Report — Clean Products

Analysis of category assignments across ~592 approximate clean products (true count is 586 — 6 products that require variation data to filter are included here and will drop out after reshape).

---

## Product counts per category

Sorted by path. Each row is a real category assignment — a product listed under a child is not automatically counted at its parent.

| Count | Path | Display Name |
|------:|------|--------------|
| 11 | `accessories` | ACCESSORIES |
| 9 | `accessories/cases` | CASES |
| 1 | `accessories/safety-protection` | Safety & Protection |
| 3 | `accessories/tools` | TOOLS |
| 15 | `all-products` | All Products |
| 51 | `bifocal-motorcycle-glasses` | BIFOCALS |
| 3 | `bifocal-motorcycle-glasses/bifocal-type` | BIFOCAL TYPE placeholder |
| 30 | `bifocal-motorcycle-glasses/bifocals-motorcycle-sport` | Sport Bifocals |
| 41 | `bifocal-motorcycle-glasses/full-lens-reader-bifocal-type` | Full Lens Reader |
| 51 | `bifocal-motorcycle-glasses/lined-bifocals-bifocal-type` | Lined Bifocals |
| 9 | `bifocal-motorcycle-glasses/multifocal-reader` | Multifocal Reader |
| 13 | `bifocal-motorcycle-glasses/polarized-bifocals` | Polarized Bifocals |
| 43 | `motorcycle-sunglasses` | SHOP SHADES |
| 20 | `motorcycle-sunglasses/brands/7eye` | 7eye |
| 64 | `motorcycle-sunglasses/brands/bikerarmour-motorcycle-riding-glasses` | BikerArmour |
| 1 | `motorcycle-sunglasses/brands/chopper` | Chopper |
| 17 | `motorcycle-sunglasses/brands/locs` | Locs |
| 94 | `motorcycle-sunglasses/brands/prosport-sunglasses` | ProSport |
| 85 | `motorcycle-sunglasses/brands/see-all-brands` | See All |
| 17 | `motorcycle-sunglasses/brands/wiley-x-sunglasses` | Wiley X |
| 5 | `motorcycle-sunglasses/brands/xloop` | X-Loop |
| 9 | `motorcycle-sunglasses/cover-overs` | Cover Overs |
| 19 | `motorcycle-sunglasses/ladies-motorcycle-sunglasses` | LADIES |
| 1 | `motorcycle-sunglasses/ladies-motorcycle-sunglasses/rhinestones` | Rhinestones |
| 8 | `motorcycle-sunglasses/lens-type` | LENS TYPE |
| 2 | `motorcycle-sunglasses/lens-type/brown-lens-type` | Brown |
| 60 | `motorcycle-sunglasses/lens-type/clear` | Clear |
| 8 | `motorcycle-sunglasses/lens-type/computer-blue-block-lenses` | Computer Blue Block Lenses |
| 46 | `motorcycle-sunglasses/lens-type/hd-copper` | HD Copper |
| 6 | `motorcycle-sunglasses/lens-type/mirror` | Mirror |
| 10 | `motorcycle-sunglasses/lens-type/mirrored` | Mirrored |
| 54 | `motorcycle-sunglasses/lens-type/polarized` | Polarized |
| 82 | `motorcycle-sunglasses/lens-type/smoke-grey` | Smoke - Grey |
| 37 | `motorcycle-sunglasses/lens-type/yellow` | Yellow |
| 12 | `motorcycle-sunglasses/lens-type/z87-safety` | Z87 Safety |
| 15 | `motorcycle-sunglasses/motorcycle-goggles` | Motorcycle Goggles |
| 10 | `motorcycle-sunglasses/shop-by-head-size` | Shop By Head Size |
| 23 | `motorcycle-sunglasses/shop-by-head-size/large-xlarge` | Large - XLarge |
| 29 | `motorcycle-sunglasses/shop-by-head-size/long-eyelashes` | Low Nose Bridge/Long Lashes |
| 1 | `motorcycle-sunglasses/shop-by-head-size/low-nose-bridge-long-lashes-shades` | Low Nose Bridge/Long Lashes. SHADES |
| 51 | `motorcycle-sunglasses/shop-by-head-size/medium-large` | Medium - Large |
| 5 | `motorcycle-sunglasses/shop-by-head-size/one-size-fits-all` | One Size Fits All |
| 22 | `motorcycle-sunglasses/shop-by-head-size/small-medium` | Small - Medium |
| 4 | `motorcycle-sunglasses/shop-by-head-size/small-medium-shop-by-head-size` | Small -Medium |
| 9 | `motorcycle-sunglasses/shop-by-head-size/xsmall-small` | XSmall - Small |
| 92 | `prescription-motorcycle-glasses` | PRESCRIPTION |
| 15 | `prescription-motorcycle-glasses/high-power-rx` | HIGH POWER Rx |
| 3 | `prescription-motorcycle-glasses/rx-brands` | Rx BRANDS |
| 26 | `prescription-motorcycle-glasses/rx-brands/7eye-rx-prescription-motorcycle-sunglasses-frames` | 7Eye Rx Frames |
| 29 | `prescription-motorcycle-glasses/rx-brands/bikerarmour-rx-frames` | BikerArmour Rx Frames |
| 90 | `prescription-motorcycle-glasses/rx-brands/see-all-rx-frames` | See All Rx Frames |
| 34 | `prescription-motorcycle-glasses/rx-brands/wileyx-rx-frames` | WileyX Rx Frames |
| 5 | `prescription-motorcycle-glasses/ziena-dry-eye-glasses` | Ziena Dry Eye |
| 12 | `sales` | SALE |
| 10 | `see-all-combo-sets` | See All Combo Sets |
| 15 | `transitions-motorcycle-sunglasses/eclipse-photochromics-motorcycle-sunglasses/bikerarmour-eclipse-photochromic-sunglasses` | BikerArmour Eclipse |
| 7 | `transitions-motorcycle-sunglasses/transition-motorcycle-sunglasses-eclipse-xt` | Eclipse XT Transitions (Best) |
| 26 | `transitions-motorcycle-sunglasses/transition-motorcycle-sunglasses-eclipse-xt/bikerarmour-eclipse-xt` | BikerArmour – Eclipse XT |
| 19 | `transitions-motorcycle-sunglasses/transition-motorcycle-sunglasses-eclipse-xt/eclipse_xt_transition_motorcycle_sunglasses_7eye` | 7eye - Eclipse XT |
| 26 | `transitions-motorcycle-sunglasses/transition-motorcycle-sunglasses-eclipse-xt/eclipse_xt_transition_motorcycle_sunglasses_wileyx` | WileyX - Eclipse XT |
| 69 | `transitions-motorcycle-sunglasses/transition-motorcycle-sunglasses-eclipse-xt/see-all-eclipse-xt-frames` | See All Eclipse XT Frames |
| 7 | `try-before-you-buy` | TRY BEFORE YOU BUY |
| 7 | `try-before-you-buy/see-all-try-before-you-buy` | See All |

---

## Findings

### Ghost paths
Three paths appear in the URL hierarchy but have no products assigned to them directly — they are navigation containers only:

- `motorcycle-sunglasses/brands`
- `transitions-motorcycle-sunglasses`
- `transitions-motorcycle-sunglasses/eclipse-photochromics-motorcycle-sunglasses`

### Categories with no clean products
These categories exist in the data but all their products are in flagged buckets:

- `accessories/strings`
- `accessories/extra-lenses`
- `accessories/return-labels`
- `got-frames`

### Duplicate concepts
The same concept is split across two slugs in three cases:

| Concept | Slug A | Count | Slug B | Count |
|---|---|---:|---|---:|
| Mirror lens | `lens-type/mirror` | 6 | `lens-type/mirrored` | 10 |
| Small-Medium head size | `shop-by-head-size/small-medium` | 22 | `shop-by-head-size/small-medium-shop-by-head-size` | 4 |
| Low nose bridge / long lashes | `shop-by-head-size/long-eyelashes` | 29 | `shop-by-head-size/low-nose-bridge-long-lashes-shades` | 1 |

### Catch-all categories
Several categories are aggregator pages that products are explicitly assigned to in addition to their specific subcategory:

| Category | Count |
|---|---:|
| `see-all-brands` | 85 |
| `see-all-rx-frames` | 90 |
| `see-all-eclipse-xt-frames` | 69 |
| `all-products` | 15 |
| `see-all-combo-sets` | 10 |
| `see-all-try-before-you-buy` | 7 |
