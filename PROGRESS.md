# Bikershades Migration Progress

## Overview

Migrating product data from bikershades.com (WordPress/WooCommerce) into a new app/database.

**Source:** `https://bikershades.com/wp-json/wc/store/products`
**Working directory:** `/Users/anshramanath/Desktop/bikershades-migration/migration/`

---

## Current File Structure

```
bikershades-migration/
  bikershades_migration_guide.md   ← original migration guide
  PROGRESS.md                      ← this file
  migration/
    fetch_products.py              ← step 1: fetch all products
    fetch_variations.py            ← step 2: fetch all variations
    reshape_products.py            ← step 3: reshape into clean schema
    products.json                  ← raw WooCommerce backup (647 products)
    variations.json                ← per-variation data (6,064 variations)
    clean_products.json            ← reshaped output (639 products)
    images/                        ← empty, for step 4
```

---

## Steps Completed

### Step 1 — Fetch all products
**Script:** `fetch_products.py`
**Result:** `products.json` — 647 products across 7 pages (per_page=100)

### Step 2 — Fetch all variations
**Script:** `fetch_variations.py`
**Result:** `variations.json` — complete (6,064/6,064 variations, 486/486 parents)
**Total variations:** 6,064 across 486 variable products

### Step 3 — Reshape products
**Script:** `reshape_products.py`
**Result:** `clean_products.json` — 639 products (8 zero-price internal products filtered out)

Key reshape decisions applied:
- Descriptions stripped to plain text, embedded image URLs extracted into `descriptionImgs[]`
- `summary` parsed from `<li>` tags into string array, with plain text fallback
- `sale` computed from two checks: `on_sale == true AND sale_price < regular_price`
- `averageRating` normalized to float
- `categories` as flat slug array
- `attributes` as flat term slug array
- `variations` array: each entry `{ attributes: [...slugs], variation: {...full variation object} }`
- Variation `summary`, `averageRating`, `reviewCount` dropped — always empty/zero at variation level

---

## Data Analysis Findings

### Product types
| Type | Count |
|---|---|
| variable | 489 |
| simple | 157 |
| prescription | 1 |

### Key observations
- **75% of products are variable** — they have color/option attributes and variation IDs
- **Prices are strings in cents** — `"1999"` = $19.99
- **524/647 products are on sale** (~81%)
- **12 products have zero images**
- **3 products have no categories**
- **`stock_status` is null on every product** — actual stock is in `is_in_stock` (bool) and `stock_availability.text`

### Image distribution
Products range from 0 to 18 images each. Most have 2-7.

### Variations
The main products endpoint only returns variation IDs + attribute slugs — not per-variation images, price, or stock. A second pass is required to get full variation data.

Each variation has:
- `parent` — ID of the parent product
- `sku` — unique per color/option
- `images` — specific to this variation
- `prices` — can differ per variation
- `is_in_stock` / `stock_availability`
- `variation` — human-readable label e.g. `"Choose Color (REQUIRED): Blue Green Smoke"`

### Attributes / color swatches
Variable products have `attributes[].terms[]` — each term has a `name` and `slug`. These drive the color swatches shown on the live site.

---

## Scripts

### `fetch_products.py`
Paginates through the WooCommerce Store API and saves all products to `products.json`. Stops when an empty page is returned.

### `fetch_variations.py`
Fetches full variation data for every variation ID found in `products.json`. Saves results to `variations.json` keyed by parent product ID.

**Resume logic:** checkpoints after every individual variation. On restart, checks which variation IDs are already saved per parent and only fetches the missing ones — safe to crash and resume at any point.

---

## Decisions Made

- **Fetch full variation data** (rather than skip) — needed for per-color images, stock, and SKUs
- **0.3s sleep between requests** — polite to the live server, avoids rate limiting
- **Checkpoint per variation** — crash-safe, resumes exactly where it left off
- **Descriptions stripped to plain text** — both product and variation descriptions stripped of HTML. Embedded image URLs extracted separately into `descriptionImgs[]`
- **`descriptionImgs[]`** — array of image URLs extracted from description HTML. 587 products have them (990 total URLs), 4 variations have them. Must be downloaded and rehosted
- **`on_sale` computed from two checks** — `on_sale == true AND sale_price < regular_price`. Owner intent (`on_sale`) + price validation both must be true. `sale_price` can exist without the product being actively on sale (owner may have it staged for future use)
- **Sale page is manually curated** — the site's sale page is not an automatic filter of all `on_sale` products. For the new app, use the `on_sale` flag for badges/pricing; build the sale page view with whatever logic fits
- **`permalink` kept as `wpUrl`** — useful for 301 redirects from old Google-indexed URLs and for debugging by comparing against the live site
- **Drop entire currency block** — all 647 products are USD only. `currency_symbol`, `currency_code`, `currency_minor_unit`, separators, prefix/suffix are all redundant. Frontend hardcodes `$` and cents division
- **Drop `price_html`** — pre-rendered WooCommerce HTML for price display, redundant when you have raw price integers
- **Drop `tags` and `brands`** — 4/647 products have tags, 0 have brands. Effectively unused
- **Drop `srcset`, `sizes`, `thumbnail_srcset`, `thumbnail_sizes` from images** — keep only `src` (full res original) and `name`. Thumbnails/srcsets generated by CDN/storage. `alt` dropped (5% populated)
- **`attributes` as flat slug array** — all attribute term slugs kept regardless of `has_variations`. Frontend ignores what it doesn't need
- **Variations excluded from pagination by design** — WooCommerce only returns parent products via pagination to keep the catalog clean. Variations fetched separately via `/products/{id}`
- **Drop `_links` block entirely** — API metadata pointing back to old WordPress endpoints, useless post-migration
- **Keep one `productUrl`** — store `https://bikershades.com/wp-json/wc/store/products/{id}` per product as a single debug reference. Keeps DB clean while giving a direct way to inspect the original data if anything looks wrong

