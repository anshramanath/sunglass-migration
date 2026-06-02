# reshape-variations verify — proSPORT Sunglasses

## Result

`verify_reshape_variations.py` — 1740 variations across 152 products — **PASSED**

## Checks

| Check | Rule |
|---|---|
| Product ID coverage | Same set of `product_id` keys in source and reshaped |
| Variation ID coverage | Same variation IDs per product in source and reshaped |
| No old fields | `status`, `permalink`, `price`, `regular_price`, `sale_price`, `on_sale`, `stock_quantity`, `stock_status` absent |
| All expected fields present | All 15 output fields present on every variation |
| Pass-through fields unchanged | `id`, `parent_id`, `name`, `type`, `sku` match source exactly |
| `oldLink` | Equals source `permalink` |
| `images` | Array; `[{src, name}]` if source `image` has a src; `[]` if source `image` is null |
| `description` | No HTML tags remaining |
| Price field types | `regularPriceCents`, `salePriceCents` are `int` or `null` |
| `regularPriceCents` | Equals source `regular_price` × 100 (rounded) |
| `salePriceCents` | Equals source `sale_price` × 100 (rounded), or `null` |
| `sale` | Equals source `on_sale` |
| `stock` | Equals `stock_quantity` if non-null, else `1`/`0` from `stock_status` |
| `weight` | Float or `null`; matches source value |
| `dimensions` | Always `{length, width, height}` dict; each field float or `null` |
| `attributes` names | `"Choose "` prefix stripped; `option` unchanged |
