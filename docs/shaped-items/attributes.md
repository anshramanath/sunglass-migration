# Attributes — Clean Products
_Last updated: 2026-05-31_

10 attribute types across 579 clean products.

**Note:** Product attribute terms are now trimmed to only what variations actually use. Unused terms are stripped during reshape — so counts here reflect what's actually selectable on the frontend.

---

## color

**Products:** 444 | **Unique terms:** 422

The primary variation attribute — nearly every variable product. Drives color swatches on listing and product pages.

Two distinct concept types are mixed together:
- **Single colors** (e.g. `black-clear`, `blue-smoke`, `hd-copper`) — drive color swatch UI
- **Bundle combos** (e.g. `black-clear-x-black-smoke-x-black-yellow`) — multi-pair pack selections, not actual colors. These use ` x ` as a separator between the included lens colors.

**Data quality issues:**
- Several term names appear twice under different slugs due to WooCommerce capitalization inconsistency:
  - `"Black"` → `black` and `Black`
  - `"Tortoise"` → `tortoise` and `Tortoise`
  - `"Black x Black"` → `black-x-black` and `Black x Black`
  - `"Black x Tortoise"` → `black-x-tortoise` and `Black x Tortoise`
- Two terms have a `-2` suffix slug indicating a duplicate entry in WooCommerce:
  - `Silver HD` → `silver-hd-2`
  - `Gloss Black HD` → `gloss-black-hd-2`

*(420 terms — full list in `shaped_items.json`. Too large to reproduce here.)*

---

## power

**Products:** 90 | **Unique terms:** 16

Bifocal/reading lens power in diopter increments from +1.00 to +6.00, plus "No Power". Used on all bifocal and reader products.

Previously 28 terms due to WooCommerce storing the same values with two slug formats (`1-00` and `1.00`). **Resolved in reshape** — all normalized to decimal format. Term count is now 16 (down from 22) because unused power strengths are stripped per-product during attribute cleanup — each product only lists the powers that have actual variations.

---

## transition-type

**Products:** 72 | **Unique terms:** 11

Photochromic lens transition options for Eclipse XT products. All "Clear to X" variants — some include anti-reflective coating or flash mirror finishes.

`w/` in display names is intentionally preserved in slugs (e.g. `clear-to-brown-w-anti-reflective-coat`). Clean and consistent.

| Name | Slug |
|------|------|
| Clear to Brown | `clear-to-brown` |
| Clear to Brown w/ Anti Reflective Coat | `clear-to-brown-w-anti-reflective-coat` |
| Clear to Gray | `clear-to-gray` |
| Clear to Gray in Flash Blue Mirror w/ Anti Reflective Coat | `clear-to-gray-in-flash-blue-mirror-w-anti-reflective-coat` |
| Clear to Gray in Flash Green Mirror w/ Anti Reflective Coat | `clear-to-gray-in-flash-green-mirror-w-anti-reflective-coat` |
| Clear to Gray in Flash Pink Mirror w/ Anti Reflective Coat | `clear-to-gray-in-flash-pink-mirror-w-anti-reflective-coat` |
| Clear to Gray in Flash Red Mirror w/ Anti Reflective Coat | `clear-to-gray-in-flash-red-mirror-w-anti-reflective-coat` |
| Clear to Gray in Flash Silver Mirror w/ Anti Reflective Coat | `clear-to-gray-in-flash-silver-mirror-w-anti-reflective-coat` |
| Clear to Gray w/ Anti Reflective Coat | `clear-to-gray-w-anti-reflective-coat` |
| Polarized Clear to Gray | `polarized-clear-to-gray` |
| Polarized Clear to Gray w/ Anti Reflective Coat | `polarized-clear-to-gray-w-anti-reflective-coat` |

---

## frame-color

**Products:** 7 | **Unique terms:** 4

Frame color options for a small set of prescription frame products.

