# Product Funnel — WooCommerce → create_items
_Pipeline: fetch → slim → validate → reshape → create_items_
_Updated: 2026-06-05. Veeqo gate now integrated into validate steps (no separate veeqo_items step)._

---

## Summary

| Stage | ProSport | Monster | BikerShades |
|---|---|---|---|
| Fetched (products) | 171 | 277 | 704 |
| Validated products | 169 (-2) | 267 (-10) | 611 (-93) |
| Fetched (variations) | 1,758 | 2,675 | 5,993 |
| Validated variations | 1,528 (-230) | 2,582 (-93) | 5,585 (-408) |
| **create_items passed** | **156 (-13)** | **257 (-10)** | **474 (-137)** |
| **Total lost** | **15 of 171 (9%)** | **20 of 277 (7%)** | **230 of 704 (33%)** |

---

## ProSport

### validate_products — 171 → 169 passed, 2 flagged
| Reason | Count |
|---|---|
| Draft status + no slug | 1 |
| No SKU | 1 |

### validate_variations — 1,758 → 1,528 passed, 230 flagged
| Reason | Count |
|---|---|
| Not in Veeqo | 198 |
| Model mismatch: BF2X6KT vs BF4X7KT (Kumatage) | 24 |
| Model mismatch: CA10X15CP vs CA10X16CP (Chipper) | 4 |
| Model mismatch: FLPL7X59SB vs FLPL73X31SB (Sharkbait Float) | 3 |
| Price missing | 1 |

The 198 Veeqo drops are variations that exist in WooCommerce but have no Veeqo presence — likely discontinued or never stocked. The 31 model mismatch flags span 3 products where WooCommerce mixed different frame families into one variable product.

### create_items — 169 → 156 passed, 13 flagged
11 variable products lost all their variations at validate_variations:

| Product | Reason |
|---|---|
| Sharkbait Polarized Float | All variations: model mismatch (FLPL7X59 vs FLPL73X31) |
| Chipper Aviator | All variations: model mismatch (CA10X15 vs CA10X16) |
| Kumatage Bifocal | All variations: model mismatch (BF2X6KT vs BF4X7KT) |
| Verbena Sunglass Readers | All variations: not in Veeqo |
| Bypass Bifocal | All variations: not in Veeqo |
| Gullwing Bifocal | All variations: not in Veeqo |
| Brooklyn Reader | All variations: not in Veeqo |
| Iris Bifocal | All variations: not in Veeqo |
| Cooper Polarized Bifocal | All variations: not in Veeqo |
| Eliminator Polarized Bifocal | All variations: not in Veeqo |
| Morocco Mirror | All variations: not in Veeqo |

2 additional products have partial variation loss but still pass:

| Product | Reason |
|---|---|
| Sharkbait Polarized Bifocal | Some high-power variations not in Veeqo; lower powers pass |
| Professor Multifocal Reader | 1 variation missing price; remaining 23 pass |

---

## Monster

### validate_products — 277 → 267 passed, 10 flagged
| Reason | Count |
|---|---|
| No SKU | 5 |
| Attribute name collision after cleaning | 3 |
| Not in Veeqo | 2 |
| No images | 2 |
| Private status | 1 |
| SKU contains spaces | 1 |

_(Some products flagged for multiple reasons; issue counts exceed product counts. The 2 not-in-Veeqo flags both co-occur with other failures — no new catches from the Veeqo check alone.)_

### validate_variations — 2,675 → 2,582 passed, 93 flagged
| Reason | Count |
|---|---|
| Model mismatch: 25X65 vs 29X34 | 42 |
| Model mismatch: BF2X6KT vs BF4X7KT (Kumatage) | 24 |
| Not in Veeqo | 19 |
| Model mismatch: CA10X15CP vs CA10X16CP (Chipper) | 4 |
| Model mismatch: FLPL7X59SB vs FLPL73X31SB (Sharkbait Float) | 3 |
| Price missing | 1 |

### create_items — 267 → 257 passed, 10 flagged
6 variable products lost all their variations:

| Product | Reason |
|---|---|
| Sharkbait Polarized Float | All variations: model mismatch (FLPL7X59 vs FLPL73X31) |
| Chipper Aviator | All variations: model mismatch (CA10X15 vs CA10X16) |
| Kumatage Bifocal | All variations: model mismatch (BF2X6KT vs BF4X7KT) |
| Harvard Multifocal Reader | All variations: model mismatch (multiple bases) |
| Morocco Mirror | All variations: model mismatch + missing price |
| First Lady Bifocal | All variations: model mismatch (BF4X33FL vs BF4X33FLCT) |

4 additional products have partial variation loss but still pass (some variations not in Veeqo or missing price; product survives with remaining variations).

---

## BikerShades

### validate_products — 704 → 611 passed, 93 flagged
| Reason | Count |
|---|---|
| No SKU | 60 |
| Not in Veeqo | 59 |
| No images | 57 |
| Private status | 51 |
| Price missing or zero | 10 |
| SKU contains spaces | 13 |
| Draft status | 4 |
| No slug | 4 |
| Variable with no variation IDs | 3 |
| Pending status | 2 |
| Attribute name collision | 2 |
| Wrong type (prescription) | 1 |

_(The 59 not-in-Veeqo flags all co-occur with other failures — no SKU, private status, no images, etc. No new catches from the Veeqo check alone.)_

