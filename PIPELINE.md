# Pipeline

All scripts live in `final-migration/pipeline/` and are run from the repo root with `BRAND=<brand>` set.

## Steps

### 1. `fetch_products.py`
Fetches all products from WooCommerce. Runs checks on simple products only; variable products pass through unchecked.

**Checks (simple products only):**
- SKU matches `NNXnn` structure (digits, X, digits in the first hyphen-segment)
- SKU exists in Veeqo CSV
- SKU is globally unique across all simple products
- `variations` array is empty (a simple product must not have variation IDs)

**Output:**
- `data/{brand}/fetch-products/products.json` — clean products (simple + variable)
- `data/{brand}/fetch-products/flagged.json` — failed simple products with reasons

---

### 2. `create_items.py`
Reads `fetch-products/products.json`. For each variable product, fetches all variations from the WooCommerce API and embeds them as full objects. Simple products pass through as-is with an empty variations array.

**Phase 1 — fetch (variable products only):**
- Variations are fetched page by page from the WooCommerce variations endpoint
- Any variation whose `parent_id` does not match the product ID is rejected
- If the API returns a non-200 or any variation fails the parent_id check, the product is flagged immediately and skipped — validity checks do not run

**Phase 2 — validity checks (variable products that passed phase 1):**
- Bad variations (not a dict, or SKU not in Veeqo) are silently dropped
- At least 2 valid variations must remain after dropping
- No duplicate SKUs within a product's surviving variations
- All surviving variation SKUs share the same `NNXnn` structure

**Output:**
- `data/{brand}/create-items/items.json` — clean items with embedded variation objects
- `data/{brand}/create-items/flagged.json` — products that failed either phase with reasons

---

### 3. `slim_items.py`
Strips each item down to the fields needed for migration.

**Product fields kept:** `name`, `description`, `short_description`, `sku`, `price`, `regular_price`, `sale_price`, `images` (src + name only)

**Variation fields kept:** `sku`, `image` (src + name only), `attributes` (name + option only), `price`, `regular_price`, `sale_price`

**Output:**
- `data/{brand}/slim-items/items.json`

---

### 4. `reshape_items_1.py`
Transforms slim items into the DB shape. All field names use camelCase.

**Product-level transformations:**
- `slug` — slugified from `name`
- `sku` — null for variable products
- `description` — HTML stripped to plain text; null if empty (deferred: will be filled in later)
- `descriptionImages` — img tags extracted from description HTML as `{src, name, sortOrder}`
- `summary` — `<li>` items become individual array elements; `<p>` becomes single-element array; empty if no short_description (deferred: will be filled in later)
- `maxPriceCents` / `minPriceCents` — highest of WC price, regular_price, sale_price in cents; null if none
- `salePriceCents` — null
- `sale` — false
- `featured` — false
- `stock` — null for variable, 0 for simple
- `inStock` — false
- `totalSales` — null for variable, 0 for simple
- `categories` — empty array (deferred: populated in a later step)
- `productImages` — `{src, name, sortOrder}` (1-indexed)
- `attributes` — empty array (populated in reshape_items_2)

**Variation-level transformations:**
- `regularPriceCents` — highest of WC price, regular_price, sale_price in cents; null if none
- `salePriceCents` — null
- `sale` — false
- `stock` — 0
- `totalSales` — 0
- `variationImages` — `{src, name, sortOrder}`
- `attribute` — `[{name, option}]` from WC attributes

**Output:**
- `data/{brand}/reshape-items/items.json`

---

### 5. `reshape_items_2.py`
Enriches reshape_items_1 output with Veeqo CSV data, then derives variable product fields from children.

**Veeqo enrichment:**
- Price source: `sales_price` column; highest value wins if a SKU has duplicate rows; converted to cents
- Stock source: `qty_on_hand` column; lowest value wins if a SKU has duplicate rows
- Veeqo always takes priority over WC values; 0 is a valid Veeqo value

**Simple products:**
- `maxPriceCents` / `minPriceCents` — overridden with Veeqo price; null if neither Veeqo nor WC has a price
- `stock` — overridden with Veeqo qty; defaults to 0 if not in Veeqo
- `inStock` — true if stock > 0

**Variations (variable products):**
- Variations with null `regularPriceCents` or empty `attribute` after enrichment are silently dropped
- `regularPriceCents` — overridden with Veeqo price; null if neither Veeqo nor WC has a price
- `stock` — overridden with Veeqo qty; defaults to 0 if not in Veeqo

**Variable products (derived from surviving children):**
- `maxPriceCents` — highest child `regularPriceCents` (nulls excluded)
- `minPriceCents` — lowest child `regularPriceCents` (nulls excluded)
- `inStock` — true if any child has stock > 0
- `attributes` — aggregated from child `attribute` arrays: one entry per unique name, options deduplicated and ordered by first appearance

**Output:**
- `data/{brand}/reshape-items-2/items.json`

---

### 6. `validate_items.py`
Validates all items against DB constraints. Skips description, summary, and categories (deferred fields).

**Checks (all products):**
- `name`, `slug` — non-empty string
- `minPriceCents`, `maxPriceCents` — non-null int; min ≤ max
- `salePriceCents` — int or null
- `featured`, `sale`, `inStock` — boolean
- `attributes` — list
- All image entries (productImages, descriptionImages) — src/name non-empty, sortOrder int

**Additional checks (simple products):**
- `sku` — non-null, non-empty
- `stock`, `totalSales` — int
- `variations` — must be empty

**Additional checks (variable products):**
- `sku` — must be null
- `stock`, `totalSales` — must be null
- At least 2 variations
- Each variation: `sku` non-empty, `regularPriceCents` int, `stock` int, `totalSales` int, `sale` bool, `attribute` non-empty list; variation image entries valid

**Output:**
- `data/{brand}/validate-items/items.json` — items that pass all checks
- `data/{brand}/validate-items/flagged.json` — items with reasons

---

## Shared modules

- `veeqo.py` — loads `sellables_export*.csv` once at import; exposes `check_veeqo(sku) -> bool`
- `sku_structure.py` — `check_sku(sku) -> bool` and `get_structure(sku) -> str | None` for the `NNXnn` pattern

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
    (next: fill description/summary, categorize, download images, import to Supabase)
```
