# validate-variations flagged — proSPORT Sunglasses
_18 variations flagged, 1740 passed_

## SKU contains spaces — parent=2145 (proSPORT Eliminator Polarized Bifocal) — 16 variations

ids: 2146, 2147, 2152, 2153, 2154, 2155, 2156, 2157, 2158, 2159, 2160, 2161, 2162, 2163, 2164, 2165

All 16 variations have an errant space in their SKU before the `-MFS` or `-MTO` suffix e.g. `BFPL73X31EL -MBK-SM-150-MFS`.

**Decision:** excluded from pipeline. Fix the SKUs in WooCommerce and re-run, or strip the space at reshape.

---

## SKU contains spaces — parent=2211 (proSPORT Professor Multifocal Reader) — 1 variation

id: 2395, SKU: `PR29X35PR-BK-CL-350 -MFS`

Same errant space pattern before `-MFS`.

**Decision:** excluded from pipeline. Fix the SKU in WooCommerce and re-run, or strip the space at reshape.

---

## id=1355 — no price (parent=1208, proSPORT Morocco Mirror)

- `price is missing or empty` — SKU `CA25X095MRMIRROR`, `instock` with stock_quantity set, but no `price`, `regular_price`, or `sale_price`

**Decision:** excluded from pipeline. WooCommerce data issue — assign a price in WooCommerce and re-run, or drop.
