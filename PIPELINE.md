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
Reads `fetch-products/products.json`. For each variable product, fetches all variations from the WooCommerce API and embeds them as full objects. Simple products pass through as-is.

**Checks (variable products):**
- Each fetched variation has `parent_id` matching the product (enforced during fetch)
- Bad variations (not a dict, or SKU not in Veeqo) are silently dropped
- At least 2 valid variations must remain after dropping
- No duplicate SKUs within a product's surviving variations
- All surviving variation SKUs share the same `NNXnn` structure

**Output:**
- `data/{brand}/create-items/items.json` — clean items with embedded variation objects
- `data/{brand}/create-items/flagged.json` — products that failed checks with reasons

---

### 3. `slim_items.py`
Strips each item down to the fields needed for migration.

**Product fields kept:** `name`, `description`, `short_description`, `sku`, `price`, `regular_price`, `sale_price`, `images` (src + name only)

**Variation fields kept:** `sku`, `image` (src + name only), `attributes` (name + option only), `price`, `regular_price`, `sale_price`

**Output:**
- `data/{brand}/slim-items/items.json`

---

### 4. `reshape_items.py`
Transforms slim items into the shape expected by the DB. All field names use camelCase.

**Product-level transformations:**
- `slug` — slugified from `name`
- `sku` — null for variable products
- `summary` — wrapped in array (`text[]`)
- `maxPriceCents` / `minPriceCents` — highest of price, regular_price, sale_price in cents
- `salePriceCents` — null (placeholder)
- `sale` — false
- `featured` — false
- `stock` — null for variable, 0 for simple
- `inStock` — false
- `totalSales` — null for variable, 0 for simple
- `categories` — empty array (populated in a later step)
- `productImages` — src, name, sortOrder (1-indexed)
- `descriptionImages` — empty array (populated in a later step)
- `attribute` — empty array (populated in a later step)

**Variation-level transformations:**
- `regularPriceCents` — highest of price, regular_price, sale_price in cents
- `salePriceCents` — null
- `sale` — false
- `stock` — 0
- `totalSales` — 0
- `variationImages` — array of {src, name, sortOrder}
- `attribute` — [{name, option}] from WC attributes

**Output:**
- `data/{brand}/reshape-items/items.json`

---

## Shared modules

- `veeqo.py` — loads `sellables_export*.csv` once at import; exposes `check_veeqo(sku) -> bool`
- `sku_structure.py` — `check_sku(sku) -> bool` and `get_structure(sku) -> str | None` for the `NNXnn` pattern

## Data flow

```
WooCommerce API
      │
fetch_products.py  →  fetch-products/products.json
      │
create_items.py    →  create-items/items.json
      │
slim_items.py      →  slim-items/items.json
      │
reshape_items.py   →  reshape-items/items.json
      │
    (next: categorize, download images, import to Supabase)
```
