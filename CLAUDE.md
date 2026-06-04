# Sunglass Monster Migration — Claude Context
_Last updated: 2026-06-04_

## What this is
Multi-brand WooCommerce → Supabase migration pipeline. Uses the authenticated WooCommerce admin REST API (`/wp-json/wc/v3/`) for complete product data. The active brand is selected via `BRAND` in `.env`.

## Brand config

```python
BRAND_CONFIG = {
    "prosport": {
        "slug": "prosport",
        "brand_name": "proSPORT Sunglasses",
    },
    "monster": {
        "slug": "monster",
        "brand_name": "Sunglass Monster",
    },
    "bikershades": {
        "slug": "bikershades",
        "brand_name": "BikerShades",
    },
}
```

All pipeline scripts load `BRAND` from `.env` (`BRAND=prosport`, `BRAND=monster`, or `BRAND=bikershades`), look it up in `BRAND_CONFIG`, and derive the slug from there. Fetch scripts load credentials via separate env vars (`PROSPORT_BASE_URL`, `PROSPORT_CONSUMER_KEY`, `PROSPORT_CONSUMER_SECRET`, and equivalents for monster and bikershades).

`BRAND_CONFIG` lives in `new-migration/config/__init__.py` — a shared importable module. Scripts import it with:
```python
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand
```
`load_brand()` returns `(key, config)` where `key` is the env var value and `config` has slug, brand_name, base_url, consumer_key, consumer_secret. `BASE` is the `new-migration/` root path.

## Pipeline (in order)

### Products
1. `pipeline/fetch_products.py` — fetches all products via admin REST API → `data/{slug}/fetch-products/products.json`
2. `pipeline/slim_products.py` — extracts relevant fields only → `data/{slug}/slim-products/products.json`
3. `pipeline/validate_products.py` — validates all fields per product → `data/{slug}/validate-products/products.json` + `flagged.json`

### Variations
4. `pipeline/fetch_variations.py` — fetches all variations for each validated product → `data/{slug}/fetch-variations/variations.json`
5. `pipeline/slim_variations.py` — extracts relevant fields → `data/{slug}/slim-variations/variations.json`
6. `pipeline/validate_variations.py` — validates variations → `data/{slug}/validate-variations/variations.json` + `flagged.json`

### Reshape → Import
7. `pipeline/reshape_products.py` — normalizes products: HTML stripped, prices to cents, stock merged, attributes name-cleaned, descriptionImages as `{src, name}` objects → `data/{slug}/reshape-products/`
8. `pipeline/reshape_variations.py` — normalizes variations: same conventions, `image` → `images[]` array → `data/{slug}/reshape-variations/`
9. `pipeline/create_items.py` — embeds variations into products, ownership checks, attribute expansion/prune, image dedup, min/max price → `data/{slug}/create-items/`
10. `pipeline/{brand}_categorize_items.py` — brand-specific: normalizes category names, assigns leaf paths with `{level, name, slug, sortOrder}` structure → `data/{slug}/categorize-items/`
11. `pipeline/download_items.py` — downloads all images locally (crash-safe via `download_map.json`) → `data/{slug}/download-items/`
12. `pipeline/upload_items.py` — uploads to Supabase Storage (crash-safe via `upload_map.json`)
13. `pipeline/import_items.py` — inserts into Supabase DB

### Analysis (per stage)
- `analysis/analyze_products.py` — raw product field coverage and stats
- `analysis/analyze_slim_products.py` — slim product field presence and cross-checks
- `analysis/analyze_variations.py` — raw variation field coverage, pricing, stock, image, attribute stats
- `analysis/analyze_slim_variations.py` — slim variation field presence, on_sale consistency, parent_id cross-check
- `analysis/analyze_items.py` — combined items: pricing tiers, stock distribution, image dedup, attribute spread

### QA (per stage)
- `qa/audit_*.py` / `qa/verify_*.py` — per-stage audit (counts, field stats) and verify (cross-check data vs source) scripts for: products, slim-products, variations, slim-variations, reshape-products, reshape-variations, create-items, categorize-items, download-items, upload-items, import

