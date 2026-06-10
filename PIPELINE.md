# Pipeline

All scripts live in `final-migration/pipeline/` and are run from the repo root with `BRAND=<brand>` set.

```bash
BRAND=prosport python final-migration/pipeline/fetch_products.py
```

Valid brand values: `prosport`, `monster`, `bikershades`

---

## Steps

### 1. `fetch_products.py`

Fetches all products from the WooCommerce REST API, paginating at 100 per page. Variable products pass through unchecked. Simple products are validated before being included.

**Simple product checks:**
- `variations` array must be empty — a simple product must not have variation IDs
- SKU matches `NNXnn` structure (digits, X, digits in the first hyphen-segment)
- SKU exists in the Veeqo CSV
- SKU is globally unique across all simple products in this brand

**Output:**
- `data/{brand}/fetch-products/products.json` — all passing products (simple + variable)
- `data/{brand}/fetch-products/flagged.json` — failed simple products with reasons

---

### 2. `create_items.py`

Reads `fetch-products/products.json`. For each variable product, fetches all variations from the WooCommerce variations endpoint and embeds them as full objects. Simple products pass through with an empty variations array.

**Phase 1 — fetch (variable products only):**
- Variations are fetched page by page from `/products/{id}/variations`
- Any variation whose `parent_id` does not match the product ID is rejected
- A non-200 response or any `parent_id` mismatch flags the product immediately — validity checks do not run

**Phase 2 — validity checks (variable products that passed phase 1):**
- Variations that are not a dict or whose SKU is not in Veeqo are silently dropped
- At least 2 valid variations must survive
- No duplicate SKUs within a product's surviving variations
- All surviving variation SKUs must share the same `NNXnn` structure

**Output:**
- `data/{brand}/create-items/items.json` — clean items with embedded variation objects
- `data/{brand}/create-items/flagged.json` — products that failed either phase with reasons

---

### 3. `slim_items.py`

Strips each item down to only the fields needed for migration. All other WooCommerce fields are discarded here.

**Product fields kept:** `name`, `description`, `short_description`, `sku`, `price`, `regular_price`, `sale_price`, `images` (src + name only)

**Variation fields kept:** `sku`, `image` (src + name only), `attributes` (name + option only), `price`, `regular_price`, `sale_price`

**Output:**
- `data/{brand}/slim-items/items.json`

---

### 4. `reshape_items_1.py`

Transforms slim items into the DB shape. All field names use camelCase. Prices converted to cents. HTML stripped. Images restructured with `sortOrder`.

**Product-level transformations:**

| Field | Value |
|---|---|
| `slug` | Slugified from `name` |
| `sku` | `null` for variable products |
| `description` | HTML stripped to plain text; `null` if empty |
| `descriptionImages` | `img` tags extracted from description HTML as `{src, name, sortOrder}` |
| `summary` | `<li>` items → individual array elements; `<p>` → single-element array; `[]` if no short_description |
| `maxPriceCents` / `minPriceCents` | Highest of WC `price`, `regular_price`, `sale_price` in cents; `null` if none |
| `salePriceCents` | `null` |
| `sale` | `false` |
| `featured` | `false` |
| `stock` | `null` for variable, `0` for simple |
| `inStock` | `false` |
| `totalSales` | `null` for variable, `0` for simple |
| `categories` | `[]` (deferred — populated later) |
| `productImages` | `{src, name, sortOrder}` (1-indexed) |
| `attributes` | `[]` (populated in reshape_items_2) |

**Variation-level transformations:**

| Field | Value |
|---|---|
| `regularPriceCents` | Highest of WC `price`, `regular_price`, `sale_price` in cents; `null` if none |
| `salePriceCents` | `null` |
| `sale` | `false` |
| `stock` | `0` |
| `totalSales` | `0` |
| `variationImages` | `{src, name, sortOrder}` |
| `attribute` | `[{name, option}]` from WC attributes |

**Output:**
- `data/{brand}/reshape-items/items.json`

