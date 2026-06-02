# slim-products notes — proSPORT Sunglasses

## Fields in slim-products

| Field | Notes |
|---|---|
| `id` | WP post ID |
| `name` | Product title |
| `slug` | URL slug — 1 missing (draft copy) |
| `permalink` | Canonical storefront URL |
| `type` | `variable` or `simple` — metadata only, not source of truth for variations |
| `status` | `publish` or `draft` |
| `description` | HTML — 148/171 populated. Contains old Sunglass Monster image URLs. |
| `short_description` | HTML — sparse (35/171) |
| `sku` | Parent SKU — will be nulled for variable products at reshape |
| `price` | Display price. Derived from variations for variable products. |
| `regular_price` | Only on simple products (17) |
| `sale_price` | Only on simple products with active sale (16) |
| `on_sale` | Reliable for simple products only. Always True for variable — ignore it. |
| `featured` | Boolean — True on 5 products |
| `total_sales` | Integer — 80 products have >0 sales, 91 have 0. Treat 0 as unknown. |
| `stock_quantity` | Integer — only populated where `manage_stock=True` (19 products) |
| `stock_status` | `instock` / `outofstock` — source of truth for availability |
| `weight` | String — populated on 18 products |
| `dimensions` | Object `{length, width, height}` — all empty strings on every product. Drop at reshape. |
| `categories` | `[{name, slug}]` — all 171 include Uncategorized. Drop it at reshape. |
| `images` | `[{src, name}]` — parent gallery images |
| `attributes` | `[{name, options}]` — 11 products have none |
| `variations` | `[int]` — variation IDs. Source of truth for whether product is variable. |
| `related_ids` | `[int]` — WP auto-generated, not curated. Drop at reshape. |

## Decisions made

- **`stock_status` is source of truth** — `stock_quantity` kept as supplementary but `stock_status` wins.
- **`variations` is source of truth** for variable vs simple — not `type`.
- **`on_sale` ignored for variable products** — always True regardless of actual sale state.
- **`href` dropped** — `permalink` covers the URL need.
- **`dimensions` dropped at reshape** — 0/171 have real data.
- **`related_ids` dropped at reshape** — WooCommerce auto-generated, not useful.
- **`Uncategorized` stripped at reshape** — every product has it, carries no signal.
- **Parent SKU nulled for variable products at reshape** — real SKUs live on variations.

## Flags to handle at reshape

- **Draft product** — `proSPORT Cabriolet Mirror Bifocal (Copy)` (id 4019, 1 product)
- **No SKU** — `Sunglass String Chum Strap` (id 3139, simple product)
- **Description URLs** — HTML descriptions contain `sunglassmonster.com` image URLs. Decide whether to rewrite or strip.
- **11 products with no attributes** — confirm at reshape they are simple products.
