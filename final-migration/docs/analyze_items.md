# Item Analysis Report

Generated from `validate-items/items.json` across all three brands after the full reshape + validation pipeline.

---

## Overview

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Fetched from WooCommerce | 171 (1,529) | 277 (2,703) | 704 (5,737) |
| Flagged at fetch | 6 | 9 | 159 |
| Flagged at create | 12 | 6 | 35 |
| Flagged at validate | 1 | 3 | 5 |
| **Total clean items** | **152 (88.9%)** | **259 (93.5%)** | **505 (71.7%)** |
| Simple | 11 | 18 | 50 |
| Variable | 141 | 241 | 455 |
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

**Simple products**

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| stock > 0 | 5 | 10 | 24 |
| stock = 0 | 6 | 8 | 25 |
| stock < 0 | 0 | 0 | 1 |

**Variations**

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| stock > 0 | 1,118 | 1,952 | 2,938 |
| stock = 0 | 406 | 737 | 2,772 |
| stock < 0 | 0 | 2 | 6 |

BikerShades has notably thinner inventory — nearly half of all variations are at 0 stock. Negative stock values are intentional: products with stock ≤ 0 will have `inStock: false` and won't be sellable until the owner reviews and updates inventory.

---

## Pricing

Aggregated across all simple product prices and variation prices.

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Total priced entries | 1,535 | 2,709 | 5,766 |
| Min | $3.95 | $3.95 | $2.99 |
| Max | $50.99 | $83.99 | $379.00 |
| Avg | $16.95 | $17.57 | $93.69 |
| $0–$5 | 6 | 13 | 15 |
| $5–$10 | 179 | 301 | 143 |
| $10–$20 | 1,131 | 1,941 | 2,932 |
| $20–$50 | 211 | 437 | 1,021 |
| $50–$100 | 8 | 17 | 33 |
| $100+ | — | — | 1,622 |

ProSPORT and Monster are tightly clustered in the $10–$20 range. BikerShades is a significantly higher price point — 1,622 entries above $100, driven by its prescription lens upgrade and multifocal options.

**Variable product price ranges** (per-product min/max/spread)

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Avg min price | $16.04 | $15.54 | $64.67 |
| Avg max price | $16.74 | $17.01 | $83.19 |
| Avg spread | $0.71 | $1.47 | $18.51 |
| Max spread | $21.00 | $75.00 | $130.00 |
| Products with spread > $0 | 17 | 51 | 260 |

ProSPORT and Monster have very tight spreads — most variable products are single-price. BikerShades has wide spreads driven by prescription and lens upgrade options stacked on the same product (up to $130 between the cheapest and most expensive variation).

---

## Images

**Product images**

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Min | 2 | 1 | 1 |
| Max | 10 | 8 | 18 |
| Avg | 3.4 | 3.2 | 4.1 |
| 1 image | — | 1 | 22 |
| 2 images | 27 | 74 | 260 |
| 3 images | 76 | 110 | 45 |
| 4–5 images | 45 | 67 | 46 |
| 6+ images | 4 | 7 | 132 |

**Description images**

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Products with description images | 136 (89.5%) | 239 (92.3%) | 487 (96.4%) |
| Avg count when present | 1.0 | 1.1 | 1.7 |

**Variation images**

| | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Variations with no image | 0 | 0 | 37 (0.6%) |

Description images are extracted from description HTML during reshape. Variations without a dedicated image inherit from the product level by design.

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
| Unique attribute names | 2 | 8 | 10 |
| Products with >1 attribute | 56 | 82 | 165 |
| Avg options per attribute | 4.4 | 4.5 | 6.2 |
| Unique options total | 218 | 368 | 508 |

Dominant attribute names across all brands are `Choose Color (REQUIRED)` and `Choose Power`. BikerShades additionally has `Choose Transition Type` (74 products) reflecting its prescription/photochromic lens range.

**Attribute name frequency (number of products)**

| Attribute name | proSPORT | Monster | BikerShades |
|---|---|---|---|
| Choose Color (REQUIRED) | — | 237 | 447 |
| Choose Power | 58 | 80 | 91 |
| Choose Color | 139 | 1 | 1 |
| Choose Transition Type | — | — | 74 |
| Qty | — | 2 | — |
| Choose Quantity | — | 1 | 1 |
| Cleaner Spray Bottle QTY | — | 1 | 1 |
| Choose Bandana Color | — | 1 | 1 |
| Color | — | 1 | — |
| Choose Frame Color (Required) | — | — | 1 |
| Choose 7 Eye Style | — | — | 1 |
| Shipping Option | — | — | 1 |

`Choose Color` and `Choose Color (REQUIRED)` are the same attribute across brands — a normalisation candidate before import.

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
