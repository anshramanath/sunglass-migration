# Category tree — proSPORT Sunglasses

Max depth: 1 hop from root (2 levels). A product can appear in multiple branches — counts can sum to more than the unique product count.

## Before

```
SHOP BY STYLE
├── SPORT (31)
├── STREET (10)
└── METAL & AVIATORS (6)

LENS COLOR
├── POLARIZED (36)
├── HD COPPER (15)
└── CLEAR & YELLOW (11)

READERS SPECIAL FIT
├── BIFOCALS (44)
└── FULL LENS (23)

NEW ARRIVALS
├── BIG & TALL (2)
├── SMALL & PETIT (0)
└── ASIAN FIT (0)

Uncategorized (21)
```

## After collapse

NEW ARRIVALS is dropped. Both BIG & TALL products already appear elsewhere in the tree (Conquest Wide → STREET, El Capitan → SPORT) so their counts there are unchanged. The 2 products simply lose the BIG & TALL tag — no products become newly homeless.

```
SHOP BY STYLE
├── SPORT (31)
├── STREET (10)
└── METAL & AVIATORS (6)

LENS COLOR
├── POLARIZED (36)
├── HD COPPER (15)
└── CLEAR & YELLOW (11)

READERS SPECIAL FIT
├── BIFOCALS (44)
└── FULL LENS (23)

Uncategorized (21)
```

---

## Plan for 21 homeless products

### Sunglasses (9) — assign a leaf category

| id | Product | Suggested |
|---|---|---|
| 2887 | proSPORT Apollo Safety Wrap Sunglasses | FULL LENS (has Power attribute → reader) |
| 1160 | proSPORT Yogi Mirror Aviator Sunglasses | METAL & AVIATORS |
| 1184 | proSPORT Mako Metal Mirror Sunglasses | METAL & AVIATORS |
| 1165 | Zulu Metal Fashion Sunglasses | METAL & AVIATORS |
| 1224 | Brandy | METAL & AVIATORS |
| 1179 | Carmen Fashion Sunglasses | STREET |
| 1189 | Popcat | STREET |
| 1170 | Miami Square Fashion Sunglasses | STREET |
| 1175 | proSPORT Kuna | STREET |

### Cases & accessories (12) → ACCESSORIES

| id | Product |
|---|---|
| 2905 | Leopard Print Hard Case |
| 2904 | Ruby Extra Large Zipper Case |
| 2899 | Jade Deep Fabric Case |
| 2898 | Garnet Deep Zipper Case with Clipper |
| 2778 | Diamond Chrome Hard Case |
| 2773 | Ametrine Medium Leather Hard Case |
| 2772 | Hematite Small Shiny - Leather Case |
| 2768 | Citrine Woody - Hard Case |
| 2749 | Agate Lady Black Extra Large - Leather Case |
| 2748 | Sunglasses Repair Kit |
| 2747 | Sunglasses Repair Screw Driver - Key Chain |
| 2746 | Sunglasses Lens Cleaner - Spray Bottle |

---

## After recategorize

```
SHOP BY STYLE
├── SPORT (31)
├── STREET (14)
└── METAL & AVIATORS (10)

LENS COLOR
├── POLARIZED (36)
├── HD COPPER (15)
└── CLEAR & YELLOW (11)

READERS SPECIAL FIT
├── BIFOCALS (44)
└── FULL LENS (24)

Accessories (12)
```

---

## Naming convention

- **Name**: title case — first letter of every word capitalised, except `and` which stays lowercase. e.g. `Readers Special Fit`, `Metal and Aviators`
- **Slug**: derived from name — `name.lower().replace(' ', '-')` e.g. `readers-special-fit`
- **Round-trip checks**:
  - `slugify(name)` = `name.lower().replace(' ', '-')`
  - `namify(slug)` = capitalise first letter of each `-`-separated word, except `and`
  - `slugify(name) == slug` and `namify(slug) == name` must both hold
- `&` is not allowed in names — use `and` instead so the round-trip is clean

## Category name map (old → new)

| Old (WooCommerce) | New name | New slug |
|---|---|---|
| SHOP BY STYLE | Shop By Style | shop-by-style |
| SPORT | Sport | sport |
| STREET | Street | street |
| METALS & AVIATORS / METAL & AVIATORS | Metal and Aviators | metal-and-aviators |
| LENS COLOR | Lens Color | lens-color |
| POLARIZED | Polarized | polarized |
| HD COPPER | Hd Copper | hd-copper |
| CLEAR & YELLOW | Clear and Yellow | clear-and-yellow |
| READERS SPECIAL FIT | Readers Special Fit | readers-special-fit |
| BIFOCALS | Bifocals | bifocals |
| FULL LENS | Full Lens | full-lens |
| NEW ARRIVALS | — dropped — | — |
| BIG & TALL | — dropped — | — |
| Uncategorized | — dropped — | — |
| *(new)* | Accessories | accessories |

## Category structure per product

`categories` is an array of path arrays. Each path is its own array — parent and child are always paired together, no ambiguity when a product sits at multiple leaves.

Single leaf with parent:
```json
[
  [
    { "level": 1, "name": "Readers Special Fit", "slug": "readers-special-fit" },
    { "level": 2, "name": "Bifocals", "slug": "bifocals" }
  ]
]
```

Root-level leaf (no parent):
```json
[
  [
    { "level": 1, "name": "Accessories", "slug": "accessories" }
  ]
]
```

Product at two leaves:
```json
[
  [
    { "level": 1, "name": "Lens Color", "slug": "lens-color" },
    { "level": 2, "name": "Hd Copper", "slug": "hd-copper" }
  ],
  [
    { "level": 1, "name": "Shop By Style", "slug": "shop-by-style" },
    { "level": 2, "name": "Sport", "slug": "sport" }
  ]
]
```