BikerShades has many non-product WooCommerce entries: Rx services, reseller items, accessory listings, phone-order products — these drive the high no-SKU and no-image counts.

### validate_variations — 5,993 → 5,585 passed, 408 flagged
| Reason | Count |
|---|---|
| Not in Veeqo | 84 |
| Model mismatch: 79X76 + 90X23 + 90X32 (Socket/Magnum/Evolution goggle lines) | 68 |
| Model mismatch: 25X88 vs 85X11 | 48 |
| Model mismatch: 25X65 vs 29X34 | 42 |
| Model mismatch: 48X78 vs 54X600 (goggle mix) | 41 |
| Model mismatch: 0X47 vs 47X28 | 36 |
| Model mismatch: BF2X6KT vs BF4X7KT (Kumatage) | 26 |
| Name invalid | 22 |
| Model mismatch: 20X08 vs 20X8 | 21 |
| Private status | 14 |
| Model mismatch: 10X15 + 10X16 + 20X22 | 5 |
| Model mismatch: CLOTHMASKS vs PM2.5 masks (non-sunglass) | 4 |
| Model mismatch: 210X91 vs 290X91 | 4 |
| Price missing | 3 |
| Model mismatch: 73X31 vs 7X59 (Sharkbait Float) | 3 |
| Model mismatch: 60X03 vs 60X13 (Brooklyn) | 2 |

### create_items — 611 → 474 passed, 137 flagged
25 variable products lost all their variations. Key groups:

| Group | Products | Reason |
|---|---|---|
| Mixed goggle/lens lines (Socket, Magnum, Evolution, Cayman, Anaconda, Angel) | ~15 | All variations: model mismatch |
| Bifocals (First Lady, Kumatage, Bypass, Finish Line, Puma) | ~6 | All variations: model mismatch |
| Regular sunglasses (Sharkbait Float, Chipper, Brooklyn, Aruba, etc.) | ~4 | All variations: model mismatch |
| USPS return shipping labels | 3 | Non-product SKU (LABEL- prefix) |
| Try Before You Buy deposits | 6 | Non-product SKU (TRYB4UB- prefix) |
| Rx frames (7eye, Wiley X, BikerArmour, foam-pad) | ~65 | Non-product SKU (-RX / -HIGHRX token) |

Additional products with partial variation loss still pass (unreplaced variation IDs where some but not all variations were filtered).

---

## Cross-brand patterns

**Model number mismatch** is the dominant cause of variation loss across all brands — variations with different model numbers (after decoding the NNXnn encoding) that WooCommerce incorrectly grouped under one variable product. Three root causes:

- **Polarized vs non-polarized mixed into one WC product** — same frame, different lens treatment, inconsistent SKU prefix. The C-prefix rule (CPR... vs PR... = combo vs single) correctly passes those through; only genuine model differences are flagged.
- **SKU revision coexisting with original** — product was re-SKU'd but old and new variations both live in the same WC listing (Brooklyn: 60X03 vs 60X13; First Lady: BF4X33FL vs BF4X33FLCT; Morocco Mirror: CA25X095MR vs CA25X095MRMIRROR).
- **Multiple distinct models consolidated under one WC product** — most visible in BikerShades' goggle lines (Socket, Magnum, Evolution sold separately by lens type then also in a consolidated listing mixing all three) and Harvard Multifocal Reader (multiple frame styles with different bases).

**Veeqo absence.** The 198 ProSport, 19 Monster, and 84 BikerShades variations not in Veeqo are almost certainly discontinued SKUs or high-power reader/bifocal variations never stocked in Veeqo. At the product level, the same bifocal/reader pattern holds: ProSport lost 7+ products entirely (Verbena, Bypass, Gullwing, Brooklyn, Iris, Cooper, Eliminator, Morocco) because every variation was absent from Veeqo.

**BikerShades non-product tail.** A large share of BikerShades' 230-product loss comes from WooCommerce entries that are not actual products: Rx frame services (65+ listings), USPS return labels (3), Try Before You Buy deposits (6+), warranty/accessory/phone-order placeholders. These are excluded by the non-product SKU filter in create_items and drive the high flagged count at both validate_products and create_items.

---

## Veeqo gate — integration note

The Veeqo check was moved from a separate `veeqo_items.py` pipeline step into `validate_variations.py` and `validate_products.py`. All checks now run on every product/variation before anything is dropped:

- **validate_products** — simple products: `not in Veeqo` is a flag reason alongside structural checks. (Currently catches no new cases — all failing simples also fail other checks.)
- **validate_variations** — all variations: `not in Veeqo` is a flag reason. Variations flagged for any reason (including Veeqo absence) are excluded from what moves to reshape.

This means downstream stages (reshape → create_items) only process Veeqo-confirmed data and the separate veeqo_items gating step is no longer needed.

---

## BikerShades — features to build

**Try Before You Buy and Rx frame submission** are currently handled as individual WooCommerce product listings (70+ products across both programs), each manually created per frame model. These are flagged and excluded from migration. When building BikerShades, both flows should be reimplemented as first-class features:

- **Try Before You Buy** — a single configurable program page where customers select frame models and pay a deposit, rather than separate deposit products per bundle combination.
- **Send your frame for Rx** — a single submission flow where customers select their frame model and lens prescription, rather than individual `-RX` and `-HIGHRX` SKU listings per frame.