---

### 5. `reshape_items_2.py`

Enriches reshape_items_1 output with Veeqo CSV data, then derives variable product fields from surviving children.

**Veeqo enrichment rules:**
- Price source: `sales_price` column → cents. Highest value wins if a SKU appears in multiple rows.
- Stock source: `qty_on_hand` column. Lowest value wins if a SKU appears in multiple rows.
- Veeqo always takes priority over WooCommerce values. `0` is a valid Veeqo value.

**Simple products:**
- `maxPriceCents` / `minPriceCents` — overridden with Veeqo price; `null` if neither Veeqo nor WC has a price
- `stock` — overridden with Veeqo qty; defaults to `0` if SKU not in Veeqo
- `inStock` — `true` if stock > 0

**Variable products — variations:**
- Variations with `null` `regularPriceCents` or empty `attribute` are silently dropped after enrichment
- `regularPriceCents` — overridden with Veeqo price; `null` if neither source has a price
- `stock` — overridden with Veeqo qty; defaults to `0` if not in Veeqo

**Variable products — derived from surviving children:**
- `maxPriceCents` — highest child `regularPriceCents` (nulls excluded)
- `minPriceCents` — lowest child `regularPriceCents` (nulls excluded)
- `inStock` — `true` if any child has stock > 0
- `attributes` — aggregated from child `attribute` arrays; one entry per unique name; options deduplicated and ordered by first appearance

**Output:**
- `data/{brand}/reshape-items-2/items.json`

---

### 6. `validate_items.py`

Validates all items against DB constraints. Description, summary, and categories are deferred fields and are not checked here.

**Checks (all products):**
- `name`, `slug` — non-empty string
- `minPriceCents`, `maxPriceCents` — non-null int > 0; min ≤ max
- `salePriceCents` — must be `null`
- `featured`, `sale` — must be `false`
- `inStock` — must be boolean
- `categories` — must be `[]`
- `productImages` — non-empty; each entry has non-empty `src`, non-empty `name`, `sortOrder` int > 0
- `descriptionImages` — each entry valid if present

**Additional checks (simple products):**
- `sku` — non-null, non-empty
- `stock`, `totalSales` — must be int
- `variations` — must be empty

**Additional checks (variable products):**
- `sku` — must be `null`
- `stock`, `totalSales` — must be `null`
- `attributes` — non-empty; each entry has non-empty `name` and at least one non-empty option
- At least 2 variations; each variation: `sku` non-empty, `regularPriceCents` int > 0, `stock` int, `totalSales` int `0`, `sale` `false`, `attribute` non-empty list with valid name/option entries; variation image entries valid

**Output:**
- `data/{brand}/validate-items/items.json` — items that pass all checks
- `data/{brand}/validate-items/flagged.json` — items with reasons

---

### 7. `remove_items.py`

Reads `docs/remove_items.md` and filters out items that should not be imported. The markdown table is parsed at runtime — brand column must match the current brand.

**Match rules:**

| Type | Matched by |
|---|---|
| `Simple` | Product `sku` |
| `Variable product` | Product `slug` |
| `Variation` | Variation `sku` |

If a variable product loses variations such that fewer than 2 survive, the entire product is dropped.

**Output:**
- `data/{brand}/remove-items/items.json`

---

### 8. `merge_attributes.py`

Consolidates inconsistent WooCommerce attribute names into canonical lowercase names and rewrites options where needed. Applied to both product-level `attributes` and variation-level `attribute`. Options are deduplicated within merged names.

**Merge map:**

| Original name | Canonical name |
|---|---|
| Choose Color (REQUIRED), Choose Color, Color, Choose Frame Color (Required), Choose Bandana Color | `color` |
| Choose Power | `power` |
| Qty, Choose Quantity, Cleaner Spray Bottle QTY, Qty (packs of 3) | `quantity` |
| Choose Transition Type | `transition` |
| Choose Size | `size` |

