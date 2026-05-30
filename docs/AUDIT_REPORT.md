# Clean Products Audit Report

**Source:** `reshaped/clean_products_shape.json`
**Products:** 589 | **Variations:** 5,784

---

## Overview

| | Count |
|---|---|
| Products | 589 |
| Simple products (no variations) | 128 |
| Variable products | 461 |
| Total variations | 5,784 |
| Products on sale | 496 (84%) |
| Products with reviews | 104 (18%) |
| Price range | $5.95 – $349.00 |
| Average price | $74.12 |
| Average discount (sale products) | 23.4% |
| Largest discount | 52.0% |

---

## Critical Issues

### `product.weight = 0.0` — 2 products

These passed the weight check during reshaping (`weight is not None`) but the value is `0.0`, which is invalid for shipping.

| SKU | Name | Live URL | Variations |
|---|---|---|---|
| `PL46X10AP-BK-DRO` | Apex Polarized Rose | [link](https://bikershades.com/shop/motorcycle-sunglasses/lens-type/polarized/apex-polarized-rose/) | 0 (simple) |
| `PL46X10AP-0` | Apex Polarized | [link](https://bikershades.com/shop/motorcycle-sunglasses/lens-type/polarized/apex-polarized/) | 2 |

**Fix:** Look up the real weight for these two products and run an `UPDATE products SET weight = X WHERE sku = '...'` in Supabase SQL editor. `PL46X10AP-0` and `PL46X10AP-BK-DRO` are likely the same frame — they probably share the same weight.

---

## Informational Issues

These are not blockers. Each one is explained below.

---

### `product.summary[empty]` — 189 / 589 (32.1%)

The `summary` field is parsed from `<li>` tags in the product's short description. Empty means WooCommerce had no `short_description` set for that product.

| Group | Count |
|---|---|
| Simple products with no summary | 13 |
| Variable products with no summary | 176 |

Variable products dominating this count is expected — most variable products on bikershades.com relied on variation descriptions rather than a top-level short description. The frontend should render `summary` as a bullet list when present, and gracefully omit the section when empty.

---

### `product.attributes[empty]` — 115 / 589 (19.5%)

All 115 are **simple products** (no variations). Simple products have no color/size/option attributes by definition — there's nothing to group. Zero variable products are missing attributes. This is correct behavior.

---

### `product.dimensions.*[null]` — 42–43 / 589 (~7%)

42 products have all three dimension fields (`length`, `width`, `height`) null. These were never entered in WooCommerce — the data simply doesn't exist.

- Dimensions are informational (not used for shipping calculation — weight is)
- The frontend should hide the dimensions row rather than showing null/zero values
- Not worth fixing unless the owner wants to manually enter them

---

### `product.description[empty]` — 17 / 589 (2.9%)

17 products have no description text at all. This was the case in WooCommerce — nothing to strip. Frontend should handle an empty string gracefully.

---

### `product.descriptionImgs[empty]` — 26 / 589 (4.4%)

These products had no images embedded in their description HTML. Normal — most products don't use description images.

---

### `variation.description[empty]` — 2,538 / 5,784 (43.9%)

Nearly half of all variations have no description. This is standard WooCommerce behavior — variation descriptions are almost never filled out because merchants rely on the parent product description. The frontend should fall back to the parent product's description when a variation's is empty.

---

### `variation.dimensions.*[null]` — 192 / 5,784 (3.3%)

Same story as product dimensions — never entered in WooCommerce. These 192 belong to the 42 products that also have null dimensions at the product level.

---

### `variation.images[empty]` — 22 / 5,784 (0.4%)

All 22 imageless variations belong to exactly 2 products:

**Wiley X Ovation for Eclipse XT [SM – LG]** — 11 variations, all imageless

| SKU | Variation |
|---|---|
| `WX-OVATION-MBK-XTCLEARTOBROWNNO-MFB` | matte-black / clear-to-brown |
| `WX-OVATION-MBK-XTCLEARTOBROWNYES-MFB` | matte-black / clear-to-brown w/ anti-reflective |
| `WX-OVATION-MBK-XTCLEARTOGRAYNO-MFB` | matte-black / clear-to-gray |
| `WX-OVATION-MBK-XTCLEARTOGRAYYES-MFB` | matte-black / clear-to-gray w/ anti-reflective |
| `WX-OVATION-MBK-XTPOLCLEARTOGRAYNO-MFB` | matte-black / polarized clear-to-gray |
| `WX-OVATION-MBK-XTPOLCLEARTOGRAYYES-MFB` | matte-black / polarized clear-to-gray w/ anti-reflective |
| `WX-OVATION-MBK-XTCLEARTOGRAYFLASHBLUEMIRROR` | matte-black / clear-to-gray flash blue mirror |
| `WX-OVATION-MBK-XTCLEARTOGRAYFLASHGREENMIRROR` | matte-black / clear-to-gray flash green mirror |
| `WX-OVATION-MBK-XTCLEARTOGRAYFLASHPINKMIRROR` | matte-black / clear-to-gray flash pink mirror |
| `WX-OVATION-MBK-XTCLEARTOGRAYFLASHREDMIRROR` | matte-black / clear-to-gray flash red mirror |
| `WX-OVATION-MBK-XTCLEARTOGRAYFLASHSILVERMIRROR` | matte-black / clear-to-gray flash silver mirror |

**BikerArmour Robin for Eclipse XT [XXSM – SM]** — 11 variations, all imageless

| SKU | Variation |
|---|---|
| `GO47X11RB-BK-XTCLEARTOBROWNNO-MFB` | black / clear-to-brown |
| `GO47X11RB-BK-XTCLEARTOBROWNYES` | black / clear-to-brown w/ anti-reflective |
| `GO47X11RB-BK-XTCLEARTOGRAYNO-MFB` | black / clear-to-gray |
| `GO47X11RB-BK-XTCLEARTOGRAYYES-MFB` | black / clear-to-gray w/ anti-reflective |
| `GO47X11RB-BK-XTPOLCLEARTOGRAYNO-MFB` | black / polarized clear-to-gray |
| `GO47X11RB-BK-XTPOLCLEARTOGRAYYES-MFB` | black / polarized clear-to-gray w/ anti-reflective |
| `GO47X11RB-BK-XTCLEARTOGRAYFLASHSILVERMIRROR` | black / clear-to-gray flash silver mirror |
| `GO47X11RB-BK-XTCLEARTOGRAYFLASHBLUEMIRROR` | black / clear-to-gray flash blue mirror |
| `GO47X11RB-BK-XTCLEARTOGRAYFLASHGREENMIRROR` | black / clear-to-gray flash green mirror |
| `GO47X11RB-BK-XTCLEARTOGRAYFLASHREDMIRROR` | black / clear-to-gray flash red mirror |
| `GO47X11RB-BK-XTCLEARTOGRAYFLASHPINKMIRROR` | black / clear-to-gray flash pink mirror |

Both are **Eclipse XT** products — these are prescription/transition lens variants where the variation image was never uploaded to WooCommerce. The frontend should fall back to the parent product images. These variations are otherwise complete with full pricing, stock, and SKU data.

---

## Ratings & Reviews

| Rating | Products |
|---|---|
| 5.0 | 59 |
| 4.5 | 7 |
| 4.67 | 1 |
| 4.0 | 30 |
| 3.0 | 1 |
| 0.0 (no rating) | 491 |

- 491 / 589 products (83%) have no reviews — seeded from WooCommerce
- Max reviews on a single product: 3
- These are starting values only — a real review system will replace them over time

---

## Full Field Summary

| Field | Missing | / Total | % | Severity |
|---|---|---|---|---|
| `product.weight[zero]` | 2 | 589 | 0.3% | 🔴 Critical |
| `product.summary[empty]` | 189 | 589 | 32.1% | ⚪ Expected |
| `product.attributes[empty]` | 115 | 589 | 19.5% | ⚪ Expected (all simple products) |
| `product.dimensions.*[null]` | 42–43 | 589 | ~7% | 🟡 Low — no WooCommerce data |
| `product.descriptionImgs[empty]` | 26 | 589 | 4.4% | ⚪ Expected |
| `product.description[empty]` | 17 | 589 | 2.9% | ⚪ Expected |
| `variation.description[empty]` | 2,538 | 5,784 | 43.9% | ⚪ Expected |
| `variation.dimensions.*[null]` | 192 | 5,784 | 3.3% | 🟡 Low — inherits from parent |
| `variation.images[empty]` | 22 | 5,784 | 0.4% | 🟡 Low — 2 Eclipse XT products, use parent images |

---

## Action Items

| Priority | Item |
|---|---|
| 🔴 Fix now | Look up real weight for `PL46X10AP-0` (Apex Polarized) and `PL46X10AP-BK-DRO` (Apex Polarized Rose). Patch via SQL. |
| 🟡 Frontend | Fall back to parent product description when `variation.description` is empty |
| 🟡 Frontend | Fall back to parent product images when `variation.images` is empty |
| 🟡 Frontend | Hide dimensions row when all dimension fields are null |
| 🟡 Frontend | Gracefully omit `summary` bullet list when array is empty |
| ⚪ Later | Owner can optionally fill in missing dimensions — not blocking anything |
