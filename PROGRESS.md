# Sunglass Monster Migration Progress
_Last updated: 2026-06-04_

Multi-brand WooCommerce → Supabase migration using the authenticated admin REST API.

---

## Brands

| Brand | Status |
|-------|--------|
| proSPORT Sunglasses | 🔄 In progress (create-items done, categorize → download → upload → import next) |
| Sunglass Monster | 🔄 In progress (create-items done, write monster_categorize_items.py next) |
| BikerShades | 🔄 In progress (create-items done, write bikershades_categorize_items.py next) |

---

## Decisions

- **Admin REST API over Store API** — authenticated, returns real stock quantities, complete variation data, and full price fields. Store API was used for BikerShades (old pipeline) but was lossy — variation images limited to 1, no real stock counts.
- **`BRAND` env var selects active brand** — hardcoded dict maps brand name → slug + credential env var names. Switching brands is one `.env` change.
- **Shared config module (`config/__init__.py`)** — `BRAND_CONFIG` and `load_brand()` live in `new-migration/config/__init__.py`. All pipeline/analysis/qa scripts import from it via `sys.path.insert` + `from config import BASE, load_brand`. Single source of truth; adding a new brand is one dict entry.
- **Output isolated per brand slug** — all pipeline output written to `data/{slug}/` so multiple brands can coexist on disk without collision.
- **Docs isolated per brand and run** — `docs/prosport/build-run/`, `docs/prosport/run-1/`, `docs/monster/build-run/`. Per-stage notes, analysis, audit, and verify files at each stage.
- **Categorize script is brand-specific** — `{brand}_categorize_items.py` because category mapping is subjective and brand-dependent.
- **Variable product stock = null** — reshape sets `stock=null` for all variable products. WooCommerce aggregate is misleading; variation-level stock is the source of truth.
- **Variable product weight/dimensions = null** — `reshape_products.py` also nullifies `weight` and all three dimension fields for variable products. Variation-level is source of truth; WooCommerce sometimes disagrees across variations.
- **All-or-nothing dimensions** — if only some of length/width/height are present, all three are nullified with an `[INFO]` print. Applies to simple products and all variations. Doesn't block the pipeline — just surfaces data quality issues.
- **`sortOrder` on images (1-indexed)** — every image object in `images[]`, `descriptionImages[]`, and variation `images[]` carries a `sortOrder` field set during reshape. Import reads it directly — no enumerate or generated sort order at import time.
- **`weightUnit` / `dimensionUnit` as null fields** — present in reshape output (both null for now). Import reads from data, no hardcoded None in import.
- **Category `sortOrder` on every node** — `{brand}_categorize_items.py` has a flat `SORT_ORDER` dict (slug → int). Every node in every path gets its sortOrder stamped. Same slug always gets the same sort order. Import reads `node["sortOrder"]`.
- **Import as pure insertion** — no field generation or inline defaults in `import_items.py`. All values come from categorize-items output. Removed: `enumerate` for sort_order, `.get("stock", 1)`, `.get("sale", False)`, `.get("summary") or []`, `.get("totalSales", 0)`, hardcoded `None` for units.
- **`ATTR_OVERRIDES` in reshape scripts** — brand-keyed dict for raw WooCommerce attribute names that need manual remapping before generic cleaning rules run. Lives in the reshape script, not config, so brand-specific transform logic stays in transform scripts.
- **Attribute name collision detection at validate time** — `validate_products.py` and `validate_variations.py` simulate `clean_attr_name` and flag any product/variation where two attributes would collide after cleaning. Catches reshape-time issues early without touching the data.
- **WooCommerce slug validation** — just checks non-empty string; removed `slugify(name)==slug` comparison since WooCommerce slugs diverge from names.
- **Empty attribute options OK** — `validate_products.py` allows empty `options[]` arrays; `create_items.py` fills them from variation data.
- **Base SKU consistency check** — `validate_variations.py` flags variations where the pre-dash SKU base differs across a product. A leading `C` difference is allowed (combo vs single). Catches polarized/non-polarized mixing, SKU revisions coexisting with originals, and consolidated multi-model WC listings.
- **Non-product SKU filtering** — `create_items.py` has `JUNK_SKU_PREFIXES`, `JUNK_SKU_SUFFIXES`, and `JUNK_SKU_CONTAINS` dicts per brand. BikerShades: flags `LABEL-` (shipping labels), `TRYB4UB-` (Try Before You Buy deposits), `-RX` token (Rx frame listings).
- **Veeqo as QA-only** — `qa/veeqo_items.py` reports which create-items SKUs are absent from Veeqo. Informational only; no output files; does not gate the pipeline. WooCommerce feeds Veeqo as a channel — Veeqo is downstream and unreliable as a source of truth.
- **Null variation image allowed** — `validate_variations.py` allows `image: null`; only flags if an image is present but malformed (no src, bad URL, empty name).
- **Variable product SKU kept as-is from WooCommerce** — WooCommerce appends `-0` (or similar suffix) to variable product SKUs specifically to prevent duplicates when two products share the same variation base. Deriving the parent SKU from common variation segments strips this and collapses distinct products into the same SKU. Keep WC product SKU unchanged.

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

**Full run summary:** `docs/prosport/run-1/migration-complete/summary.md`

### Run 2 (pipeline improvements applied)

Re-run from scratch with: null weight/dims for variable products, all-or-nothing dims, sortOrder on all images, weightUnit/dimensionUnit fields, category sortOrder on every node, import as pure insertion.

