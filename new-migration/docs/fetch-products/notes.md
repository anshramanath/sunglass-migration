# fetch-products notes — proSPORT Sunglasses

## Fields kept in slim-products

| Field | Shape after slim | Notes |
|---|---|---|
| `id` | integer | WP post ID |
| `name` | string | Product title |
| `slug` | string | URL slug — 1 product missing (draft copy) |
| `permalink` | string | Canonical store URL |
| `type` | string | `variable` or `simple` — not source of truth for variations; use `variations` array |
| `status` | string | `publish` or `draft` — 1 draft to decide on |
| `description` | string | HTML, 148/171 populated |
| `short_description` | string | HTML, sparse (35/171) |
| `sku` | string | Parent SKU — will be nulled for variable products at reshape |
| `price` | string | Display price (derived from variations for variable products) |
| `regular_price` | string | Only meaningful on simple products (17) |
| `sale_price` | string | Only on simple products with active sale |
| `on_sale` | boolean | Unreliable for variable products — always True. Reliable for simples only. |
| `stock_quantity` | integer\|null | Only valid when `manage_stock=True` on the raw product |
| `stock_status` | string | `instock` / `outofstock` |
| `weight` | string | Populated on 18 products |
| `dimensions` | object | `{length, width, height}` — mostly empty strings |
| `categories` | `[{name, slug}]` | id dropped — drop Uncategorized at reshape |
| `images` | `[{src, name}]` | id/alt/srcset dropped — parent gallery only, not variation images |
| `attributes` | `[{name, options}]` | id/slug/variation flag dropped |
| `variations` | `[int]` | Variation IDs — source of truth for whether product has variations |
| `related_ids` | `[int]` | WP-generated related product IDs |
| `href` | string | Self link from `_links.self[0].href` |

## Fields dropped entirely

All carry zero information (always null, always empty, or all-same WooCommerce defaults):

`date_on_sale_from/to`, `virtual`, `downloadable`, `downloads`, `download_limit`, `download_expiry`, `external_url`, `button_text`, `tax_status`, `tax_class`, `backorders`, `backorders_allowed`, `backordered`, `low_stock_amount`, `sold_individually`, `shipping_required`, `shipping_taxable`, `shipping_class`, `shipping_class_id`, `reviews_allowed`, `average_rating`, `rating_count`, `upsell_ids`, `cross_sell_ids`, `parent_id`, `purchase_note`, `brands`, `tags`, `default_attributes`, `grouped_products`, `menu_order`, `post_password`, `global_unique_id`, `meta_data`, `has_options`, `purchasable`, `catalog_visibility`, `date_created`, `date_modified` (and all `_gmt` twins), `price_html`, `manage_stock`, `total_sales`, `featured`

## Gotchas

- **`on_sale=True` on 170/171 products** — WooCommerce quirk. Meaningless at the parent level for variable products. Real sale logic lives on variations.
- **Uncategorized tag on every product** — all 171 are tagged it alongside their real category. Must strip at reshape.
- **Parent SKU on variable products** — meaningless, real SKUs are on variations. Nullify at reshape.
- **`stock_quantity`** — only valid when `manage_stock=True` on the raw product. Otherwise null even if the product is instock.
- **Descriptions contain Sunglass Monster URLs** — images in description HTML point to the old store (`sunglassmonster.com`). Decide at reshape whether to rewrite or strip.
- **11 products have no attributes** — inspect at reshape; likely simple products.
- **1 draft product** — `proSPORT Cabriolet Mirror Bifocal (Copy)`, id 4019. Drop at reshape unless needed.
- **`type` field** — kept for metadata but `len(variations) > 0` is the actual source of truth for whether a product is variable.
