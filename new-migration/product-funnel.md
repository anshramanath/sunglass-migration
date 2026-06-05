# Product Funnel — WooCommerce → create_items
_Pipeline: fetch → validate → reshape → create_items_

---

## Summary

| Stage | ProSport | Monster | BikerShades |
|---|---|---|---|
| Fetched (products) | 171 | 277 | 704 |
| Validated products | 169 (-2) | 267 (-10) | 611 (-93) |
| Fetched (variations) | 1,758 | 2,675 | 5,993 |
| Validated variations | 1,669 (-89) | 2,560 (-115) | 5,299 (-694) |
| create_items passed | 161 (-8) | 260 (-7) | 461 (-150) |
| **veeqo_items passed** | **154 (-7)** | **255 (-5)** | **458 (-3)** |
| **Total lost** | **17 of 171 (10%)** | **22 of 277 (8%)** | **246 of 704 (35%)** |

---

## ProSport

### validate_products — 171 → 169 passed, 2 flagged
| Reason | Count |
|---|---|
| Draft status + no slug | 1 |
| No SKU | 1 |

### validate_variations — 1,758 → 1,669 passed, 89 flagged
| Reason | Count |
|---|---|
| SKU base mismatch (mixed product families in one WC listing) | 72 |
| SKU contains spaces | 17 |
| Price missing | 1 |

The 72 base mismatch variations belong to products where WooCommerce grouped different frame styles (polarized vs non-polarized) into one variable product with inconsistent SKU prefixes.

### create_items — 169 → 161 passed, 8 flagged
All 8 flagged are variable products that lost every variation at validate_variations, leaving nothing to embed:

| Product | Reason |
|---|---|
| Sharkbait Polarized Float | All variations had SKU base mismatch |
| Chipper Aviator | All variations had SKU base mismatch |
| Eliminator Polarized Bifocal | All variations had SKU base mismatch |
| First Lady Bifocal | All variations had SKU base mismatch |
| Kumatage Bifocal | All variations had SKU base mismatch |
| Cooper Bifocal | All variations had SKU base mismatch |
| Morocco Mirror | All variations had SKU base mismatch |
| Professor Multifocal Reader | 1 variation had a space in SKU (remaining 23 pass) |

### veeqo_items — 161 → 154 passed, 7 flagged

| Product | Absent SKUs | Note |
|---|---|---|
| Verbena Sunglass Readers | 45/45 | Entirely absent from Veeqo |
| Bypass Bifocal | 36/36 | Entirely absent from Veeqo |
| Gullwing Bifocal | 44/44 | Entirely absent from Veeqo |
| Brooklyn Reader | 18/18 | Entirely absent from Veeqo |
| Iris Bifocal | 12/12 | Entirely absent from Veeqo |
| Cooper Polarized Bifocal | 8/8 | Entirely absent from Veeqo |
| Sharkbait Polarized Bifocal | 7/16 | Low powers present, high powers (1.25+) absent |

---

## Monster

### validate_products — 277 → 267 passed, 10 flagged
| Reason | Count |
|---|---|
| No SKU | 5 |
| Attribute name collision after cleaning | 3 |
| No images | 2 |
| Private status | 1 |
| SKU contains spaces | 1 |

_(Some products flagged for multiple reasons; issue counts exceed product counts.)_

### validate_variations — 2,675 → 2,560 passed, 115 flagged
| Reason | Count |
|---|---|
| SKU base mismatch | 114 |
| SKU contains spaces | 1 |
| Price missing | 1 |

The 114 base mismatch variations span 6 products where WooCommerce mixed variations from different actual products (different frame sizes, combo vs single, etc.).

### create_items — 267 → 260 passed, 7 flagged
All 7 flagged are variable products with no valid variations remaining:

| Product | Reason |
|---|---|
| Sharkbait Polarized Float | All variations had SKU base mismatch (FLPL7X59 vs FLPL73X31) |
| Chipper Aviator | All variations had SKU base mismatch (CA10X15 vs CA10X16) |
| Harvard Multifocal Reader | All variations had SKU base mismatch (4 distinct bases) |
| First Lady Bifocal | All variations had SKU base mismatch (BF4X33FL vs BF4X33FLCT) |
| Kumatage Bifocal | All variations had SKU base mismatch (BF2X6KT vs BF4X7KT) |
| Morocco Mirror | All variations had SKU base mismatch + 1 missing price |
| Professor Multifocal Reader | 1 variation had a space in SKU (remaining 23 pass) |

