# Reshaped Problems — Diagnosis

589 of 647 products migrated cleanly. The remaining 58 were flagged during reshaping and split into 6 buckets. This file summarizes each bucket and points to the detailed review and treatment docs.

---

## Files in this folder

| File | What it is |
|---|---|
| `diagnosis.md` | This file — high-level summary of all 6 buckets |
| `treatment.md` | Owner-facing action doc — questions grouped by what we need |
| `zero_price_review.md` | Per-product notes for the 8 zero-price products |
| `no_weight_review.md` | Per-product notes for the 12 no-weight products |
| `no_image_review.md` | Per-product notes for the 3 no-image products |
| `invalid_sku_review.md` | Per-product notes for the 22 invalid-SKU products |
| `missing_attributes_review.md` | Per-product notes for the 7 missing-attributes products |
| `duplicate_name_review.md` | Per-product notes for the 6 duplicate-name products |

---

## Bucket Summaries

### Zero Price — 8 products
**File:** `zero_price_review.md`

Products with `regularPriceInCents = 0`. Themes:
- **Internal artifacts** — blank placeholder pages with no SKU, image, or categories (e.g. Distributor Invoice). Default exclude.
- **Rx / configurator flows** — multi-step intake forms that can't be modeled as normal fixed-price products (e.g. Got Your Own Frame, Wiley X Saint for Rx, Custom Prescription Lenses). Need owner decision on whether to rebuild these flows.
- **Real products with missing price** — Panther and Sahara Dark Polarized look like genuine catalog products where price was removed or zeroed out. Need price restored.

**Blocker:** Owner must confirm which Rx flows still exist and provide prices for the real products.

---

### No Weight — 12 products
**File:** `no_weight_review.md`

Products with `weight = null`. Themes:
- **Service/shipping items** — return label products, warranty plans, USPS shipping options. These aren't physical products so missing weight is expected. Need owner to confirm if these workflows belong on the new site at all.
- **Real physical products missing weight** — combo products (Dynamo, Dragster, Cobra), Eclipse XT products, and accessories (Wiley X case, strap). These are otherwise complete and ready to import — they just need a weight in oz entered by the owner.

**Blocker:** Owner confirms which service items stay, provides weights for the real products.

---

### No Image — 3 products
**File:** `no_image_review.md`

Products with an empty `images[]` array. All three need owner input before any action:
- **Wiley X Replacement Foam Seal** — replacement part, no image in source data
- **7 Eye Replacement Eyecup** — replacement part, no image in source data
- **Angel Rhinestones for Ladies COMBOS** — real combo product, images appear to have gone stale/missing from the server

**Blocker:** Owner checks if they still have assets for these. No placeholder images without explicit approval.

---

### Invalid SKU — 22 products
**File:** `invalid_sku_review.md`

Products where `sku` is null or contains a space. Two distinct groups:

- **Service/workflow items with no real SKU** — Rx options, expedited shipping, try-before-you-buy, prism fee. These items don't belong as normal catalog products. 2 are safe excludes; the rest need owner confirmation on whether the programs still exist.
- **Real physical products with dirty SKUs** — accessories like Wiley X strap, cleaning cloth, misc sunglass parts, cases, bandannas. Legitimate products where the SKU just needs cleanup (remove spaces, assign canonical value). Owner needs to confirm the correct SKU for each.

**Blocker:** Owner confirms which service items stay and provides clean SKUs for the real accessories.

---

### Missing Attributes — 7 products
**File:** `missing_attributes_review.md`

Products where some or all variations are missing option metadata (color, lens type, etc.) in both the reshaped data and the raw WooCommerce source. The missing data can't be reconstructed safely without owner input.

All 7 are real products with real variations — the attribute data is just absent from the API response:
- Magnum – Clear (36 variations)
- Locs Impala 91025 (4 variations)
- Seaway (4 variations)
- Aruba Polarized Sunglasses (10 variations)
- Taxi Polarized Bifocal (22 variations)
- Starlet Over Sized Fashion Bifocal (16 variations)
- Finish Line Bifocal (12 variations)

**Blocker:** Owner checks each product's live site dropdowns and provides the correct variation options.

---

### Duplicate Name — 6 products
**File:** `duplicate_name_review.md`

Products where multiple distinct items share the exact same reshaped name. The new site requires unique product names. Two groups:

- **BikerArmour Angel Chrome with Rhinestones [MED – LG]** — 4 separate products with this name, each with a different base colorway (HD, Yellow, Clear, Smoke) and 13–16 variations. Likely should be merged into one product or given distinct names.
- **BikerArmour Barricade [MED – XLG]** — 2 separate products with this name, each with 7 variations.

**Blocker:** Owner decides whether to merge, rename, or split each group.

---

## Status Overview

| Bucket | Count | Main blocker | Ready to act? |
|---|---|---|---|
| Zero price | 8 | Owner confirms Rx flows + provides prices | ❌ |
| No weight | 12 | Owner provides weights for real products | Partial — service items need owner first |
| No image | 3 | Owner checks for assets | ❌ |
| Invalid SKU | 22 | Owner confirms service items + provides clean SKUs | Partial — 2 safe excludes now |
| Missing attributes | 7 | Owner provides variation options from live site | ❌ |
| Duplicate name | 6 | Owner decides merge/rename/split | ❌ |

**Next step:** Share `treatment.md` with the owner. It has every question organized by what's needed, with live site links for each product.
