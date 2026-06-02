# create-items analysis — proSPORT Sunglasses

## Overview

- 166 items passed (150 variable, 16 simple)
- 3 flagged
- 1,713 variations embedded across 150 variable products

---

## Field presence

### Products

| Field | Present | Null/Empty |
|---|---|---|
| id, name, slug, oldLink, type, sku | 166/166 (100%) | 0 |
| description | 144/166 (86.7%) | 22 null |
| minPriceCents, maxPriceCents | 166/166 (100%) | 0 |
| salePriceCents | 16/166 (9.6%) — simple products only | 150 null |
| sale, featured, totalSales, stock | 166/166 (100%) | 0 |
| weight | 17/166 (10.2%) | 149 null |
| categories, images | 166/166 (100%) non-empty | — |
| attributes | 156/166 (94.0%) non-empty | 10 empty |
| descriptionImages | 143/166 (86.1%) non-empty | 23 empty |
| shortDescription | 32/166 (19.3%) non-empty | 134 empty |
| dimensions | always an object — all 166 have all-null inner fields | — |

### Variations

| Field | Present | Null |
|---|---|---|
| id, parent_id, name, type, oldLink, sku | 1713/1713 (100%) | 0 |
| regularPriceCents, salePriceCents, sale | 1713/1713 (100%) | 0 |
| stock, weight | 1713/1713 (100%) | 0 |
| description | 413/1713 (24.1%) | 1,300 null |
| image | 36/1713 (2.1%) | 1,677 null (deduped) |
| dimensions | always an object — all 1,713 have all-null inner fields | — |

---

## Pricing — products

**Variable (150):**
- `minPriceCents`: min=$5.95 · p25=$16.99 · median=$25.95 · p75=$29.95 · max=$67.95 · mean=$26.26
- `maxPriceCents`: min=$5.95 · p25=$16.99 · median=$25.95 · p75=$29.95 · max=$67.95 · mean=$26.71
- Flat pricing (min==max): 141 products — all variations same price
- Tiered pricing (min<max): 9 products — multifocal readers where higher powers cost more

| Product | min | max |
|---|---|---|
| proSPORT Jersey Sunglass Readers | $17.49 | $32.49 |
| proSPORT Horsepower Foam Bifocal | $24.99 | $35.99 |
| proSPORT Studio Multifocal Reader | $19.94 | $28.69 |
| proSPORT Georgetown Multifocal Reader | $19.94 | $28.69 |
| proSPORT Altitude Polarized Leather Shield | $31.95 | $39.95 |

**Simple (16):**
- `minPriceCents`: min=$5.95 · median=$25.95 · max=$31.95 · mean=$17.45

**Sale:**
- `sale=True`: 166/166 (100%) — every product is flagged on-sale in WooCommerce

---

## Pricing — variations

- `regularPriceCents`: 1713/1713 set — min=$5.95 · p25=$19.95 · median=$25.95 · p75=$27.95 · max=$67.95
- `salePriceCents`: 1713/1713 set — min=$4.95 · p25=$12.95 · median=$14.95 · p75=$16.99 · max=$50.99
- 0 inversions (no variation has salePriceCents ≥ regularPriceCents)
- All 1,713 sale=True variations have a corresponding salePriceCents

**Discount rates:**
- min=15% · p25=32% · median=41% · p75=42% · max=47% · mean=37%
- Top rates: 42% (354 vars), 43% (292 vars), 38% (221 vars), 20% (190 vars)

**Distinct `regularPriceCents` values:** 32

| Price | Variations |
|---|---|
| $25.95 | 316 |
| $15.95 | 221 |
| $27.95 | 171 |
| $21.95 | 157 |
| $29.95 | 118 |

---

## Variation count distribution

- min=2 · p25=4 · median=5 · p75=16 · max=88 · mean=11.4

| Bucket | Products |
|---|---|
| 1–5 | 83 |
| 6–10 | 15 |
| 11–20 | 27 |
| 21–50 | 24 |
| 51–100 | 1 |

**Most variations:** Jersey Sunglass Readers (88), Garnet Gradient Reader (48), Verbena Sunglass Readers (45), Cleo Bifocal (45), Gullwing Bifocal (44)

**Fewest:** 5 products with exactly 2 variations (all polarized singles)

---

## Stock

**Products:**
- stock=0: 11 · stock=1: 147 · stock>1: 8
- Total product stock units: 212

**Variations:**
- stock=0: 299/1713 (17.5%) · stock=1: 82 · stock>1: 1,332 · stock>10: 5
- Total variation stock units: 9,497
- min=0 · p25=2 · median=7 · p75=8 · max=14 · mean=5.5

**Variable products fully out of stock:** 2
- id=2632 proSPORT Navigator Rimless HD Copper
- id=2606 proSPORT Eagle Eye HD Copper

**Variable products partially out of stock:** 50

