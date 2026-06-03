# reshape-variations notes — proSPORT Sunglasses

## Results

- Input: `validate-variations/variations.json` (1740 variations across 152 products)
- Output: `reshape-variations/variations.json` (1740 variations across 152 products)
- Structure preserved: `[{product_id, variations: [...]}]`

## Field transformations

| Source field | Output field | Transformation |
|---|---|---|
| `status` | — | Dropped — always `"publish"` |
| `permalink` | `oldLink` | Renamed |
| `regular_price` | `regularPriceCents` | Cents (×100, rounded); `null` if empty |
| `sale_price` | `salePriceCents` | Cents (×100, rounded); `null` if empty |
| `on_sale` | `sale` | Renamed |
| `price` | — | Dropped — derivable from `regularPriceCents`/`salePriceCents` |
| `stock_quantity` + `stock_status` | `stock` | `stock_quantity` if non-null, else `1` if `instock` or `0` if `outofstock` |
| `weight` | `weight` | String → float; `null` if empty |
| `dimensions` | `dimensions` | Always `{length, width, height}`; each field float or `null` |
| `attributes[].name` | `attributes[].name` | `"Choose "` prefix stripped (e.g. `Choose Color` → `Color`) |
| `image` | `images` | Wrapped in array: `[image]` if source image has a src; `[]` if null. Object passed through as-is (`{src, name}` from slim stage) |

All other fields (`id`, `parent_id`, `name`, `type`, `sku`, `description`) pass through unchanged except `description` has HTML stripped to plain text.

## Design decisions

- **Grouped structure preserved** — `[{product_id, variations: [...]}]` kept from validate stage; `parent_id` on each variation also preserves the relationship for the combine step.
- **`price` dropped** — the current selling price is derivable: `salePriceCents` if `sale=True`, else `regularPriceCents`. Storing it separately would be redundant and could drift.
- **`regularPriceCents` not `minPriceCents`/`maxPriceCents`** — unlike products, a variation has a single fixed price, not a range.
- **`status` and `type` handling** — `status` dropped (always `"publish"`); `type` kept (always `"variation"` but useful as a discriminator at the combine step).
- **Attribute name cleaning** — only `"Choose "` prefix stripped; no `"for Filter"` suffix exists on variations (those attrs only appear on products).
- **Dimensions always an object** — `{length, width, height}` with nullable fields. No ProSport variations have dimension data; all fields are `null`.
- **Empty strings → null** — all optional scalar fields follow this convention, matching product reshape.