### veeqo_items — 260 → 255 passed, 5 flagged

| Product | Absent SKUs | Note |
|---|---|---|
| Verbena Sun Reader | 1/63 | Single high-power variation absent |
| Cooper Polarized Bifocal | 4/20 | High powers (2.50+) absent |
| Sharkbait Polarized Bifocal | 7/16 | High powers (1.25+) absent |
| Mysto Sunglasses | 4/4 | Entirely absent — likely discontinued, never added to Veeqo |
| Nautica Polarized Sunglasses | 3/3 | Entirely absent — likely discontinued, never added to Veeqo |

---

## BikerShades

### validate_products — 704 → 611 passed, 93 flagged
| Reason | Count |
|---|---|
| No SKU | 60 |
| No images | 57 |
| Private status | 51 |
| SKU contains spaces | 13 |
| Price missing or zero | 10 |
| Draft status | 4 |
| No slug | 4 |
| Variable with no variation IDs | 3 |
| Pending status | 2 |
| Attribute name collision | 2 |
| Wrong type (prescription) | 1 |

BikerShades has many non-product WooCommerce entries: Rx services, reseller items, accessory listings, phone order products — these drive the high no-SKU and no-image counts.

### validate_variations — 5,993 → 5,299 passed, 694 flagged
| Reason | Count |
|---|---|
| SKU base mismatch | 653 |
| Null image (photochromic variations) | 22 |
| Private status | 14 |
| Duplicate SKU (USPS return label junk) | 5 |
| SKU contains spaces | 4 |
| Price missing | 3 |

653 base mismatch variations span 49 products where polarized and non-polarized versions were grouped into the same WooCommerce variable product with inconsistent SKU prefixes. The C-prefix rule (CPR... vs PR... = combo vs single of same product) correctly passes those through; only genuine mismatches are flagged.

### create_items — 611 → 461 passed, 150 flagged
38 products lost all their variations at validate_variations and have nothing to embed. Key groups:

| Group | Products | Reason |
|---|---|---|
| BikerArmour goggle/lens lines (Socket, Magnum, Evolution, Cayman, Anaconda, Angel) | 15 | All variations had SKU base mismatch |
| BikerArmour Angel/Slider older listings | 5 | All variations had SKU base mismatch |
| Bifocals (First Lady, Kumatage, Bypass, Finish Line, Puma) | 6 | All variations had SKU base mismatch |
| Regular sunglasses (Sharkbait, Chipper, Eliminator, Brooklyn, Aruba, Rusty, Locs Impala) | 7 | All variations had SKU base mismatch |
| Harvard/Professor Multifocal, Seaway, Apex, Wiley X Boss, Taxi, Overdrive | 6 | Partial — 1–2 variations flagged; product still passes |
| USPS return shipping labels | 3 | Non-product SKU (LABEL- prefix) |
| Try Before You Buy deposits | 7 | Non-product SKU (TRYB4UB- prefix) |
| Rx frames (BikerArmour, 7eye/Ziena, Wiley X) | 94 | Non-product SKU (-RX token / HIGHRX suffix) |
| Warranty + Face Masks | 2 | Duplicate SKUs across variations |

### veeqo_items — 461 → 458 passed, 3 flagged

| Product | Absent SKUs | Note |
|---|---|---|
| Cabot Photochromic Computer Reader | 8/10 | High powers (2.50+) absent |
| Edison Photochromic Computer Reader | 8/10 | High powers (2.50+) absent |
| Hawkeye HD Bifocal | 20/26 | High powers (2.25+) absent |

---

## Cross-brand patterns

**SKU base mismatch** is the dominant cause of variation loss across all three brands — 72 variations (ProSport), 114 (Monster), 653 (BikerShades), causing 6, 6, and 36 products to lose variations respectively. Three consistent root causes:

