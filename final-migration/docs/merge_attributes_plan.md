# Attribute Name Merge Plan

Attribute names are normalised after removing items in `remove_items.md`. All counts are number of products carrying that attribute.

Target names: `color`, `power`, `quantity`, `transition`, `size`

---

## Merge map

| Original name | Merges to |
|---|---|
| Choose Color (REQUIRED) | color |
| Choose Color | color |
| Color | color |
| Choose Frame Color (Required) | color |
| Choose Bandana Color | color |
| Choose Power | power |
| Qty | quantity |
| Choose Quantity | quantity |
| Cleaner Spray Bottle QTY | quantity |
| Qty (packs of 3) | quantity |
| Choose Transition Type | transition |
| Choose Size | size |

---

## proSPORT

| Attribute | Before | After removal | After merge |
|---|---|---|---|
| Choose Color | 139 | 139 | — |
| Choose Power | 58 | 58 | — |
| **color** | — | — | 139 |
| **power** | — | — | 58 |

No items removed from proSPORT. No change from removal step.

---

## Monster

| Attribute | Before | After removal | After merge |
|---|---|---|---|
| Choose Color (REQUIRED) | 237 | 237 | — |
| Choose Power | 80 | 80 | — |
| Qty | 2 | 2 | — |
| Color | 1 | 1 | — |
| Choose Color | 1 | 1 | — |
| Choose Quantity | 1 | — | — |
| Cleaner Spray Bottle QTY | 1 | — | — |
| Choose Bandana Color | 1 | 1 | — |
| **color** | — | — | 239 |
| **power** | — | — | 80 |
| **quantity** | — | — | 2 |

Removal drops `Choose Quantity` and `Cleaner Spray Bottle QTY` (both were only on the VShield product).

---

## BikerShades

| Attribute | Before | After removal | After merge |
|---|---|---|---|
| Choose Color (REQUIRED) | 447 | 447 | — |
| Choose Power | 91 | 91 | — |
| Choose Transition Type | 74 | 74 | — |
| Choose Frame Color (Required) | 1 | 1 | — |
| Choose Bandana Color | 1 | 1 | — |
| Choose 7 Eye Style | 1 | — | — |
| Shipping Option | 1 | — | — |
| Choose Color | 1 | — | — |
| Choose Quantity | 1 | — | — |
| Cleaner Spray Bottle QTY | 1 | — | — |
| Qty (packs of 3) | 1 | 1 | — |
| Choose Size | 1 | 1 | — |
| **color** | — | — | 449 |
| **power** | — | — | 91 |
| **transition** | — | — | 74 |
| **color** | — | — | 449 |
| **power** | — | — | 91 |
| **transition** | — | — | 74 |
| **quantity** | — | — | 1 |
| **size** | — | — | 1 |

Removal drops `Choose 7 Eye Style`, `Shipping Option`, `Choose Color`, `Choose Quantity`, and `Cleaner Spray Bottle QTY`.

> **Note:** When merging `Qty (packs of 3)` into `quantity`, the option values must also be rewritten: `1 pack (3 masks total)` → `3 masks`, `2 packs (6 masks total)` → `6 masks`, `5 packs (15 masks total)` → `15 masks`, `10 packs (30 masks total)` → `30 masks`.
