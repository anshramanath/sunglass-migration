# No-Category Items Review
_Last updated: 2026-05-31_

**Source:** `recategorized/no_category_items.json`

These 2 products had every one of their WooCommerce category links dropped during recategorization, leaving them with no valid category. They cannot be imported until the owner assigns them to a category.

Both were only in the `all-products` WooCommerce category — a catch-all that was dropped from the new tree since it maps to everything and nothing specific.

---

## Products

### Pacific Mirror Bifocal
- **SKU:** `BF4X05PC-0`
- **WpUrl:** https://bikershades.com/shop/all-products/pacific-mirror-bifocal/
- **WooCommerce category:** `all-products` (dropped — too broad)
- **Action needed:** Owner places this in the correct category (likely `bifocals`)

---

### Jersey Sunglass Reader
- **SKU:** `SRE81X13JS-0`
- **WpUrl:** https://bikershades.com/shop/all-products/jersey-sun-reader/
- **WooCommerce category:** `all-products` (dropped — too broad)
- **Action needed:** Owner places this in the correct category (likely `bifocals` or `prescription`)

---

## Blocker

Owner assigns each product to the correct leaf category. Once confirmed, add the category slug to the `recategorize_items.py` merge map and re-run recategorize.
