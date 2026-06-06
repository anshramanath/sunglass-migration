# Item Analysis Report

Generated from `validate-items/items.json` across all three brands after the full reshape + validation pipeline.

---

## Overview

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Fetched from WooCommerce | 171 | 277 | 704 |
| Flagged at fetch | 6 | 9 | 159 |
| Flagged at create | 12 | 6 | 35 |
| Flagged at validate | 1 | 3 | 5 |
| **Total clean items** | **152** | **259** | **505** |
| Simple | 11 (7.2%) | 18 (6.9%) | 50 (9.9%) |
| Variable | 141 (92.8%) | 241 (93.1%) | 455 (90.1%) |
| Starting variations (post-create) | 1,529 | 2,703 | 5,737 |
| **Total clean variations** | **1,524** | **2,691** | **5,716** |

---

## Flagged Items (not in clean output)

### proSPORT (1 flagged)
- **proSPORT Morocco Mirror** — one variation (`CA25X095MRMIRROR`) has a $0.00 price in Veeqo, which pulls `minPriceCents` to $0. Likely a data entry error. Needs a price assigned before import.

### Monster (3 flagged)
- **proSPORT Morocco Mirror** — same as above (`CA25X095MRMIRROR-0` SKU variant).
- **proSPORT Rocket High Wrap Reader Sunglasses** — no product images in WooCommerce.
- **Leopard Print Hard Case** — no product images in WooCommerce.

### BikerShades (5 flagged)
- **Rx Option: $150.00 Lens Remake** — service listing: no SKU, no price, no images. Not a real product.
- **Rx Prescription PHONE order** — same as above.
- **Robin Goggle for Rx** — simple product at $0.00. Rx frame placeholder, not a sellable product.
- **Angel Rhinestones for Ladies COMBOS** — no product images.
- **Locs Impala 91025** — all 4 WooCommerce variations have empty attribute arrays; none survived reshape_2 validation filter, leaving 0 variations and no attributes.

---

## Data Quality Issues to Resolve

### Duplicate Names & Slugs
Duplicate slugs will cause a DB unique constraint violation on import.

**Monster:**
- `Vato` — two separate products with the same name and slug `vato`. One is id=25019, the other id=28701 (fetched as separate variable products). Slugs must be made unique before import.

**BikerShades:**
- `BikerArmour Angel Chrome with Rhinestones [MED - LG]` — duplicate name → duplicate slug `bikerarmour-angel-chrome-with-rhinestones-med-lg`
- `BikerArmour Barricade [MED - XLG]` — duplicate name → duplicate slug `bikerarmour-barricade-med-xlg`
- `bikerarmour-thunder-cover-over-fits-over-sm-med-frames` — slug collision from two distinct product names that slugify identically

### Attribute Name Inconsistency
On Monster and BikerShades, `Choose Color (REQUIRED)` and `Choose Color` exist as separate attribute names across different products. These will appear as distinct attributes in the DB. Should be normalised to a single name if they represent the same attribute.

---

## Stock & Availability

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Simple in stock | 45.5% | 55.6% | 48.0% |
| Variable in stock | 85.8% | 85.9% | 69.0% |
| Variations at 0 stock | 26.6% | 27.4% | 48.5% |
| Variations negative | 0 | 0.1% | 0.1% |

BikerShades has notably thinner inventory — nearly half of all variations are at 0 stock, and only 69% of variable products have any stock at all. Negative stock values are intentional: products with stock ≤ 0 will have `inStock: false` and won't be sellable until the owner reviews and updates inventory.

---

## Pricing

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Simple avg price | $12.32 | $12.77 | $32.14 |
| Variable avg min | $16.04 | $15.54 | $64.67 |
| Variable avg max | $16.74 | $17.01 | $83.19 |
| Variation avg price | $16.99 | $17.61 | $94.23 |
| Products with price spread | 17 | 51 | 260 |

BikerShades is a significantly higher price point. The large number of products with price spreads (260) reflects its lens upgrade / prescription option structure where variations carry very different prices (up to $130 spread within a single product).

ProSPORT and Monster pricing is tightly clustered — most products fall in the $10–$20 range.

---

## Images

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Products with no images | 0 | 0 | 0 |
| Avg product images | 3.4 | 3.2 | 4.1 |
| Products with description images | 89.5% | 92.3% | 96.4% |
| Variations with no image | 0 | 0 | 37 (0.6%) |

All clean products have at least one product image. Description images are present on the vast majority of products across all brands — the pipeline extracts these from the description HTML during reshape. Variations without a dedicated image inherit from the product level by design.

---

## Content (Deferred Fields)

Description and summary are not yet populated for all products. These will be filled in a later step.

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Null description | 15 (9.9%) | 13 (5.0%) | 14 (2.8%) |
| Empty summary | 118 (77.6%) | 120 (46.3%) | 184 (36.4%) |
| Missing both | 15 (9.9%) | 12 (4.6%) | 13 (2.6%) |
| Has both | 34 (22.4%) | 138 (53.3%) | 320 (63.4%) |

ProSPORT has the worst content coverage — 77.6% of products have no summary. Monster and BikerShades are better, with over half of products having both fields populated from WooCommerce.

---

## Attributes

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Products with >1 attribute | 56 | 82 | 165 |
| Avg options per attribute | 4.4 | 4.5 | 6.2 |
| Unique options total | 218 | 368 | 508 |

Dominant attribute names across all brands are `Choose Color (REQUIRED)` and `Choose Power`. BikerShades additionally has `Choose Transition Type` (74 products) reflecting its prescription/photochromic lens range.

---

## Variations

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Total | 1,524 | 2,691 | 5,716 |
| Avg per product | 10.8 | 11.2 | 12.6 |
| Min | 2 | 2 | 2 |
| Max | 88 | 88 | 92 |
| 2–5 variations | 81 products | 150 products | 182 products |
| 51+ variations | 1 product | 7 products | 8 products |

Products with 51+ variations are reader/multifocal products that combine multiple color and power options into a single variable product.
