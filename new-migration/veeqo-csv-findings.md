# Veeqo CSV Findings
_Source: `sellables_export_2715027799-...-btj8ab_original.csv` — exported Jun 5, 2026_

---

## Overview

| | Count |
|---|---|
| Total rows | 25,008 |
| Rows with SKU | 24,897 |
| Rows without SKU | 111 |
| Unique SKUs | 24,396 |

The 111 "without SKU" rows have other fields populated (title, price, etc.) but the `sku_code` field is empty. Breaking all rows into mutually exclusive buckets by SKU quality:

| SKU quality | Rows |
|---|---|
| Clean | 22,695 |
| Contains spaces | 2,156 |
| `none` / `none1`–`none30` placeholders | 42 |
| Empty (blank `sku_code`) | 111 |
| All digits (e.g. `204150`, `204200`) | 4 |
| **Total** | **25,008** |

2,313 rows have some kind of SKU quality issue. The categories are mutually exclusive — "all lowercase" is not a separate bucket, it's a subset of the spaces group.

**SKUs with spaces** — two sub-types:
- Informal descriptive names with no structure: `"cobra smoke"`, `"clutch full reader 1.0blk"`, `"Bandanna - Black"` — products entered with human-readable names instead of proper codes
- Typo'd real SKUs: e.g. `"CRE59X22DE- BKXBK-CL-100-MFS"` — a space entered after the hyphen

**`none*` placeholders** — Amazon listings created without a real SKU. The same placeholder (e.g. `none1`) is reused across different products, causing SKU collisions.

**All-digit SKUs** — `204150`, `204200`, `204250`, `204300` — likely vendor/supplier reference codes, not product SKUs.

---

## SKU Collisions

431 SKUs appear more than once, accounting for 501 extra rows:

| Duplicates per SKU | SKUs | Rows affected |
|---|---|---|
| 3 duplicates (appears 4x) | 22 | 88 |
| 2 duplicates (appears 3x) | 26 | 78 |
| 1 duplicate (appears 2x) | 383 | 766 |
| **Total** | **431** | **932** |

After cleanup, 431 SKUs remain — each appearing exactly once. The 501 extra rows (932 − 431) are removed.

Two root causes:

**1. Same SKU listed multiple times on a channel** — a SKU can be listed under different listing names on the same channel (e.g. two separate eBay listings for the same SKU). Veeqo creates a separate entry per listing, so the same SKU appears multiple times in the export. This is the dominant cause of the 431 duplicates and explains the conflicting prices (different listings may be priced differently).

**2. `none*` placeholder SKUs** — Amazon listings that were created without real SKUs have been given placeholder values (`none`, `none1`, `none2`, ..., `none30`). These placeholders are reused across different products, causing collision. 40+ rows share these SKU values across unrelated products.

---

## Price

| | Rows | % |
|---|---|---|
| Non-zero price | 24,839 | 99.8% |
| Zero price | 58 | 0.2% |
| No price | 0 | 0.0% |

- Range: $2.84 – $399.00
- Mean: $40.01
- **162 of the 431 colliding SKUs have conflicting prices** — the same SKU has a different `sales_price` value across its rows, meaning the same product is listed at different prices on different channel listings. When deduplicating, a decision is needed on which price to keep.

---

## Stock

| | Rows | % |
|---|---|---|
| Zero stock | 10,046 | 40.4% |
| Positive stock | 14,749 | 59.2% |
| **Total units on hand** | **111,805** | |

40% of rows have zero stock. This makes stock unreliable as a migration data source — many valid active products will show 0.

---

## Images

Each row has at most one `image_url` field — Veeqo stores one image per variant, no gallery.

| | Rows | % |
|---|---|---|
| Has image | 21,243 | 85.3% |
| No image | 3,654 | 14.7% |

---

## Field Coverage

| Field | Present | % |
|---|---|---|
| Description | 20,045 | 80.5% |
| Image | 21,243 | 85.3% |
| Brand | 9,129 | 36.7% |
| UPC | 5,017 | 20.2% |

Description and image coverage are reasonable. Brand and UPC are sparse — not reliable fields to depend on.

The `brand` field is free-text. Of the 9,129 rows that have it, values are inconsistent — the same brand entered multiple ways:

| Value | Count |
|---|---|
| proSPORT | 6,927 |
| Bikershades | 1,607 |
| proSPORTsunglasses | 264 |
| Biker Armour | 105 |
| bikershades | 65 |
| proSPORT sunglasses | 52 |
| Locs | 41 |
| BikerArmour | 37 |
| frame&optic | 9 |
| proSport | 8 |
| proSPORT Sunglasses | 4 |
| Loc | 3 |
| MODA | 3 |
| Locs Eyewear | 1 |
| SA106 | 1 |
| X LOOP | 1 |
| X LOOP Eyewear | 1 |

`proSPORT`, `proSPORTsunglasses`, `proSPORT sunglasses`, and `proSport` are all the same brand. Same with `Bikershades`, `bikershades`, `Biker Armour`, and `BikerArmour`. Not usable as a structured field without normalization.

---

## Variant Options

| | Rows |
|---|---|
| Has options | 22,223 |
| Empty / no options | 2,785 |
| All values null | 27 |

Keys are not normalized — `color`, `Choose Color (REQUIRED)`, `Choose Color`, `Frame Color`, `Choose Frame Color` are all the same concept entered differently depending on how the WooCommerce attribute was named. Same issue with power: `magnification_strength`, `Choose Power`, `Bifocal Power`.

Top option keys:

| Key | Rows |
|---|---|
| color | 12,550 |
| magnification_strength | 8,061 |
| Choose Color (REQUIRED) | 5,729 |
| Choose Power | 4,058 |
| Choose Transition Type | 1,369 |
| size | 1,281 |
| Choose Color | 975 |

**Non-null values are reliable.** Channel listings (Amazon, eBay, Walmart) require variant options to distinguish products — a non-null value was enforced by the channel, so it's genuine attribute data. A null value means the field wasn't required or wasn't set. A row with at least one non-null option value is likely a true variable product variant.