## Pipeline robustness improvements (added during Monster run + ProSport run-2)

- **Attribute name collision detection** — `validate_products.py` and `validate_variations.py` simulate `clean_attr_name` at validate time and flag any product/variation where two raw attribute names would map to the same cleaned name. Catches reshape-time collisions early.
- **`ATTR_OVERRIDES` dict** — in `reshape_products.py` and `reshape_variations.py`, a brand-keyed dict that maps raw WooCommerce attribute names to canonical cleaned names before the generic prefix/postfix rules run. Add a new entry for each brand that needs it.
- **`clean_attr_name` rules** — strips `for Filter` suffix, `Choose ` prefix, `Filter by ` prefix, and parentheticals like `(REQUIRED)`. Overrides checked first.
- **Variable product stock = null** — `reshape_products.py` sets `stock=null` for all variable products. Variation-level stock is the source of truth; the WooCommerce aggregate is misleading.
- **Variable product weight/dimensions = null** — `reshape_products.py` also nullifies `weight` and all three dimension fields for variable products. Same reasoning: variation-level is the source of truth.
- **All-or-nothing dimensions** — if only some of length/width/height are present in reshape, all three are nullified and an `[INFO]` line is printed. Applies to both products (simple only) and variations.
- **`sortOrder` on images** — every image object in `images[]`, `descriptionImages[]`, and variation `images[]` gets a 1-indexed `sortOrder` field set during reshape. Import reads it directly; no generation at import time.
- **`weightUnit` / `dimensionUnit` fields** — set to `null` in reshape output. Import reads them from data; no inline defaults.
- **Category `sortOrder` on every node** — `{brand}_categorize_items.py` has a `SORT_ORDER` dict (slug → int, 1-indexed, resets per parent). Every node in every category path gets its `sortOrder` stamped. Import reads `node["sortOrder"]`; no generation at import time.
- **Import as pure insertion** — no field generation or inline defaults in `import_items.py`. All values come from categorize-items output. Dead fallbacks (`.get("stock", 1)`, enumerate for sort_order, hardcoded `None` for units) removed.
- **WooCommerce slug validation** — removed `slugify(name) == slug` check; WooCommerce slugs diverge from names (apostrophes, truncation, etc.). Just check non-empty string.
- **Empty attribute options OK** — `validate_products.py` no longer flags empty `options[]` arrays; `create_items.py` fills them from variation data.
- **Base SKU consistency check** — `validate_variations.py` checks that all variations within a product share the same pre-dash SKU base (e.g. `CA541X128RT` vs `CAPL541X128RT` is a mismatch). Combo products (`CPR` prefix) are caught and flagged. Skips variations with spaces or invalid SKUs when computing bases; flags the entire product's valid variations if mismatch detected.
- **Null variation image allowed** — `validate_variations.py` allows `image: null`; only flags if an image is present but malformed. BikerShades has photochromic variations with no image set in WooCommerce.

## Key differences from old pipeline

| | Old (BikerShades) | New (multi-brand) |
|---|---|---|
| API | Store API (unauthenticated) | Admin REST API (consumer key/secret) |
| Auth | None | HTTP Basic Auth |
| Stock | Binary `is_in_stock` bool | Real `stock_quantity` int |
| Prices | Inside `prices{}` object | Top-level strings |
| Variation images | `images[]` array (max 1) | `image` singular object |
| Brand selection | Hardcoded | `BRAND` env var + config dict |
| Output path | `migration/reshaped/` etc. | `data/{slug}/reshaped/` etc. |

## Admin API response shape (variation)

- `image` — singular object `{id, src, name, alt}` — the featured image
- `gallery_image_ids` — array of media IDs for additional images (empty on ProSport)
- `regular_price`, `sale_price` — top-level strings (not inside a `prices` object)
- `on_sale` — boolean, but verify with price comparison (same rule as before)
- `stock_quantity` — integer (real quantity), `manage_stock` bool
- `stock_status` — `"instock"` / `"outofstock"` / `"onbackorder"` string
- `attributes` — `[{id, name, slug, option}]` where `option` is the term name (not slug)

