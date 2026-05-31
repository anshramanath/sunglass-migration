# Categorized Items Verification
_Last updated: 2026-05-30_

**Source:** `recategorized/` — all three output files
**Script:** `migration/qa/verify_categorized_items.py`

---

## Result

**All checks passed.** 586 shaped items fully accounted for across three output buckets.

---

## Checks

| Check | Result |
|-------|--------|
| All shaped items accounted for | ✅ |
| No extra items in output | ✅ |
| No item in multiple buckets | ✅ |
| Count integrity: 581 + 2 + 3 = 586 | ✅ |
| All paths end at leaf nodes — no item assigned to a branch node | ✅ |
| No redundant parent paths — no path is a prefix of another path for the same item | ✅ |
| No single-item leaves remaining in categorized output | ✅ |
| No dropped slugs survived into output | ✅ |
| No merged slugs survived into output | ✅ |
| Non-category fields unchanged during recategorization | ✅ |

---

## Counts

| Bucket | Count |
|--------|------:|
| `categorized_items.json` | 581 |
| `no_category_items.json` | 2 |
| `single_leaf_items.json` | 3 |
| **Total** | **586** |

---

## Flagged buckets

### no_category_items.json (2)
Only category was `all-products` which was dropped. Pending owner review.

| SKU | Name |
|-----|------|
| `BF4X05PC-0` | Pacific Mirror Bifocal |
| `SRE81X13JS-0` | Jersey Sunglass Reader |

### single_leaf_items.json (3)
Only item assigned to their leaf category. A nav button with a single product behind it — pending owner review to reassign or confirm.

| SKU | Name | Original leaf |
|-----|------|--------------|
| `FM63X32PK-0` | BikerArmour Pinkie [SM – MED] | `rhinestones` |
| `clothmasks` | PM 2.5 Medical Face Masks | `safety-protection` |
| `CH8CP901-0` | Chopper 901 Fits SM-LG | `chopper` |
