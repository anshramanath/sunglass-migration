# fetch-products notes — proSPORT Sunglasses

## Fields to keep

| Field | Notes |
|---|---|
| `id` | WP post ID — use as foreign key reference |
| `name` | Product title |
| `slug` | URL slug — 1 product missing (draft copy) |
| `type` | `variable` or `simple` |
| `status` | `publish` or `draft` — 1 draft to decide on |
| `description` | HTML, 148/171 populated |
| `short_description` | HTML, sparse (35/171) |
| `sku` | Parent SKU — null for variable products at reshape |
| `price` | Display price (derived from variations for variable) |
| `regular_price` | Only on simple products (17) |
| `sale_price` | Only on simple products with active sale |
| `on_sale` | Unreliable at parent level — always verify via price comparison |
| `categories` | Array of `{id, name, slug}` — drop Uncategorized at reshape |
| `images` | Parent gallery — array of `{id, src, name, alt}` |
| `attributes` | Array of `{id, name, slug, options[], variation}` |
| `variations` | Array of variation IDs (integers) — fetch separately |
| `stock_status` | `instock` / `outofstock` |
| `manage_stock` | True on 19 products |
| `stock_quantity` | Only meaningful when `manage_stock=True` |
| `weight` | Populated on 18 products |
| `total_sales` | 47% populated — treat 0 as unknown, not confirmed zero |
| `featured` | True on 5 products |

## Fields to drop

All of these are 0% filled or carry only WooCommerce defaults with no signal:

`date_on_sale_from/to`, `virtual`, `downloadable`, `downloads`, `download_limit`, `download_expiry`, `external_url`, `button_text`, `tax_status`, `tax_class`, `backorders`, `backorders_allowed`, `backordered`, `low_stock_amount`, `sold_individually`, `dimensions`, `shipping_required`, `shipping_taxable`, `shipping_class`, `shipping_class_id`, `reviews_allowed`, `average_rating`, `rating_count`, `upsell_ids`, `cross_sell_ids`, `parent_id`, `purchase_note`, `brands`, `tags`, `default_attributes`, `grouped_products`, `menu_order`, `post_password`, `global_unique_id`, `related_ids`, `meta_data`, `has_options`, `purchasable`, `catalog_visibility`, `permalink`, `date_created`, `date_modified` (and all `_gmt` twins), `price_html`, `_links`

## Gotchas

- **`on_sale=True` on 170/171 products** — WooCommerce quirk. Meaningless at the parent level for variable products. Real sale logic lives on variations.
- **Uncategorized tag on every product** — all 171 are tagged it alongside their real category. Must strip at reshape.
- **Parent SKU on variable products** — meaningless, real SKUs are on variations. Nullify at reshape.
- **`total_sales=0`** — could mean zero sales or untracked. Don't treat as confirmed data.
- **`stock_quantity`** — only valid when `manage_stock=True`. Otherwise null even if the product is instock.
- **Descriptions contain Sunglass Monster URLs** — images in description HTML point to the old store (`sunglassmonster.com`). Need to decide whether to rewrite or strip at reshape.
- **11 products have no attributes** — inspect at reshape to confirm they are simple products or intentional.
- **1 draft product** — `proSPORT Cabriolet Mirror Bifocal (Copy)`, id 4019. Drop at reshape unless needed.
