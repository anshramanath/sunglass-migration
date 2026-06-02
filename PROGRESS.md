# Sunglass Monster Migration Progress
_Last updated: 2026-06-01_

Multi-brand WooCommerce → Supabase migration using the authenticated admin REST API.

---

## Brands

| Brand | Status |
|-------|--------|
| proSPORT Sunglasses | 🔄 In progress |

---

## Decisions

- **Admin REST API over Store API** — authenticated, returns real stock quantities, complete variation data, and full price fields. Store API was used for BikerShades (old pipeline) but was lossy — variation images limited to 1, no real stock counts.
- **`BRAND` env var selects active brand** — hardcoded dict maps brand name → slug + credential env var names. Switching brands is one `.env` change.
- **Output isolated per brand slug** — all pipeline output written to `data/{slug}/` so multiple brands can coexist on disk without collision.
- **Docs isolated per brand** — `docs/{slug}/` mirrors the same structure as old pipeline docs.

---

## ProSport Sunglasses

**Credentials:** Confirmed working 2026-06-01.
**Products:** 171 (154 variable, 17 simple).
**Variation images:** Single `image` field only — no `gallery_image_ids` populated across any product.
**Stock:** Real `stock_quantity` integers available (`manage_stock: true` on variable products).

### Admin API shape differences to handle in reshape

| Field | Old Store API | New Admin API |
|-------|--------------|---------------|
| Prices | `prices.regular_price` | `regular_price` (top-level string) |
| Stock | `is_in_stock` bool | `stock_quantity` int + `stock_status` string |
| Variation images | `images[]` array | `image` singular object |
| Attributes | `{name, value}` | `{id, name, slug, option}` — `option` is term name |

### Steps

- [x] Credentials acquired and confirmed
- [x] Raw product shape inspected
- [ ] `fetch_products.py` written and run
- [ ] `fetch_variations.py` written and run
- [ ] Analyze raw data — categories, attributes, image coverage
- [ ] `reshape_items.py` written
- [ ] QA reshape
- [ ] `recategorize_items.py` written
- [ ] QA recategorize
- [ ] Download images
- [ ] Upload images
- [ ] Import
