# Categorized Items Audit
_Last updated: 2026-05-30_

**Source:** `recategorized/categorized_items.json`
**Script:** `migration/qa/audit_categorized_items.py`

---

## Result

**Zero issues.** All 584 categorized items have valid category paths. All path levels, names, and slugs are well-formed.

---

## Counts

| | Count |
|---|---:|
| Shaped items (input) | 586 |
| Categorized items | 584 |
| No-category items | 2 |
| Total category assignments | 1,316 |

Items can appear in multiple root categories — total assignments exceed item count.

---

## Trees

**8 root categories.** Height = number of levels from root to deepest leaf (root alone = height 1).

| Root | Display Name | Height | Unique Items | Total Assignments |
|------|-------------|-------:|-------------:|------------------:|
| `sunglasses` | Sunglasses | 3 | 315 | 775 |
| `prescription` | Prescription | 3 | 94 | 204 |
| `transitions` | Transitions | 3 | 85 | 92 |
| `bifocals` | Bifocals | 2 | 92 | 192 |
| `accessories` | Accessories | 2 | 13 | 24 |
| `sale` | Sale | 1 | 12 | 12 |
| `combo-sets` | Combo Sets | 1 | 10 | 10 |
| `try-before-you-buy` | Try Before You Buy | 1 | 7 | 7 |

---

## Path depth distribution

| Depth | Assignments | Notes |
|------:|------------:|-------|
| 1 | 225 | Root-level only (e.g. `sale`, `combo-sets`, parent-level assignments) |
| 2 | 246 | Two levels deep (e.g. `sunglasses → lens-type`) |
| 3 | 845 | Three levels deep (e.g. `sunglasses → brands → prosport`) |

---

## No-category items

These 2 items had all their WooCommerce category links dropped during recategorization (their only category was `all-products`). Pending owner review.

| SKU | Name |
|-----|------|
| `BF4X05PC-0` | Pacific Mirror Bifocal |
| `SRE81X13JS-0` | Jersey Sunglass Reader |
