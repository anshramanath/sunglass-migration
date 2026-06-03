# Category tree — initial (run 2, proSPORT Sunglasses)
_2026-06-03_

WooCommerce categories unchanged from run-1. Tree structure and leaf assignments unchanged.
New in run-2: `sortOrder` added to every node, hardcoded by slug in the categorize script.

---

## Proposed tree with sort orders

Sort order resets per parent — each number is relative to siblings only.
Root-level sort order determines navbar button order.

```
1  Shop By Style
   ├── 1  Sport
   ├── 2  Street
   └── 3  Metal and Aviators

2  Lens Color
   ├── 1  Polarized
   ├── 2  Hd Copper
   └── 3  Clear and Yellow

3  Readers Special Fit
   ├── 1  Bifocals
   └── 2  Full Lens

4  Accessories
```

---

## Slug → sortOrder mapping (what gets hardcoded)

| Slug | Sort Order | Parent |
|------|-----------|--------|
| `shop-by-style` | 1 | root |
| `lens-color` | 2 | root |
| `readers-special-fit` | 3 | root |
| `accessories` | 4 | root |
| `sport` | 1 | shop-by-style |
| `street` | 2 | shop-by-style |
| `metal-and-aviators` | 3 | shop-by-style |
| `polarized` | 1 | lens-color |
| `hd-copper` | 2 | lens-color |
| `clear-and-yellow` | 3 | lens-color |
| `bifocals` | 1 | readers-special-fit |
| `full-lens` | 2 | readers-special-fit |
