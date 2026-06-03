# slim-products analysis — proSPORT Sunglasses
_171 products after slimming from fetch-products_

## Field presence

"Filled" means a genuinely valid value — not just the field existing. Dimensions requires all three subfields non-empty. Categories and images require at least one item in the array. `featured` and `total_sales` are always present (False/0 are valid values, not missing).

| Field | Filled | Notes |
|---|---|---|
| `id` | 171/171 | |
| `name` | 171/171 | |
| `slug` | 170/171 | 1 missing — the draft copy product |
| `permalink` | 171/171 | |
| `type` | 171/171 | |
| `status` | 171/171 | |
| `description` | 148/171 | 23 products have no description |
| `short_description` | 35/171 | Sparse — most products don't have one |
| `sku` | 170/171 | 1 simple product missing (`Sunglass String Chum Strap`, id 3139) |
| `price` | 171/171 | |
| `regular_price` | 17/171 | Simple products only |
| `sale_price` | 16/171 | Simple products with active sale only |
| `on_sale` | 171/171 | Unreliable for variable products — see below |
| `featured` | 171/171 | Always present; True on 5 products |
| `total_sales` | 171/171 | Always present; >0 on 80 products, 0 on 91 |
| `stock_quantity` | 19/171 | Only where `manage_stock=True` in raw |
| `stock_status` | 171/171 | |
| `weight` | 18/171 | |
| `dimensions` | 0/171 | Object always present but all subfields are empty strings |
| `categories` | 171/171 | All have at least one category object |
| `images` | 171/171 | All have at least one image object |
| `attributes` | 160/171 | 11 products have no attributes |
| `variations` | 154/171 | 17 simple products have empty array |

## Flags

- **1 draft product** — `proSPORT Cabriolet Mirror Bifocal (Copy)` (id 4019). Excluded at validation.
- **1 product with no SKU** — `Sunglass String Chum Strap` (id 3139, simple). Excluded at validation.
- **dimensions** — 0/171 usable. The field is structurally always present but carries no real data. Drop at reshape.

## type vs variations

Perfectly consistent — no surprises:
- All 154 `variable` products have a non-empty `variations` array
- All 17 `simple` products have an empty `variations` array

`len(variations) > 0` and `type == "variable"` agree on every product. Use `variations` as the source of truth.

## on_sale truthfulness

`on_sale` is unreliable for variable products. 154 products have `on_sale=True` with no `sale_price` — all of them variable. WooCommerce sets it True when any variation is on sale, but the actual price lives on the variation. For simple products it is accurate and agrees with `sale_price` in every case.

## featured

5 products are featured:
- proSPORT Apex Day Vision Polarized Sunglasses (id 2689)
- proSPORT Puma Bifocal (id 2056)
- proSPORT Methane Bifocal (id 2037)
- proSPORT Taxi Polarized Bifocal (id 1493)
- proSPORT Commando Polarized Bifocal (id 1476)

## total_sales

- Has sales (>0): 80 products
- Zero sales: 91 products
- Top values: 1×22, 2×11, 3×12, 4×11, 7×5

`0` means either no sales or untracked — treat it as unknown, not confirmed zero.

## Stock: quantity vs status

`stock_status` is the source of truth. `stock_quantity` is only populated on 19 products where the store actively tracks inventory.

| Combination | Count |
|---|---|
| no quantity + instock | 150 |
| no quantity + outofstock | 2 |
| has quantity + instock | 10 |
| has quantity + outofstock | 9 |

The 2 products that are `outofstock` with no quantity (`proSPORT Navigator Rimless HD Copper` and `proSPORT Eagle Eye HD Copper`) have no quantity signal at all — `stock_status` is the only way to know they're unavailable.

## Categories

11 unique categories. Every product carries **Uncategorized** alongside its real category — drop it at reshape.

| Category | Products |
|---|---|
| Uncategorized | 171 |
| READERS SPECIAL FIT | 68 |
| BIFOCALS | 46 |
| POLARIZED | 36 |
| SPORT | 31 |
| FULL LENS | 24 |
| HD COPPER | 15 |
| CLEAR & YELLOW | 11 |
| STREET | 10 |
| METALS & AVIATORS | 6 |
| BIG & TALL | 2 |