**Issue:** `"Matte Black"` has slug `Matte Black` — mixed case with a space, not URL-safe. Should be `matte-black`.

| Name | Slug |
|------|------|
| Black | `black` |
| Matte Black | `Matte Black` |
| Silver | `silver` |
| Tortoise | `tortoise` |

---

## size

**Products:** 4 | **Unique terms:** 2

Head size variants used on a small number of products. Overlaps conceptually with the `shop-by-head-size` categories.

| Name | Slug |
|------|------|
| Medium - Large | `medium-large` |
| Medium - XLarge | `medium-xlarge` |

---

## brand

**Products:** 1 | **Unique terms:** 1
**Product:** [Ziena Verona Dry-Eye Prescription Glasses](https://bikershades.com/shop/prescription-motorcycle-glasses/rx-brands/see-all-rx-frames/ziena-verona-dry-eye-prescription-glasses/)

Single-product attribute. Not a meaningful catalog filter.

| Name | Slug |
|------|------|
| 7Eye | `7eye` |

---

## foam-type

**Products:** 1 | **Unique terms:** 1
**Product:** [Ziena Verona Dry-Eye Prescription Glasses](https://bikershades.com/shop/prescription-motorcycle-glasses/rx-brands/see-all-rx-frames/ziena-verona-dry-eye-prescription-glasses/)

Same product as `brand`. Removable foam seal option.

| Name | Slug |
|------|------|
| Removable Foam | `removable-foam` |

---

## quantity-packs-3

**Products:** 1 | **Unique terms:** 4
**Product:** [PM 2.5 Medical Face Masks – PACK OF THREE!](https://bikershades.com/shop/accessories/safety-protection/cotton-face-mask/)

Pack quantity selector. Not a color/style attribute — it's a quantity picker.

**Issue:** Slugs are the raw name string with spaces and parentheses — not URL-safe.

| Name | Slug |
|------|------|
| 1 pack (3 masks total) | `1 pack (3 masks total)` |
| 2 packs (6 masks total) | `2 packs (6 masks total)` |
| 5 packs (15 masks total) | `5 packs (15 masks total)` |
| 10 packs (30 masks total) | `10 packs (30 masks total)` |

---

## lens-genuine-transition

**Products:** 1 | **Unique terms:** 2
**Product:** [7eye Aspen for Rx [SM – MED]](https://bikershades.com/shop/prescription-motorcycle-glasses/rx-brands/see-all-rx-frames/7eye-aspen-for-rx/)

Genuine Transitions® lens options on a single product.

**Issue:** Slugs are internal WooCommerce labels, not derived from display names (e.g. `transitions-generation-8-clear-to-gray-green-good`).

| Name | Slug |
|------|------|
| Transitions Gen8 Clear to Graphite Green | `transitions-generation-8-clear-to-gray-green-good` |
| Transitions Gen8 Clear to Grey | `transitions-generation8-clear-to-gray-good` |

---

## original-price

**Products:** 1 | **Unique terms:** 5

Single-product attribute used as a reference price on a try-before-you-buy or return-label type product. Not a selectable variation option in the traditional sense — the slug values are price strings.

**Issue:** Slugs are raw price strings, not URL-safe attribute identifiers.

*(Full term list in `shaped_items.json`.)*

---

## Issues Summary

| Attribute | Issue | Status |
|-----------|-------|--------|
| `color` | Capitalization duplicates (`black`/`Black`, `tortoise`/`Tortoise`, etc.) and `-2` suffix slugs | Open |
| `power` | Duplicate terms with two slug formats (`1-00` and `1.00`) | ✅ Resolved in reshape |
| `frame-color` | `"Matte Black"` slug is un-normalized (`Matte Black` instead of `matte-black`) | Open |
| `quantity-packs-3` | Slugs are raw name strings with spaces and parentheses | Open |
| `lens-genuine-transition` | Slugs are internal WooCommerce labels, not derived from names | Open |