- **Polarized vs non-polarized mixed into one WC product** — biggest bucket, especially BikerShades. Same frame, different lens treatment, inconsistent SKU prefix. Examples: `SP73X31EL` (standard) vs `SPPL73X31EL` (polarized) on Eliminator; `BF4X7KT` vs `SP2X6KT` on Kumatage.
- **SKU revision coexisting with original** — the product was re-SKU'd but old and new variations both live in the same WC listing. Examples: `BF4X33FL` vs `BF4X33FLCT` (First Lady), `CA25X095MR` vs `CA25X095MRMIRROR` (Morocco Mirror), `CA60X03BL` vs `CA60X13BL` (Brooklyn).
- **Multiple distinct models consolidated under one WC product** — most visible in BikerShades' BikerArmour goggle lines (Socket, Magnum, Evolution, Cayman, Anaconda, Angel). Each was sold separately by lens type (Clear, HD, Yellow) with its own SKU base, then also appeared in a consolidated listing mixing all three. Harvard Multifocal Reader has the same issue: two different frame styles lumped under one product with four distinct bases.

**Bifocals and readers dominate Veeqo misses.** Across all three brands there are 15 total veeqo-flagged products. 13 of 15 are bifocals or readers — the two exceptions are Mysto and Nautica (Monster), regular sunglasses that appear to be discontinued and never added to Veeqo. Within the bifocal/reader group, two sub-patterns:

- **Entire product absent** — Verbena, Bypass, Gullwing, Brooklyn (ProSport) have zero SKUs in Veeqo across any power. These products likely were never stocked in Veeqo or were discontinued before the Veeqo account was set up.
- **High-power variations missing** — Sharkbait and Cooper (ProSport + Monster), Hawkeye HD, Cabot and Edison photochromic (BikerShades) are present in Veeqo at lower powers but drop off at 2.25–3.00+. The niche high-power SKUs were never added to inventory.

**BikerShades** has a large non-product tail in WooCommerce (Rx services, warranty listings, accessories, phone-order placeholders) that accounts for most of its high validate_products loss rate.

---

## Questionable flags

**Professor Multifocal Reader — create_items (all three brands)**
Flagged for "unreplaced variation IDs" because 1 variation had a space in its SKU and was correctly excluded at validate_variations. However the product still has 23 valid variations embedded and is fully usable. The current pipeline excludes it entirely based on any flag, which causes 23 good variations × 3 brands = 69 variations to be dropped unnecessarily.

---

## Veeqo — findings

`pipeline/veeqo_items.py` is a gating pipeline step: reads `create-items/items.json`, flags items whose SKUs are absent from Veeqo, and writes `veeqo-items/items.json` (clean) + `flagged.json`. Categorize reads from `veeqo-items/`.

**Counts:** 7 ProSport, 5 Monster, and 3 BikerShades products flagged — all bifocals/readers, either entirely missing from Veeqo or missing high-power variations (2.25+).

**Why these products land here:**
- **Prices are unreliable as a gate** — Veeqo is connected to WC as a sales channel, causing 431 SKUs to appear twice (native Veeqo entry + channel-synced WC copy), 162 with conflicting prices. WooCommerce is the authoritative price source.
- **Stock is empty** in the Veeqo export — not useful as a gate.
- **SKU absence is meaningful** — if a product has no Veeqo presence at all, it has never been stocked or sold through the Veeqo-managed channel. These are the right items to flag.

**Descriptions — open question.**
Veeqo has richer marketing descriptions for ~241 products where WooCommerce only has raw dimension specs. For those products Veeqo copy is clearly better. Nearly full coverage: only 1–9 products per brand have a WC description but no Veeqo equivalent. Two decisions needed:
1. Which description is preferred when both sources have real content (they've drifted independently)?
2. For the ~241 dimension-spec-only WC products, pull Veeqo description as a pipeline enrichment step.

---

## BikerShades — features to build

**Try Before You Buy and Rx frame submission** are currently handled as individual WooCommerce product listings (100 products across both programs), each manually created per frame model. These are flagged and excluded from migration. When building BikerShades, both flows should be reimplemented as first-class features rather than individual products:

- **Try Before You Buy** — a single configurable program page where customers select frame models and pay a deposit, rather than separate deposit products per bundle combination.
- **Send your frame for Rx** — a single submission flow where customers select their frame model and lens prescription, rather than individual `-RX` and `-HIGHRX` SKU listings per frame. This also makes it easier to add new frames to the program without creating new products.
