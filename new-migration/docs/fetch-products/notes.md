# fetch-products notes — proSPORT Sunglasses

## Fields kept in slim-products

| Field | Shape after slim | Notes |
|---|---|---|
| `id` | integer | WP post ID |
| `name` | string | Product title |
| `slug` | string | URL slug — 1 missing (draft copy, id 4019) |
| `permalink` | string | Canonical storefront URL |
| `type` | string | `variable` or `simple` — metadata only, not source of truth |
| `status` | string | `publish` or `draft` |
| `description` | string | HTML — 148/171 populated. Contains old Sunglass Monster image URLs. |
| `short_description` | string | HTML — sparse (35/171) |
| `sku` | string | Parent SKU — nulled for variable products at reshape |
| `price` | string | Display price. Derived from variations for variable products. |
| `regular_price` | string | Only on simple products (17) |
| `sale_price` | string | Only on simple products with active sale (16) |
| `on_sale` | boolean | Reliable for simples only. Always True for variable (WC quirk) — ignore at reshape. |
| `featured` | boolean | True on 5 products |
| `total_sales` | integer | >0 on 80 products. Treat 0 as unknown, not confirmed zero. |
| `stock_quantity` | integer\|null | Only valid when `manage_stock=True` in raw (19 products) |
| `stock_status` | string | `instock` / `outofstock` — source of truth for availability |
| `weight` | string | Populated on 18 products |
| `dimensions` | object | `{length, width, height}` — all empty strings on every product. Drop at reshape. |
| `categories` | `[{name, slug}]` | id dropped. All include Uncategorized — strip at reshape. |
| `images` | `[{src, name}]` | id/alt/srcset dropped. Parent gallery only, not variation images. |
| `attributes` | `[{name, options}]` | id/slug/variation flag dropped |
| `variations` | `[int]` | Variation IDs — source of truth for whether product is variable |

## Fields dropped entirely

All carry zero information (always null, always empty, or all-same WooCommerce defaults):

`date_on_sale_from/to`, `virtual`, `downloadable`, `downloads`, `download_limit`, `download_expiry`, `external_url`, `button_text`, `tax_status`, `tax_class`, `backorders`, `backorders_allowed`, `backordered`, `low_stock_amount`, `sold_individually`, `shipping_required`, `shipping_taxable`, `shipping_class`, `shipping_class_id`, `reviews_allowed`, `average_rating`, `rating_count`, `upsell_ids`, `cross_sell_ids`, `parent_id`, `purchase_note`, `brands`, `tags`, `default_attributes`, `grouped_products`, `menu_order`, `post_password`, `global_unique_id`, `meta_data`, `has_options`, `purchasable`, `catalog_visibility`, `date_created`, `date_modified` (and all `_gmt` twins), `price_html`, `manage_stock`, `href`, `_links`, `related_ids`

## Gotchas

- **`on_sale=True` on 170/171 products** — WooCommerce sets it when any variation is on sale. 154 variable products have it True with no parent `sale_price`. Ignore for variable products.
- **Uncategorized on every product** — must strip at reshape.
- **Parent SKU on variable products** — meaningless. Nullify at reshape.
- **`dimensions`** — object always present but all subfields empty. Drop at reshape.
- **`stock_quantity`** — only valid when `manage_stock=True`. Use `stock_status` as source of truth.
- **Descriptions contain Sunglass Monster URLs** — HTML points to `sunglassmonster.com`. Decide at reshape whether to rewrite or strip.
- **11 products with no attributes** — likely all simple products. Verify at reshape.
- **1 draft product** — `proSPORT Cabriolet Mirror Bifocal (Copy)` (id 4019). Flag at reshape.
- **1 product with no SKU** — `Sunglass String Chum Strap` (id 3139, simple). Flag at reshape.
- **`type` field** — use `len(variations) > 0` as the actual source of truth for variable vs simple.
