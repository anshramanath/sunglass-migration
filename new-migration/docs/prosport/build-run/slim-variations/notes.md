# slim-variations notes — proSPORT Sunglasses

## Fields in slim-variations

| Field | Notes |
|---|---|
| `id` | WP variation post ID |
| `parent_id` | Parent product ID — native from API, verified against fetch key |
| `name` | WC auto-generated e.g. `"Matte Black x Gloss Tortoise, 4.00"` |
| `type` | Always `"variation"` |
| `status` | All `publish` |
| `description` | String — sparse (429/1758) |
| `permalink` | Canonical variation URL |
| `sku` | Variation SKU — all 1758 present and unique |
| `price` | Display price — 1757/1758 present |
| `regular_price` | 1757/1758 present |
| `sale_price` | Present when on sale — reliable on variations |
| `on_sale` | Boolean — fully reliable (unlike parent products) |
| `stock_quantity` | Integer — all 1758 have a real quantity |
| `stock_status` | `instock` / `outofstock` — consistent with `stock_quantity` on all variations |
| `weight` | String — 1757/1758 populated. Values: `"2"`, `"0.0"`, `"2.0"` |
| `dimensions` | `{length, width, height}` — all empty strings. Drop at reshape. |
| `image` | `{src, name}` — 1758/1758 have a valid src |
| `attributes` | `[{name, option}]` — selected options per variation. 1–2 per variation. |

## Decisions made

- **`on_sale` reliable on variations** — every `True` has a real `sale_price`. Safe to use at reshape.
- **`stock_quantity` kept** — all 1758 have a real value (`manage_stock=True` on all). Both `stock_quantity` and `stock_status` are reliable signals.
- **`dimensions` dropped at reshape** — 0/1758 have real data.
- **`attributes` slimmed to `{name, option}`** — dropped `id` and `slug` from each attribute entry.
- **`image` slimmed to `{src, name}`** — dropped `id`, `alt`, and date fields.

## Flags to handle at validation

- **id=1355** (parent=1208, SKU=`CA25X095MRMIRROR`) — no price fields. Will be flagged and excluded.
