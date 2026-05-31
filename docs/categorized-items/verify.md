# Categorized Items Verify
_Last updated: 2026-05-31_

**Source:** `reshaped/shaped_items.json` cross-referenced against all three recategorized outputs

---

## Result

**All checks passed.** All 564 shaped items accounted for across buckets. No data loss.

---

## Checks

| Check | Result |
|-------|--------|
| All shaped items accounted for | ✅ |
| No extra items in output | ✅ |
| No item in multiple buckets | ✅ |
| Count integrity (559 + 2 + 3 = 564) | ✅ |
| All paths end at leaf nodes | ✅ |
| No redundant parent paths | ✅ |
| No single-item leaves in categorized output | ✅ |
| No dropped slugs survived | ✅ |
| No merged slugs survived | ✅ |
| Non-category fields unchanged | ✅ |

---

## Counts

| Bucket | Count |
|--------|------:|
| `categorized_items.json` | 559 |
| `no_category_items.json` | 2 |
| `single_leaf_items.json` | 3 |
| **Total** | **564** |
