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

ACCESSORIES (12)
```