Note: `product.stock` is the WC aggregate (always 1 for managed variable products), not the sum of variation stocks. Variation stock is the source of truth — 147/150 variable products show this expected mismatch.

---

## Images

**Product images:**
- min=1 · p25=3 · median=3 · p75=4 · max=13 · mean=3.4
- Distribution: {1: 1, 2: 31, 3: 82, 4: 21, 5: 26, 6: 2, 7: 1, 10: 1, 13: 1}
- 373 unique image URLs across all products
- 0 products with no images

**Variation images:**
- 1,677/1,713 (97.9%) null — deduped against parent
- 36/1,713 (2.1%) carry a unique image
- 149/150 variable products have all variation images nulled
- 1 product (Professor Multifocal, id=2211) has 23 unique variation images — each variation has its own photo

---

## Description & short description

| State | Count |
|---|---|
| description text + descriptionImages | 143 |
| description text only | 1 |
| neither | 22 |

- All 143 products with descriptionImages have exactly 1 image (always the lens diagram from sunglassmonster.com)
- `shortDescription` (bullet list): 32/166 products — 4–7 bullets each, mean=5.6
- Variations with description: 413/1713 (24.1%)

**22 products with no content at all** — content gaps in WooCommerce, will import with null/empty fields.

---

## Categories

- 11 unique categories
- Every product has `Uncategorized` (166/166) — present alongside real categories on categorized products, and alone on the 21 uncategorized products

| Category | Products |
|---|---|
| Uncategorized | 166 |
| READERS SPECIAL FIT | 65 |
| BIFOCALS | 44 |
| POLARIZED | 36 |
| SPORT | 31 |
| FULL LENS | 23 |
| HD COPPER | 15 |
| CLEAR &amp; YELLOW | 11 |
| STREET | 10 |
| METALS &amp; AVIATORS | 6 |
| BIG &amp; TALL | 2 |

Note: `CLEAR &amp; YELLOW`, `METALS &amp; AVIATORS`, and `BIG &amp; TALL` have raw HTML entities — decoded in `recategorize_items.py`.

- Categories per product: min=1 · median=3 · max=4 · mean=2.5
- 21 products have only `Uncategorized` — assigned real categories in recategorize step

---

## Attributes — products

| Attribute | Products | Unique options | Options/product avg |
|---|---|---|---|
| Color | 147 | 208 | 3.5 |
| Power | 65 | 13 | 6.6 |
| Activity | 6 | 2 | 1.5 |
| Frame Color | 6 | 1 | 1.0 |
| Frame Styles | 6 | 4 | 1.5 |
| Gender | 6 | 2 | 2.0 |
| Lens Color | 6 | 2 | 1.0 |
| Lens Type | 6 | 2 | 1.0 |
| Material | 6 | 1 | 1.0 |

Power options: `1.00` through `4.00` in 0.25 steps (13 total)

- Attributes per product: min=0 · median=1 · max=7 · mean=1.5
- Distribution: {0: 10, 1: 88, 2: 62, 7: 6}
- 10 products with 0 attributes (simple products)
- 6 products with 7 attributes (the Activity/Frame/Lens/Gender/Material line)

## Attributes — variations

| Attribute | Variations | Unique options |
|---|---|---|
| Color | 1,663 | 208 |
| Power | 1,399 | 13 |

- Attributes per variation: min=1 · median=2 · max=2 · mean=1.8
- Distribution: {1: 364, 2: 1,349}
- 364 single-attribute variations (Color only) — regular sunglasses
- 1,349 two-attribute variations (Color + Power) — reader/bifocal products
- 0 mismatches between variation attribute names and parent attribute names

---

## SKUs

- All 166 products and 1,713 variations have a SKU (100%)
- Product SKU length: min=7 · median=11 · max=27 · mean=11.7
- Variation SKU length: min=16 · median=24 · max=33 · mean=23.8
- 0 collisions between variation SKUs and product SKUs
- 0 duplicate SKUs across all items and variations

---

## Total sales

- 88/166 products have 0 sales (53%)
- max=22 · mean=2.2 · total across all items=357

| Product | totalSales |
|---|---|
| proSPORT Hawkeye HD Bifocal | 22 |
| proSPORT Cobalt Polarized Bifocal | 22 |
| proSPORT Clutch Reader | 20 |
| proSPORT Carraway Reader | 20 |
| proSPORT Bypass Bifocal | 16 |

---

## Data quality signals

| Signal | Count | Notes |
|---|---|---|
| Products with no content anywhere | 22 | Content gaps in WooCommerce |
| Inverted sale prices (sale ≥ regular) | 0 | Clean |
| sale=True with no salePriceCents on any variation | 0 | Clean |
| Variation attribute names mismatching parent | 0 | Expansion worked correctly |
| Duplicate SKUs | 0 | Global uniqueness confirmed |
| Variation SKU colliding with product SKU | 0 | Clean |
| Variations with weight=0.0 | 36 | Real zero from WooCommerce, not missing |
