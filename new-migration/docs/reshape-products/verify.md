# reshape-products verify — proSPORT Sunglasses

## Result

`verify_reshape_products.py` — 169 products checked — **PASSED**

## Checks

| Check | Rule |
|---|---|
| ID coverage | Same set of IDs in `validate-products` and `reshape-products` |
| No old fields | `status`, `permalink`, `price`, `regular_price`, `sale_price`, `on_sale`, `short_description`, `stock_quantity`, `stock_status` absent |
| All expected fields present | All 21 output fields present on every product |
| Pass-through fields unchanged | `id`, `name`, `slug`, `type`, `sku`, `featured`, `categories`, `variations` match source exactly |
| `attributes` names cleaned | `"Choose "` prefix and `" for Filter"` suffix stripped; options unchanged |
| `oldLink` | Equals source `permalink` |
| `images` | Unchanged from source |
| `totalSales` | Equals source `total_sales` |
| `description` | No HTML tags remaining |
| `descriptionImages` | Always a list of `{src, name}` objects; `src` starts with `http`; `name` derived from URL path after `/uploads/`; `[]` if none |
| `shortDescription` | Always a list of plain strings (no HTML); `[]` if empty |
| Price field types | `minPriceCents`, `maxPriceCents`, `salePriceCents` are `int` or `null` |
| Variable pricing | `minPriceCents`, `maxPriceCents`, `salePriceCents` all `null`; `sale` matches source `on_sale` |
| Simple pricing | `minPriceCents == maxPriceCents`; equals `regularPrice` cents if set, else `price` cents; `salePriceCents` matches source `sale_price`; `sale` matches source `on_sale` |
| `stock` | Equals `stock_quantity` if non-null, else `1`/`0` from `stock_status` |
| `weight` | Float or `null`; matches source value |
| `dimensions` | Always `{length, width, height}` dict; each field float or `null` |
