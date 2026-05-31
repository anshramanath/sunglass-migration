# Reshaped Problems — Diagnosis
_Last updated: 2026-05-31_

564 of 647 products migrated cleanly. The remaining 83 were flagged during reshaping and split into 8 buckets. This file summarizes each bucket and points to the detailed review and treatment docs.

---

## Files in this folder

| File | What it is |
|---|---|
| `diagnosis.md` | This file — high-level summary of all 8 buckets |
| `treatment.md` | Owner-facing action doc — questions grouped by what we need |
| `zero_price_review.md` | Per-product notes for the zero-price products |
| `no_weight_review.md` | Per-product notes for the no-weight products |
| `no_image_review.md` | Per-product notes for the 3 no-image products |
| `invalid_sku_review.md` | Per-product notes for the 22 invalid-SKU products |
| `missing_attributes_review.md` | Per-product notes for the missing-attributes products |
| `duplicate_name_review.md` | Per-product notes for the 6 duplicate-name products |

---

## Bucket Summaries

### Zero Price — 10 products
**File:** `zero_price_review.md`

Products where `minPriceCents = 0` after reshape (either the WooCommerce product price was zero, or all variation prices were zero). Themes:
- **Internal artifacts** — blank placeholder pages with no SKU, image, or categories. Default exclude.
- **Rx / configurator flows** — multi-step intake forms that can't be modeled as normal fixed-price products. Need owner decision on whether to rebuild these flows.
- **Real products with missing price** — genuine catalog products where price was removed or zeroed out. Need price restored.

**Blocker:** Owner must confirm which Rx flows still exist and provide prices for the real products.

---

### No Weight — 14 products
**File:** `no_weight_review.md`

Products with `weight = null` or `weight = 0.0`. Themes:
- **Service/shipping items** — return label products, warranty plans, USPS shipping options. Not physical products; missing weight is expected. Need owner to confirm if these workflows belong on the new site.
- **Real physical products missing weight** — combo products, Eclipse XT products, accessories. Otherwise complete — just need a weight in oz from the owner.

**Blocker:** Owner confirms which service items stay, provides weights for the real products.

---

### No Image — 3 products
**File:** `no_image_review.md`

Products with an empty `images[]` array. All three need owner input:
- **Wiley X Replacement Foam Seal** — replacement part, no image in source data
- **7 Eye Replacement Eyecup** — replacement part, no image in source data
- **Angel Rhinestones for Ladies COMBOS** — real combo product, images appear to have gone stale/missing from server

**Blocker:** Owner checks if they still have assets for these.

---

### Invalid SKU — 22 products
**File:** `invalid_sku_review.md`

Products where `sku` is null or contains a space. Two distinct groups:
- **Service/workflow items with no real SKU** — Rx options, expedited shipping, try-before-you-buy, prism fee. Don't belong as normal catalog products.
- **Real physical products with dirty SKUs** — accessories where the SKU just needs cleanup (remove spaces, assign canonical value).

**Blocker:** Owner confirms which service items stay and provides clean SKUs for the real accessories.

---

### Missing Attributes — 5 products
**File:** `missing_attributes_review.md`

Products where one or more variations have a completely empty `attribute` array — the WooCommerce variation stub had no attribute values at all. The product defines colors/options but those variations carry no option data, so there is no way to connect a product attribute to a variation. Clicking a color on the frontend has nothing to resolve to.

**Blocker:** Owner checks each product's live site dropdowns and provides the correct variation options.

---

### Mismatched Attributes — 22 products

Products where variation attribute slugs don't exist in the product's attribute terms. The variation references a color or power value that was never defined at the product level — either added directly to the variation in WooCommerce without updating the product's attribute list, or the attribute term was deleted from the product but the variation was left behind.

Common examples: `red-clear`, `black-mirror-blue`, `tortoise-green-gradient-smoke`, `black-polarized-smoke` (appears across 3 related products).

**Note:** We can't auto-recover these by adding the slug to product attributes because we only have the slug, not the display name. Owner needs to either confirm the display name for the orphaned color or remove the orphaned variation.

**Blocker:** Owner reviews each flagged color slug and provides the display name, or confirms the variation should be dropped.

---

### Duplicate Name — 6 products
**File:** `duplicate_name_review.md`

Products where multiple distinct items share the exact same reshaped name. The new site requires unique product names. Two groups:
- **BikerArmour Angel Chrome with Rhinestones [MED – LG]** — 4 separate products with this name, each with a different base colorway and 13–16 variations.
- **BikerArmour Barricade [MED – XLG]** — 2 separate products, each with 7 variations.

**Blocker:** Owner decides whether to merge, rename, or split each group.

---

### Multiple Variation Images — 1 product

One product has a variation with more than 1 image — a WooCommerce misconfiguration. Variations are expected to have at most 1 image; the first is used and the rest dropped. Owner should confirm which image is correct for that variation.

---

## Status Overview

| Bucket | Count | Main blocker | Ready to act? |
|---|---|---|---|
| Zero price | 10 | Owner confirms Rx flows + provides prices | ❌ |
| No weight | 14 | Owner provides weights for real products | Partial — service items need owner first |
| No image | 3 | Owner checks for assets | ❌ |
| Invalid SKU | 22 | Owner confirms service items + provides clean SKUs | Partial — 2 safe excludes now |
| Missing attributes | 5 | Owner provides variation options from live site | ❌ |
| Mismatched attributes | 22 | Owner provides display names for orphaned color slugs | ❌ |
| Duplicate name | 6 | Owner decides merge/rename/split | ❌ |
| Multiple variation images | 1 | Owner confirms correct image | ❌ |
| **Total flagged** | **83** | | |

**Next step:** Share `treatment.md` with the owner. It has every question organized by what's needed, with live site links for each product.
