# reshape-products verify — proSPORT Sunglasses

## Result

`verify_reshape_products.py` — 169 products checked — **PASSED**

## Checks

| Check | Rule |
|---|---|
| ID coverage | Same set of IDs in `validate-products` and `reshape-products` |
| No old fields | `status`, `permalink`, `price`, `regular_price`, `sale_price`, `on_sale`, `short_description`, `stock_quantity`, `stock_status` absent |
| All expected fields present | All 21 output fields present on every product |
| Pass-through fields unchanged | `id`, `name`, `slug`, `type`, `sku`, `featured`, `categories`, `attributes`, `variations` match source exactly |
| `oldLink` | Equals source `permalink` |
| `images` | Unchanged from source |
| `totalSales` | Equals source `total_sales` |
| `description` | No HTML tags remaining |
| `descriptionImages` | List of `http` URLs or `null` |
| `shortDescription` | List of plain strings (no HTML) or `null` |
| Price field types | `minPriceCents`, `maxPriceCents`, `salePriceCents` are `int` or `null` |
| Variable pricing | `minPriceCents`, `maxPriceCents`, `salePriceCents` all `null`; `sale` matches source `on_sale` |
| Simple pricing | `minPriceCents == maxPriceCents`; equals `regularPrice` cents if set, else `price` cents; `salePriceCents` matches source `sale_price`; `sale` matches source `on_sale` |
| `stock` | Equals `stock_quantity` if non-null, else `1`/`0` from `stock_status` |
| `weight` | Float or `null`; matches source value |
| `dimensions` | `null` or all-three-field object with float values |