**Products**
- [x] `fetch_products.py` — 171 products (same source)
- [x] `slim_products.py`
- [x] `validate_products.py` — 169 passed, 2 flagged (same)
- [x] `analyze_*.py` scripts

**Variations**
- [x] `fetch_variations.py` — 1,758 variations
- [x] `slim_variations.py`
- [x] `validate_variations.py` — 1,740 passed, 18 flagged (same)
- [x] `analyze_*.py` scripts

**Reshape → Create Items**
- [x] `reshape_products.py` — 169 products, variable weight/dims=null, sortOrder on images, weightUnit/dimensionUnit=null
- [x] `reshape_variations.py` — 1,740 variations, all-or-nothing dims, sortOrder on variation images
- [x] `audit_reshape_products.py` + `verify_reshape_products.py` — PASSED
- [x] `audit_reshape_variations.py` + `verify_reshape_variations.py` — PASSED
- [x] `create_items.py` — 166 items, 3 flagged (same), 1,713 variations embedded
- [x] `audit_create_items.py` + `verify_create_items.py` + `analyze_items.py` — PASSED

**Categorize → Import**
- [x] `prosport_categorize_items.py` — 166 items, 197 leaf assignments, sortOrder on all 382 category nodes → PASSED
- [ ] `download_items.py` ← next
- [ ] `upload_items.py`
- [ ] `import_items.py`

**Run-2 docs:** `docs/prosport/run-2/`

---

## Sunglass Monster

**Credentials:** Confirmed working 2026-06-02.
**Products:** 277 (242 variable, 25 simple + 10 flagged).

### Steps

**Products**
- [x] `fetch_products.py` — 277 products
- [x] `analyze_products.py`
- [x] `slim_products.py`
- [x] `analyze_slim_products.py`
- [x] `validate_products.py` — 267 passed, 10 flagged
  - 2 attribute name collisions (Holiday Reader 29701, Dorothy Reader 29640 — `Lens Type for Filter` + `Filter by Lens Type` both clean to `Lens Type`)
  - 5 no-SKU products
  - 2 no-image products
  - 1 private status + SKU space + attribute collision (proSPORT VShield 25942)

**Variations**
- [x] `fetch_variations.py` — 2,675 variations across 242 variable products
- [x] `analyze_variations.py`
- [x] `slim_variations.py`
- [x] `analyze_slim_variations.py`
- [x] `validate_variations.py` — 2,560 passed, 115 flagged
  - 114: base SKU mismatch across 6 products
  - 1: SKU space (11143)
  - 1: no price (7682)

**Reshape → Create Items**
- [x] `reshape_products.py` — 267 products
- [x] `reshape_variations.py` — 2,560 variations
- [x] `audit_reshape_products.py` + `verify_reshape_products.py` — PASSED
- [x] `audit_reshape_variations.py` + `verify_reshape_variations.py` — PASSED
- [x] `create_items.py` — 260 items, 7 flagged, 2,537 variations embedded
- [x] `audit_create_items.py` + `verify_create_items.py` + `analyze_items.py` — PASSED

**Categorize → Import**
- [ ] `monster_categorize_items.py` — to be written ← next
- [ ] `download_items.py`
- [ ] `upload_items.py`
- [ ] `import_items.py`

---

## BikerShades

**Credentials:** Confirmed working 2026-06-04.
**Products:** 704 fetched (heavy WooCommerce junk: Rx add-ons, admin/private items, misc parts).
**Variation images:** Can be `null` — some photochromic/transition lens variations have no image set.

### Steps

**Products**
- [x] `fetch_products.py` — 704 products
- [x] `slim_products.py`
- [x] `validate_products.py` — 611 passed, 93 flagged (Rx add-ons, private/no-SKU/no-image junk)

**Variations**
- [x] `fetch_variations.py` — 5,993 variations across 478 variable products
- [x] `analyze_variations.py`
- [x] `slim_variations.py`
- [x] `analyze_slim_variations.py`
- [x] `validate_variations.py` — 5,299 passed, 694 flagged
  - 653: base SKU mismatch (36 products — polarized/non-polarized, SKU revisions, consolidated goggle lines)
  - 22: no name (photochromic variations)
  - 14: private status
  - 5: duplicate SKU (USPS return label junk)
  - 4: SKU spaces
  - 3: missing price

**Reshape → Create Items**
- [x] `reshape_products.py` — 611 products
- [x] `reshape_variations.py` — 5,299 variations
- [x] `audit_reshape_products.py` + `verify_reshape_products.py` — PASSED
- [x] `audit_reshape_variations.py` + `verify_reshape_variations.py` — PASSED
- [x] `create_items.py` — 461 items passed, 150 flagged, 5,239 variations embedded
  - 38 variable products with no filled variations (base SKU mismatch)
  - 94 Rx frame listings (-RX token in SKU — to be reimplemented as a feature)
  - 7 Try Before You Buy deposits (TRYB4UB- prefix — to be reimplemented as a feature)
  - 3 USPS return shipping labels (LABEL- prefix)
  - 6 partial unreplaced IDs (product still passes)
  - 2 duplicate SKU: 62556 (warranty), 49895 (face masks)
- [x] `audit_create_items.py` + `verify_create_items.py` + `analyze_items.py` — PASSED

**Categorize → Import**
- [ ] `bikershades_categorize_items.py` — to be written ← next
- [ ] `download_items.py`
- [ ] `upload_items.py`
- [ ] `import_items.py`
