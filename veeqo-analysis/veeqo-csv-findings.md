# Veeqo CSV Findings
_Source: `sellables_export_2715106881-522cca85784aae20260606-23-66wn2d_original.csv` — analyzed Jun 5, 2026_

---

## Overview

| | Count |
|---|---|
| Total rows | 25,008 |
| Rows with SKU | 24,897 |
| Rows without SKU | 111 |
| Unique SKUs | 24,396 |

---

## SKU Quality

| SKU quality | Count | Flagged? |
|---|---|---|
| Clean | 22,332 | No |
| Contains spaces | 2,029 | No — acknowledged, they connect and work |
| Placeholders (`none*` / all-digit) | 35 | Yes |

**Contains spaces** — two sub-types:
- Informal descriptive names with no structure: `"cobra smoke"`, `"clutch full reader 1.0blk"`, `"Bandanna - Black"` — products entered with human-readable names instead of proper codes
- Typo'd real SKUs: e.g. `"CRE59X22DE- BKXBK-CL-100-MFS"` — a space entered after the hyphen

**Placeholders:**
- `none` / `none1`–`none30` — Amazon listings created without a real SKU. The same placeholder is reused across different products, causing collisions and price conflicts.
- `204150`, `204200`, `204250`, `204300` — all-digit codes, likely vendor/supplier reference numbers, not product SKUs.

---

## Duplicates

| | Count |
|---|---|
| SKUs appearing 2+ times | 431 |
| Of which, price differs | 162 — flagged |
| Same-price duplicates | 269 — not flagged |

A SKU can be listed under multiple channel listings (e.g. two separate eBay listings for the same SKU). Veeqo creates a separate row per listing — same-price duplicates are expected and not a problem. Only duplicates where the price differs across rows are flagged, as they indicate the same product is being sold at different prices on different channels.

---

## Price

| | Rows | % |
|---|---|---|
| Non-zero price | 24,839 | 99.8% |
| Zero price | 56 SKUs | — flagged |
| No price | 0 | — |

- Range: $2.84 – $399.00
- Mean: $40.01

---

## Stock

| | Rows | % |
|---|---|---|
| Zero stock | 10,056 | 40.4% |
| Positive stock | 14,738 | 59.2% |
| **Total qty on hand** | **111,777** | |

40% of rows have zero stock. Stock is unreliable as a migration signal — many valid active products show 0.

---

## Rows Without SKU (111)

These rows have other fields populated (title, price, etc.) but `sku_code` is empty. They should either be assigned a real SKU or deleted.

Heavy on Rx option add-ons (~30 rows: single vision, progressive, A/R, mirror coatings, transitions, prism, lens remake fees). The rest are a mix of operational and miscellaneous eBay/Amazon listings:

| Category | Examples |
|---|---|
| Rx option add-ons | Rx Option: Single Vision Digital Lens, Rx Option: Progressive Digital Lens, Rx Option: Classic A/R, Rx OptionM: Flash Mirror - Pink/Red/Green/Gold/Silver/Rose Gold, Rx Option: Transitions Gen 8, etc. |
| 7eye Replacement Foam | 7 Eye Replacement Foam (3 rows), 7eye Replacement Foam |
| Bulk sunglass lots | 28 pairs motorcycle riding sunglasses, Sunglass Mens 3 Pairs Square Black Frame, Women SUNGLASSES Wholesale Lot 26 pairs, etc. |
| Operational / service | Custom Product for Phone Orders, Distributor Invoice, Expedited Shipping, Misc Frame, Misc Shipping Cost, Prism Custom Fee, Product Upgrade, Quick product, Try Before You Buy Rx Order, Try Before You Buy: WileyX 7eye BikerArmou |
| Nike / sporting goods | 2 PAIRS Nike Dri Fit Shorts, 3 Nike Men's Dri Fit Shorts, Nike Sportswear STORM-FIT ADV Shell Parka, Nike Pants Womens Medium, etc. |
| Face masks / shields | 10 pcs Kids Face Mask, 12 SHIELDS FOR KIDS!, 13/15/38/5 Face Mask packs, Space Shield Clear Face Mask, Childrens Boys Girls Flip UP Shield |
| Misc | Playing cards, baseball hat, toner cartridges, refrigerator part, Spyder tail lights, Steph Curry poster, Medical Laboratory Goggle, Reseller: POP 36 Display Stand, Reseller: BikerArmour Sunglasses |
