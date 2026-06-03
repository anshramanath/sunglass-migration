# reshape-products audit — Sunglass Monster

```
Total:    269  (variable: 244, simple: 25)

── Field presence ──
  description            250/269 (92.9%)
  descriptionImages      245/269 (91.1%)
  summary                139/269 (51.7%)
  weight                 269/269 (100.0%)
  images                 269/269 (100.0%)
  dimensions             247/269 (91.8%)

── Pricing (simple) ──
  sale=True: 25 / 25
  minPriceCents range: $5.95–$31.95
  salePriceCents range: $3.95–$18.99

── Pricing (variable) ──
  min/max/salePriceCents=null: 244/244 (deferred to create_items)

── Stock ──
  stock=0: 33  |  stock=1 (fallback): 203  |  stock>1 (real): 33

── Images ──
  Total: 863  |  per product: min 1 / max 13 / avg 3.2
  Products with no images: 0

── Attributes ──
  Color          244 products  331 unique options
  Frame Color    199 products   19 unique options
  Lens Color     199 products   22 unique options
  Activity       192 products    9 unique options
  Style          192 products    9 unique options
  Lens Type      190 products    9 unique options
  Material       187 products    3 unique options
  Gender          83 products    2 unique options
  Power           82 products   22 unique options
  Brand            7 products    1 unique options
  Size             7 products    2 unique options
  Foam Type        2 products    1 unique options

  unique names: ['Activity', 'Brand', 'Color', 'Foam Type', 'Frame Color', 'Gender', 'Lens Color', 'Lens Type', 'Material', 'Power', 'Size', 'Style']
```
