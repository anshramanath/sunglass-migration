# validate-products notes — proSPORT Sunglasses

## Results

- Input: `slim-products/products.json` (171 products)
- Passed: 169 → `validated-products/products.json`
- Flagged: 2 → `validated-products/flagged.json`

See [flagged.md](flagged.md) for details and decisions on each flagged product.

## Checks

All checks are hard errors — a product with any failure is excluded from `products.json` and written to `flagged.json` with its full list of reasons.

| Field | Rule |
|---|---|
| `id` | Number, unique across all products |
| `name` | Non-empty string |
| `slug` | Non-empty string |
| `permalink` | Non-empty string |
| `type` | Must be `variable` or `simple` |
| `type` vs `variations` | `variable` must have variation IDs; `simple` must have none |
| `status` | Must be `publish` or `draft`; `draft` is an error |
| `description` | String or null |
| `short_description` | String or null |
| `sku` | Non-empty string, no spaces, unique across all products |
| `price` | Valid number greater than zero |
| `regular_price` | Null or empty string OK; if present must be a valid number |
| `sale_price` | Null or empty string OK; if present must be a valid number; must be less than `regular_price` when both present |
| `on_sale` | Boolean |
| `featured` | Boolean |
| `total_sales` | Number or null |
| `stock_quantity` | Number or null |
| `stock_status` | Required; must be `instock` or `outofstock` |
| `weight` | Null or empty OK; if present must be a valid number |
| `dimensions.length/width/height` | Null or empty OK; if present must be a valid number |
| `categories[].name` | Non-empty string |
| `categories[].slug` | Non-empty string; must match `slugify(name)` |
| `images[].src` | Non-empty string starting with `http` |
| `images[].name` | Non-empty string |
| `attributes[].name` | Non-empty string |
| `attributes[].options[]` | Each option a non-empty string |
| `variations[]` | Each entry a number |
| `related_ids[]` | Each entry a number |

## Design decisions

- **Brand-agnostic** — no hardcoded category names or brand-specific values. Works for any WooCommerce brand.
- **All checks run per product** — a product accumulates every failure, not just the first.
- **No separate audit/verify** — validation output is already structured (pass/fail JSON). Audit/verify belongs at later stages (reshape, import).
