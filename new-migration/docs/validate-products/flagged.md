# validate-products flagged — proSPORT Sunglasses
_2 products flagged, 169 passed_

## id=4019 — proSPORT Cabriolet Mirror Bifocal (Copy)

- `slug is not a valid non-empty string` — slug is `""`, product has no URL slug
- `status=draft` — not published, likely a copy/junk entry

**Decision:** excluded from pipeline. Draft copy with no URL slug — drop.

---

## id=3139 — Sunglass String Chum Strap

- `sku is not a valid non-empty string` — sku is `""`, simple product with no SKU

**Decision:** excluded from pipeline. Needs a SKU assigned before it can be imported — either fix in WooCommerce and re-run, or drop.