**Option rewrite (Qty (packs of 3) only):**

| Original | Rewritten |
|---|---|
| 1 pack (3 masks total) | 3 masks |
| 2 packs (6 masks total) | 6 masks |
| 5 packs (15 masks total) | 15 masks |
| 10 packs (30 masks total) | 30 masks |

**Output:**
- `data/{brand}/merge-attributes/items.json`

---

### 9. `dedup_images.py`

Removes duplicate product images and variation images that repeat the parent's product images.

- `productImages` deduped by `src` URL — first occurrence kept, duplicates dropped
- Any `variationImages` entry whose `src` appears in the parent's `productImages` is removed entirely
- Empty `variationImages` on a variation means the frontend inherits the parent's product images — intentional

**Output:**
- `data/{brand}/dedup-images/items.json`

---

### 10. `generate_content.py`

Initializes the generate-content stage. Records what was originally missing from WooCommerce, then nulls everything so the MCP server regenerates all descriptions and summaries from scratch.

**Fields added:**

| Field | Value |
|---|---|
| `wasMissingDescription` | `true` if `description` was `null` in source |
| `wasMissingSummary` | `true` if `summary` was empty in source |
| `description` | Always set to `null` |
| `summary` | Always set to `[]` |

**Output:**
- `data/{brand}/generate-content/items.json`

---

### 11. MCP server (`mcp/server.py`)

AI-generates descriptions and summaries for all products using Claude Desktop and product images. This is not run as a pipeline script — Claude Desktop spawns it as a local process and communicates over stdio.

**Tools exposed:**

| Tool | Description |
|---|---|
| `get_next_product(brand)` | Returns next item needing content + fetches and attaches the product image |
| `save_content(brand, slug, description, summary)` | Validates content against format rules and writes to `generate-content/items.json` |
| `get_progress(brand)` | Returns `done/total, remaining` as a plain string |

**Validation rules enforced by `save_content`:**
- Description: max 80 words, no measurements, no banned phrases (`available in`, `choose from`, `comes in`)
- Summary: 4–6 bullets, each 5–12 words, capitalized first word, no trailing period, no banned phrases
- Returns `VALIDATION FAILED` with reasons if any rule is broken — Claude Desktop must fix and retry

**Claude Desktop config:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Prompt to use in Claude Desktop:**
```
Process {brand}. For each product:
1. Call get_next_product with brand="{brand}"
2. Study the image carefully
3. Generate the description and summary following the rules exactly
4. Call save_content — if it returns VALIDATION FAILED, fix and retry
5. Repeat until get_progress shows 0 remaining

Do not stop for status updates. Keep going until done.
If get_next_product returns the same slug twice in a row, stop immediately and report the slug — do not attempt to save again.
```

**Known issue — duplicate slugs:** If two products share the same slug, `save_content` always saves the first match. The second item gets stuck in an infinite loop. Fix: manually copy the saved content from the first duplicate to the second in the JSON file.

### 12. `{brand}_categorize_items.py`

Brand-specific scripts (`prosport_categorize_items.py`, `monster_categorize_items.py`, `bikershades_categorize_items.py`). Reads `generate-content/items.json` and assigns each item a category path based on a hardcoded tree. Sets the `categories` deferred field.

**Output:**
- `data/{brand}/categorize-items/items.json`

---

### 13. `normalize_image_names.py`

Reads `categorize-items/items.json`. Normalizes the `name` field on every image (product, description, variation) by deriving it from the image's `src` URL: takes the URL path basename stem and replaces dashes and underscores with spaces.

e.g. `https://example.com/uploads/2018/01/Black-Angle-3.jpg` → name becomes `Black Angle 3`

**Output:**
- `data/{brand}/normalize-images/items.json`

---

### 14. `validate_items_final.py`

Thorough pre-import validation. Stricter than `validate_items.py` — checks all fields including deferred ones now that they're populated.