---

## Reshape Decisions

### Product fields
| WooCommerce field | Renamed to | Notes |
|---|---|---|
| `name` | `name` | |
| `slug` | `slug` | for URL routing, already unique |
| `sku` | `sku` | |
| `permalink` | `wpUrl` | for 301 redirects + debugging |
| `_links.self.href` | `productUrl` | single debug reference back to WooCommerce API |
| `description` | `description` | stripped to plain text |
| `description` (img tags) | `descriptionImgs[]` | extracted image URLs for download/rehost |
| `short_description` | `summary` | parse `<li>` tags into string array, plain text fallback |
| `on_sale` | `sale` | only true if `on_sale == true AND sale_price < regular_price` |
| `prices.regular_price` | `regularPriceInCents` | string → integer |
| `prices.sale_price` | `salePriceInCents` | string → integer |
| `average_rating` | `averageRating` | normalized to float, seed data for new review system |
| `review_count` | `reviewCount` | seed data for new review system |
| `is_in_stock` | `inStock` | |
| `categories[].slug` | `categories[]` | flat array of slugs only — for filtering |
| `images[].src` | `images[].src` | full res original only |
| `images[].name` | `images[].name` | |
| `attributes[].terms[].slug` | `attributes[]` | flat array of term slugs, all attributes kept regardless of `has_variations` |
| `variations` (merged with variations.json) | `variations[]` | each entry: `{ attributes: ["black-clear", "1-00"], variation: {...full variation object} }` |
| `weight` | `weight` | string → number |
| `dimensions` | `dimensions` | all strings → numbers |
| — | `weightUnit` | hardcoded `"oz"` |
| — | `dimensionUnit` | hardcoded `"in"` |

### Variation fields
| WooCommerce field | Renamed to | Notes |
|---|---|---|
| `name` | `name` | |
| `slug` | `slug` | |
| `sku` | `sku` | |
| `variation` | `variation` | human-readable combo string e.g. `"Choose Color: Black, Choose Power: 1.50"` |
| `permalink` | `wpUrl` | |
| `_links.self.href` | `productUrl` | |
| `description` | `description` | stripped to plain text |
| `description` (img tags) | `descriptionImgs[]` | extracted image URLs (only 4 variations have these) |
| `on_sale` | `sale` | same two-check logic as product |
| `prices.regular_price` | `regularPriceInCents` | string → integer |
| `prices.sale_price` | `salePriceInCents` | string → integer |
| `is_in_stock` | `inStock` | |
| `images[].src` | `images[].src` | |
| `images[].name` | `images[].name` | |
| `weight` | `weight` | string → number |
| `dimensions` | `dimensions` | all strings → numbers |
| — | `weightUnit` | hardcoded `"oz"` |
| — | `dimensionUnit` | hardcoded `"in"` |

**Dropped from variations only:** `summary` (always empty), `averageRating` (always 0), `reviewCount` (always 0), `categories`, `attributes`

### Fields to drop
`id` (new DB generates its own), `parent` (redundant — already in `productUrl`), `type` (inferable from whether `variations` is non-empty), `variation`, `price_html`, `price_range`, `tags`, `brands`, `grouped_products`, `has_options`, `is_purchasable`, `is_on_backorder` (never true across all products and variations), `low_stock_remaining` (keep stock binary), `stock_availability` (both `text` and `class`), `sold_individually`, `is_password_protected`, `extensions`, `add_to_cart`, `_links`, `formatted_weight`, `formatted_dimensions`, all currency fields, `srcset`/`sizes`/`thumbnail`/`thumbnail_srcset`/`thumbnail_sizes` from images, image `alt` (only 5% populated)

### Variations array (merged in)
Each variation stub in `products.json` looks like:
```json
{ "id": 65388, "attributes": [{ "name": "Choose Color", "value": "black-clear" }, { "name": "Choose Power", "value": "1-00" }] }
```

In the reshape, replace `id` with the full variation object from `variations.json`, and simplify `attributes` to just values (drop `name` — order matches parent attribute keys, and the variation string on the full object has names if ever needed):
```json
{
  "attributes": ["black-clear", "1-00"],
  "variation": { ...full variation object with same field cleanup as parent... }
}
```

Whether a product is variable is determined solely by whether `variations` is non-empty. `type` and `has_variations` are not used as source of truth.

**38 empty `variation` strings** — resolved by using `attributes` array from the variation stub in `products.json` as the source of truth for attribute values. No fallback parsing needed.

**9 simple products with `has_variations: true` attributes** — WooCommerce misconfiguration. Resolve naturally since they have no variations. No special handling needed.

---

## Known Issues (Priority Order)

1. ~~**Filter out zero-price products**~~ — resolved. 8 products filtered in reshape.

2. ~~**`short_description` parsing fallback**~~ — resolved. Plain text fallback implemented in `reshape_products.py`.

3. **990 description image URLs across 587 products + 4 variations** — must be downloaded and rehosted. `descriptionImgs[]` field captures all URLs.

4. **11 products with no images and no variations** — mostly resolved by zero-price filter. Check remaining after download step.

5. **56 variations with no images** — low priority. Frontend falls back to parent product images naturally.

---

## Up Next

- [x] Wait for `variations.json` to complete
- [x] Write `reshape_products.py` — normalize WooCommerce schema into clean app schema
- [ ] Write `download_images.py` — download all product/variation images locally
- [ ] Decide database schema
- [ ] Upload images to storage (Supabase / S3 / Cloudinary)
- [ ] Write import script to insert products into DB
