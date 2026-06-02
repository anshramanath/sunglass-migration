# reshape-products notes — proSPORT Sunglasses

## Results

- Input: `validate-products/products.json` (169 products)
- Output: `reshape-products/products.json` (169 products)

## Field transformations

| Source field | Output field | Transformation |
|---|---|---|
| `permalink` | `oldLink` | Renamed |
| `status` | — | Dropped |
| `description` | `description` | All HTML stripped to plain text; `<img>` tags removed first |
| _(from description)_ | `descriptionImages` | Array of `src` URLs extracted from `<img>` tags; `null` if none |
| `short_description` | `shortDescription` | `<li>` items parsed to plain text array; `null` if empty |
| `price` | — | Dropped — replaced by `minPriceCents`/`maxPriceCents` |
| `regular_price` | — | Dropped — folded into `minPriceCents`/`maxPriceCents` logic |
| `sale_price` | `salePriceCents` | Cents (×100, rounded); `null` if empty. Simple only — null for variable |
| `on_sale` | `sale` | Renamed. Variable products retain WC value (deferred accuracy check); simple products use as-is |
| `total_sales` | `totalSales` | Renamed (camelCase) |
| `stock_quantity` + `stock_status` | `stock` | `stock_quantity` if non-null, else `1` if `instock` or `0` if `outofstock` |
| `weight` | `weight` | String → float; `null` if empty |
| `dimensions` | `dimensions` | All-or-nothing: all three fields as floats, or `null` if any missing |
| `images` | `images` | Unchanged (`[{src, name}]`) |
| `categories` | `categories` | Unchanged (`[{name, slug}]`) |
| `attributes` | `attributes` | Names cleaned: `"Choose "` prefix and `" for Filter"` suffix stripped (e.g. `Choose Color` → `Color`, `Lens Color for Filter` → `Lens Color`); options unchanged |
| `variations` | `variations` | Unchanged (array of IDs) |

All other fields (`id`, `name`, `slug`, `type`, `sku`, `featured`) pass through unchanged.

## Pricing logic

**Simple products:**
- `minPriceCents = maxPriceCents = regularPrice` if `regular_price` is set, else `price` (in cents)
- `salePriceCents = sale_price` in cents (or `null`)
- `sale = on_sale`

**Variable products:**
- `minPriceCents = null` — deferred to combine step (computed from variation prices)
- `maxPriceCents = null` — deferred to combine step
- `salePriceCents = null` — variable products have no product-level sale price
- `sale = on_sale` — WooCommerce value retained for cross-checking at combine step

## Design decisions

- **`regularPrice` as base for simple min/max** — `price` equals `sale_price` when a sale is active, so it's not a stable base. `regularPrice` gives the "was" price and is used when available.
- **`sale` kept on variable products** — WooCommerce sets this when any variation is on sale. Retained (not nullified) so accuracy can be verified against actual variation data at the combine step. For ProSport, 153/153 variable products have `sale=True` from WooCommerce; verified as accurate against validated variations (one exception is product 2145 whose variations were all flagged).
- **`stock` merge** — `stock_quantity` is the authoritative value when `manage_stock=true`. Fallback to `1`/`0` from `stock_status` covers products where stock management is off.
- **Dimensions all-or-nothing** — no ProSport products have dimension data. Rule ensures partial dimension objects (some fields set, others empty) don't slip through.
- **Empty strings → null** — all optional fields use `null` for absence rather than empty strings.
