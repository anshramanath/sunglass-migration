# validate-variations notes — proSPORT Sunglasses

## Results

- Input: `slim-variations/variations.json` (1758 variations across 153 products)
- Passed: 1740 → `validated-variations/variations.json`
- Flagged: 18 → `validated-variations/flagged.json`

See [flagged.md](flagged.md) for details and decisions on each flagged variation.

## Checks

All checks are hard errors — a variation with any failure is excluded from `variations.json` and written to `flagged.json` with its full list of reasons. Its parent product entry is kept but with that variation removed.

| Field | Rule |
|---|---|
| `product_id` | Number; must match a known ID in `validated-products/products.json` |
| `id` | Number, unique across all variations |
| `parent_id` | Number; must match the `product_id` of the entry it lives under |
| `name` | Non-empty string |
| `type` | Must be `"variation"` |
| `status` | Must be `"publish"` |
| `description` | String or null |
| `permalink` | Non-empty string |
| `sku` | Non-empty string, no spaces, unique across all variations |
| `price` | Required; valid number greater than zero |
| `regular_price` | Null or empty OK; if present must be a valid number |
| `sale_price` | Null or empty OK; if present must be a valid number; must be less than `regular_price` when both present |
| `on_sale` | Boolean |
| `on_sale` vs `sale_price` | If `on_sale=True`, must have `sale_price`; if `sale_price` set, `on_sale` must be `True` |
| `price` vs `regular_price` | When no `sale_price`, `price` must equal `regular_price` |
| `stock_quantity` | Number or null |
| `stock_status` | Required; must be `instock` or `outofstock` |
| `weight` | Null or empty OK; if present must be a valid number |
| `dimensions.length/width/height` | Null or empty OK; if present must be a valid number |
| `image.src` | Non-empty string starting with `http` |
| `image.name` | Non-empty string |
| `attributes[].name` | Non-empty string |
| `attributes[].option` | Non-empty string |

## Design decisions

- **`price` required on variations** — unlike parent products where variable products derive price from variations, every variation must have its own price.
- **`on_sale` fully reliable on variations** — checked bidirectionally. Every `on_sale=True` has a `sale_price` and every `sale_price` has `on_sale=True`.
- **`parent_id` cross-checked against entry key** — each variation's `parent_id` must match the `product_id` of the entry it was fetched under.
- **Flagged variations excluded per-variation, not per-product** — a product entry with some flagged variations still appears in `variations.json` with its valid variations intact.
- **Brand-agnostic** — no hardcoded attribute names or brand-specific values.
- **All checks run per variation** — a variation accumulates every failure, not just the first.