## Data paths

All output scoped to `data/{brand_slug}/`:
- `data/{slug}/fetch-products/products.json` — raw API response
- `data/{slug}/slim-products/products.json` — relevant fields only
- `data/{slug}/validate-products/products.json` + `flagged.json` — passed/failed validation
- `data/{slug}/fetch-variations/variations.json` — raw variation API response
- `data/{slug}/slim-variations/variations.json` — relevant fields only
- `data/{slug}/validate-variations/variations.json` + `flagged.json` — passed/failed validation
- `data/{slug}/reshape-products/products.json` — normalized products
- `data/{slug}/reshape-variations/variations.json` — normalized variations
- `data/{slug}/create-items/items.json` + `flagged.json` — combined items
- `data/{slug}/categorize-items/items.json` — items with normalized `[[{level, name, slug}]]` category paths
- `data/{slug}/download-items/download_map.json` + `flagged.json` + `images/` — downloaded images
- `data/{slug}/upload-items/upload_map.json` — Supabase storage URLs

## Docs structure

```
docs/
  prosport/
    build-run/   ← notes from building the pipeline with ProSport
    run-1/       ← full ProSport run-1 notes + summary (old pipeline, pre-improvements)
    run-2/       ← ProSport run-2 notes (new pipeline: sort orders, null weight/dims, etc.)
  monster/
    build-run/   ← Monster migration run notes (in progress)
```

## Current state (ProSport)
- **Run 2 in progress.** Re-run with all pipeline improvements (sort orders, null weight/dims, weightUnit/dimensionUnit, import as pure insertion).
- **Complete through:** `categorize-items`. Next: `download_items.py`.
- **Products:** 169 validated → 166 items, 3 flagged (2145, 2211, 1208 — same as run-1, WooCommerce not fixed yet).
- **Variations:** 1,740 validated → 1,713 embedded.
- **Categories:** 166 items, 197 leaf assignments, 12 categories with sortOrder on every node.
- **Run-1 summary (old pipeline):** `docs/prosport/run-1/migration-complete/summary.md`

## Current state (Monster)
- **In progress.** Pipeline complete through `create_items`. Next: `monster_categorize_items.py`.
- **Products:** 277 fetched → 267 validated → 265 in create-items, 10 flagged, 2 flagged at create-items.
- **Variations:** 2,675 fetched → 2,673 validated → 2,646 embedded.
- **Flagged products (10):** 2 Lens Type collisions (Holiday Reader 29701, Dorothy Reader 29640), 5 no-SKU, 2 no-image, 1 private+SKU-space+collision (proSPORT VShield 25942).
- **Flagged create-items (2):** 10471 (Professor Multifocal Reader — variation 11143 SKU space), 6688 (Morocco Mirror — variation 7682 no price).
- **All audit + verify scripts PASSED** through create-items.
- **Pending:** Write `monster_categorize_items.py`, then download → upload → import.

## Current state (BikerShades)
- **In progress.** Pipeline complete through `create_items`. Next: `bikershades_categorize_items.py`.
- **Products:** 704 fetched → 611 validated → 553 items, 58 flagged at create-items.
- **Variations:** 5,993 fetched → 4,839 validated → 4,802 embedded.
- **Flagged validate-variations (1,154):** 49 products with base SKU mismatch (1,114 variations — polarized vs non-polarized mixed in one WC product), 22 null images (photochromic variations), 14 private status, 5 duplicate SKUs (USPS return label junk), 4 SKU spaces, 3 missing price.
- **Flagged create-items (58):** Mostly variable products with no filled variations (all their variations were excluded at validate). 2 also caught for duplicate SKU (warranty product 62556, face masks 49895).
- **Pending:** Write `bikershades_categorize_items.py`, then download → upload → import.
