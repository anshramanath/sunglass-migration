# Sunglass Monster Migration Progress
_Last updated: 2026-06-02_

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
| Stock | `is_in_stock` bool | `stock_quantity` int + `stock_status` string — use `stock_status` as source of truth |
| Variation images | `images[]` array | `image` singular object |
| Attributes | `{name, value}` | `{id, name, slug, option}` — `option` is term name |

### Steps

**Products**
- [x] Credentials acquired and confirmed
- [x] `fetch_products.py` written and run — 171 products
- [x] `analyze_products.py` — raw field coverage, pricing quirks, category/attribute breakdown
- [x] `slim_products.py` — relevant fields extracted
- [x] `analyze_slim_products.py` — field presence, on_sale truthfulness, stock cross-checks
- [x] `validate_products.py` — 169 passed, 2 flagged (draft copy + no-SKU simple)

**Variations**
- [ ] `fetch_variations.py` written and run — 1,794 IDs across 154 variable products
- [ ] `slim_variations.py`
- [ ] `validate_variations.py`

**Reshape → Import**
- [ ] `reshape_items.py`
- [ ] `recategorize_items.py`
- [ ] Download images
- [ ] Upload images
- [ ] Import
