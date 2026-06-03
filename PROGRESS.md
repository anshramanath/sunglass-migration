# Sunglass Monster Migration Progress
_Last updated: 2026-06-02_

Multi-brand WooCommerce → Supabase migration using the authenticated admin REST API.

---

## Brands

| Brand | Status |
|-------|--------|
| proSPORT Sunglasses | ✅ Complete |

---

## Decisions

- **Admin REST API over Store API** — authenticated, returns real stock quantities, complete variation data, and full price fields. Store API was used for BikerShades (old pipeline) but was lossy — variation images limited to 1, no real stock counts.
- **`BRAND` env var selects active brand** — hardcoded dict maps brand name → slug + credential env var names. Switching brands is one `.env` change.
- **Shared config module (`config/__init__.py`)** — `BRAND_CONFIG` and `load_brand()` live in `new-migration/config/__init__.py`. All 28 pipeline/analysis/qa scripts import from it via `sys.path.insert` + `from config import BASE, load_brand`. Single source of truth; adding a new brand is one dict entry.
- **Output isolated per brand slug** — all pipeline output written to `data/{slug}/` so multiple brands can coexist on disk without collision.
- **Docs isolated per run** — `docs/build-run/` for pipeline development, `docs/run-1/` for first full run. Per-stage notes, analysis, audit, and verify files at each stage.

---

## ProSport Sunglasses

**Credentials:** Confirmed working 2026-06-01.
**Products:** 171 (154 variable, 17 simple).
**Variation images:** Single `image` field only — no `gallery_image_ids` populated across any product.
**Stock:** Real `stock_quantity` integers available (`manage_stock: true` on variable products).

### Admin API shape differences to handle in reshape

| Field | Old Store API | New Admin API |
|-------|--------------|---------------|
| Prices | `prices.regular_price` | `regular_price` (top-level string) |
| Stock | `is_in_stock` bool | `stock_quantity` int + `stock_status` string — use `stock_status` as source of truth |
| Variation images | `images[]` array | `image` singular object |
| Attributes | `{name, value}` | `{id, name, slug, option}` — `option` is term name |

### Steps

**Products**
- [x] Credentials acquired and confirmed
- [x] `fetch_products.py` written and run — 171 products
- [x] `analyze_products.py` — raw field coverage, pricing quirks, category/attribute breakdown
- [x] `slim_products.py` — relevant fields extracted
- [x] `analyze_slim_products.py` — field presence, on_sale truthfulness, stock cross-checks
- [x] `validate_products.py` — 169 passed, 2 flagged (draft copy + no-SKU simple)

**Variations**
- [x] `fetch_variations.py` written and run — 1,758 variations across 153 variable products
- [x] `analyze_variations.py` — raw variation field coverage, pricing, stock, image, attributes
- [x] `slim_variations.py`
- [x] `analyze_slim_variations.py` — field presence, on_sale consistency, parent_id cross-check
- [x] `validate_variations.py` — 1,740 passed, 18 flagged (17 SKU-spaces across 2 products, 1 no-price)

**Reshape → Create Items**
- [x] `reshape_products.py` — 169 products → `reshape-products/` (descriptionImages as `{src, name}` objects)
- [x] `reshape_variations.py` — 1,740 variations → `reshape-variations/` (`image` → `images[]`)
- [x] `create_items.py` — 166 items passed, 3 flagged (unreplaced variation IDs from validate) → `create-items/`

**Categorize → Import**
- [x] `prosport_categorize_items.py` — 166 items, 197 leaf assignments, 9 leaves, 21 previously uncategorized assigned → `categorize-items/`
- [x] `download_items.py` — 411 images downloaded (0 failed) → `download-items/`
- [x] `upload_items.py` — 411 uploaded (0 failed), bucket `prosport` → `upload-items/`
- [x] `import_items.py` — 166 products, 1713 variations, 12 categories → Supabase DB

**3 flagged products (2145, 2211, 1208)** — fix SKU spaces + missing price in WooCommerce, re-fetch, re-run pipeline to add them.

**Run-1 verified identical to build-run.** All verify scripts PASSED. Two transient 503s during fetch_variations resolved on retry; `analyze_slim_products.py` stale `related_ids` field removed.

**Full run summary:** `docs/run-1/migration-complete/summary.md`
