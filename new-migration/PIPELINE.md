# Pipeline — Checks & Flagging Conditions

---

## validate_products

Reads `slim-products/`. Loads Veeqo CSV for SKU presence checks.

**All products:**
- `id` not a number → flag
- `id` not unique → flag
- `name` not a non-empty string → flag
- `slug` not a non-empty string → flag
- `permalink` not a non-empty string → flag
- `type` not `"variable"` or `"simple"` → flag
- `type=variable` but `variations[]` is empty → flag
- `type=simple` but `variations[]` is non-empty → flag
- `status != "publish"` → flag
- `description` present but not a string → flag
- `short_description` present but not a string → flag
- `sku` missing or empty → flag
- `sku` contains spaces → flag
- `sku` duplicate (already seen on another product) → flag
- `price` missing, empty, not a valid number, or ≤ 0 → flag
- `regular_price` present but not a valid number → flag
- `sale_price` present but not a valid number → flag
- `sale_price >= regular_price` when both present → flag
- `on_sale` not a boolean → flag
- `featured` not a boolean → flag
- `total_sales` present but not a number → flag
- `stock_quantity` present but not a number → flag
- `stock_status` missing or not `"instock"` / `"outofstock"` → flag
- `weight` present but not a valid number → flag
- Any `dimensions.{length,width,height}` present but not a valid number → flag
- Any category `name` or `slug` not a non-empty string → flag
- `images[]` empty → flag
- Any image `src` not a non-empty string, or not starting with `http` → flag
- Any image `name` not a non-empty string → flag
- Any attribute `name` not a non-empty string → flag
- Any attribute `options[]` entry not a non-empty string (empty array is OK) → flag
- Two attribute names on the same product clean to the same string (`clean_attr_name`) → flag
- `variations[]` contains a non-number entry → flag

**Simple products only:**
- `sku` not present in Veeqo → flag
- `sku` has no `NNXnn` model number (`\d+[Xx]\d+` in first hyphen segment, leading `C` combo prefix stripped) → flag
- `on_sale=True` but no `sale_price` → flag
- `sale_price` set but `on_sale=False` → flag
- No `sale_price` but `price != regular_price` → flag

---

## validate_variations

Reads `slim-variations/` + `validate-products/products.json` (to know which product IDs are valid). Loads Veeqo CSV.

Variations whose `product_id` is not a number → skipped silently.
Variations whose `product_id` is not in the validated product set → flagged for each variation in that entry.

**Pass 1 — per variation:**
- `id` not a number → flag + skip
- `id` duplicate → flag + skip
- `parent_id` not a number → flag
- `parent_id` does not match the group's `product_id` → flag
- `status != "publish"` → flag
- `sku` empty or not present in Veeqo → flag
- `price` missing, empty, not a valid number, or ≤ 0 → flag
- `regular_price` present but not a valid number → flag
- `sale_price` present but not a valid number → flag
- `sale_price >= regular_price` when both present → flag
- `on_sale` not a boolean → flag
- `on_sale=True` but no `sale_price` → flag
- `sale_price` set but `on_sale=False` → flag
- No `sale_price` but `price != regular_price` → flag
- `stock_quantity` present but not a number → flag
- `stock_status` missing or not `"instock"` / `"outofstock"` → flag
- `weight` present but not a valid number → flag
- Any `dimensions.{length,width,height}` present but not a valid number → flag
- `image` present but has no `src`, or `src` does not start with `http` → flag (`image: null` is OK)
- Any attribute `name` not a non-empty string → flag
- Any attribute `option` not a non-empty string → flag
- Two attribute names on the same variation clean to the same string (`clean_attr_name`) → flag

**Pass 2 — model checks (only on variations that passed Pass 1):**
- `sku` has no `NNXnn` model number → flag
- Sibling variations of the same product have different model numbers → flag all siblings in that product

---

## reshape_products

Reads `validate-products/`. No flagging — transforms only.

- `description`: img URLs extracted into `descriptionImages[]` with 1-indexed `sortOrder`; HTML stripped from text
- `short_description`: `<li>` items parsed into plain-text `summary[]` array
- `images[]`: each image gets 1-indexed `sortOrder`
- `attributes[].name`: run through `clean_attr_name()`; Power options normalized to `+X.XX` / `-X.XX`
- Prices → cents via `round(float * 100)`
- Weight + dimensions → float via `to_num()`
- **Partial dimensions** (only some of l/w/h present) → all three nullified, `[INFO]` printed

**Variable products:**
- `sku = null`
- `minPriceCents`, `maxPriceCents`, `salePriceCents`, `sale` = null (derived in create_items)
- `stock`, `inStock` = null (derived in create_items)
- `weight`, all dimensions = null

**Simple products:**
- `sku` = product SKU
- Prices computed from `regular_price` / `price` / `sale_price`
- `stock` = `stock_quantity` if set, else 1 if `stock_status == "instock"` else 0
- `inStock` = `stock > 0`
- `sale` = product `on_sale`

All products: `weightUnit`, `dimensionUnit` = null.

---

## reshape_variations

Reads `validate-variations/`. No flagging — transforms only.

- `attribute[].name`: run through `clean_attr_name()`; Power options normalized
- `images[]`: `image` singular object → `images[]` array with `sortOrder: 1`; null image → empty array
- `stock` = `stock_quantity` if set, else 1 if `stock_status == "instock"` else 0
- Prices → cents; weight + dimensions → float
- **Partial dimensions** → all three nullified, `[INFO]` printed
- `weightUnit`, `dimensionUnit` = null
- `description` not included (product description is the source of truth)

---

## create_items

Reads `reshape-products/` + `reshape-variations/`. Embeds variations into products.

**Per variable product:**
- Any variation ID in the product's `variations[]` has no matching fetched variation → flag (unreplaced IDs remain as integers)
- Variable product has no filled variations after embed → flag + skip remaining checks
- A variation has an `attribute` name not present in the parent product's `attributes` → flag
  - If name does match, missing options are added to the parent's options list
- After expansion, options no variation uses are pruned; attributes with no remaining options are dropped
- Variation images that duplicate a parent product image (by `src`) are removed
- `minPriceCents` / `maxPriceCents` derived from `regularPriceCents` across filled variations
- `sale` derived: `any(v["sale"] for v in filled)`
- `inStock` derived: `any(v["stock"] > 0 for v in filled)`

**Global (all items):**
- Duplicate SKU across any two products or across a product and a variation → flag both

---

## veeqo_items

Reads `create-items/`. Flags items where SKUs are absent from Veeqo.

- Variable products: any variation SKU absent from Veeqo → flag the product
- Simple products: product SKU absent from Veeqo → flag the product

Clean items written to `veeqo-items/items.json`; flagged to `veeqo-items/flagged.json`.

---

## {brand}_categorize_items

Reads `veeqo-items/items.json`. Assigns category paths.

- Category names normalized and mapped to canonical slugs
- Each path is a list of `{level, name, slug, sortOrder}` nodes
- Every node gets a `sortOrder` from a `SORT_ORDER` dict (slug → int, 1-indexed, resets per parent)
- Output written to `categorize-items/items.json`