**Checks beyond validate_items.py:**
- `description` and `summary` are populated (non-empty)
- `categories` structure: non-empty, levels sequential, sortOrders > 0, no duplicate leaf slugs
- `slug` format matches `^[a-z0-9]+(-[a-z0-9]+)*$`
- No duplicate slugs across the entire catalogue
- Image `src` values are valid `http(s)://` URLs
- `sortOrder` values are unique within each image array
- Product image `src` values are unique within a product
- Variation images do not duplicate any product-level image `src`
- Variation price consistency: `minPriceCents`/`maxPriceCents` match actual min/max across variations
- No duplicate attribute combinations across a product's variations

**Output:**
- `data/{brand}/validate-items-final/items.json` — import-ready items
- `data/{brand}/validate-items-final/flagged.json` — items with reasons

---

### 15. `download_items.py`

Downloads all images referenced in `validate-items-final/items.json` to local disk. Sources: `productImages`, `descriptionImages`, and variation `variationImages`.

- Each unique URL is downloaded exactly once
- Filename is derived from everything after `/uploads/` or `/gallery/` in the URL path, with `/` replaced by `_` (guarantees uniqueness within a brand)
- Crash-safe: already-downloaded URLs skipped via `download_map.json`
- Post-download check: verifies every item has at least one product image successfully downloaded

**Output:**
- `data/{brand}/download-items/images/` — downloaded files
- `data/{brand}/download-items/download_map.json` — URL → local path
- `data/{brand}/download-items/flagged.json` — failed downloads with SKU and URL

---

### 16. `upload_items.py`

Uploads all unique downloaded images to a Supabase storage bucket. Bucket is named after `brand_slug` (e.g. `prosport-sunglasses`, `sunglass-monster`, `bikershades`).

- Crash-safe: already-uploaded files skipped via `upload_map.json`
- Recovers gracefully from duplicate errors (re-fetches public URL instead of failing)
- Requires env vars: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`

**Output:**
- `data/{brand}/upload-items/upload_map.json` — local path → Supabase public URL

---

### 17. `import_items.py`

Imports clean items into the Supabase Postgres database. Per-brand: deletes only the current brand's data before inserting (other brands unaffected).

- No fallbacks — all field accesses are direct; a crash means a validation gap upstream
- Image URLs resolved via chain: original src → `download_map` → `upload_map` → Supabase URL; unresolved images are warned and skipped (not crash)
- Categories upserted lazily by path as products are processed
- Requires env vars: `DATABASE_URL`

**Note:** Direct connection host (`db.xxx.supabase.co`) uses IPv6 — may fail on corporate/office networks. Use the Supabase session pooler URL if DNS resolution fails.

**Output:** Products, variations, images, and categories written to Supabase DB.

---

## Shared modules

- `veeqo.py` — loads `sellables_export*.csv` once at import; exposes `check_veeqo(sku) -> bool`
- `sku_structure.py` — `check_sku(sku) -> bool` and `get_structure(sku) -> str | None` for the `NNXnn` pattern

---

## Data flow

```
WooCommerce API
        │
fetch_products.py    →  fetch-products/products.json
        │
create_items.py      →  create-items/items.json
        │
slim_items.py        →  slim-items/items.json
        │
reshape_items_1.py   →  reshape-items/items.json
        │
reshape_items_2.py   →  reshape-items-2/items.json
        │
validate_items.py    →  validate-items/items.json
        │
remove_items.py      →  remove-items/items.json
        │
merge_attributes.py  →  merge-attributes/items.json
        │
dedup_images.py      →  dedup-images/items.json
        │
generate_content.py  →  generate-content/items.json  ←  mcp/server.py writes here
        │
categorize_items.py  →  categorize-items/items.json
        │
normalize_image_names.py  →  normalize-images/items.json
        │
validate_items_final.py  →  validate-items-final/items.json
        │
download_items.py    →  download-items/images/ + download_map.json
        │
upload_items.py      →  upload-items/upload_map.json  (Supabase storage)
        │
import_items.py      →  Supabase DB
```
