import json
import sys
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(line_buffering=True)

BASE = Path(__file__).parent.parent  # migration/

with open(BASE / "reshaped/shaped_items.json", encoding="utf-8") as f:
    shaped = json.load(f)

with open(BASE / "recategorized/categorized_items.json", encoding="utf-8") as f:
    categorized = json.load(f)

with open(BASE / "recategorized/no_category_items.json", encoding="utf-8") as f:
    no_cat = json.load(f)

with open(BASE / "recategorized/single_leaf_items.json", encoding="utf-8") as f:
    single_leaf = json.load(f)

errors = []
ok = []

def check(name, passed, detail=""):
    if passed:
        ok.append(name)
    else:
        errors.append(f"{name}{': ' + detail if detail else ''}")

shaped_skus = {item["sku"] for item in shaped}
categorized_skus = {item["sku"] for item in categorized}
no_cat_skus = {item["sku"] for item in no_cat}
single_leaf_skus = {item["sku"] for item in single_leaf}
output_skus = categorized_skus | no_cat_skus | single_leaf_skus

# ── 1. All shaped items accounted for ────────────────────────────────────────

missing = shaped_skus - output_skus
extra = output_skus - shaped_skus
check("All shaped items accounted for", not missing, f"{len(missing)} missing: {list(missing)[:3]}")
check("No extra items in output", not extra, f"{list(extra)[:3]}")

# ── 2. No item in multiple buckets ───────────────────────────────────────────

overlap = (categorized_skus & no_cat_skus) | (categorized_skus & single_leaf_skus) | (no_cat_skus & single_leaf_skus)
check("No item in multiple buckets", not overlap, f"{list(overlap)[:3]}")

# ── 3. Count integrity ────────────────────────────────────────────────────────

actual = len(categorized) + len(no_cat) + len(single_leaf)
check(f"Count integrity ({len(categorized)} + {len(no_cat)} + {len(single_leaf)} = {actual})",
      actual == len(shaped), f"expected {len(shaped)}")

# ── 4. All paths end at leaf nodes (no branch-node assignments) ───────────────

all_links = set()
for item in categorized:
    for path in item.get("categories", []):
        slugs = [n["slug"] for n in path]
        for i in range(len(slugs)):
            all_links.add("/".join(slugs[:i+1]))

non_leaf_slugs = set()
for link in all_links:
    parent = "/".join(link.split("/")[:-1])
    if parent:
        non_leaf_slugs.add(parent.split("/")[-1])

branch_violations = []
for item in categorized:
    for path in item.get("categories", []):
        leaf_slug = path[-1]["slug"]
        if leaf_slug in non_leaf_slugs:
            branch_violations.append((item["sku"], leaf_slug))

check("All paths end at leaf nodes (no branch-node assignments)", not branch_violations,
      f"{len(branch_violations)} violations: {branch_violations[:3]}")

# ── 5. No redundant parent paths (no path is prefix of another) ──────────────

redundant = []
for item in categorized:
    paths = item.get("categories", [])
    slug_paths = [[n["slug"] for n in p] for p in paths]
    for i, a in enumerate(slug_paths):
        for j, b in enumerate(slug_paths):
            if i != j and len(b) > len(a) and b[:len(a)] == a:
                redundant.append((item["sku"], a, b))

check("No redundant parent paths (no path is prefix of another)", not redundant,
      f"{len(redundant)} found: {redundant[:2]}")

# ── 6. No single-item leaves remaining in categorized output ──────────────────

leaf_counts = Counter()
for item in categorized:
    for path in item.get("categories", []):
        slugs = tuple(n["slug"] for n in path)
        leaf_counts[slugs] += 1

single_item_leaves = [(item["sku"], tuple(n["slug"] for n in path))
                      for item in categorized
                      for path in item.get("categories", [])
                      if leaf_counts[tuple(n["slug"] for n in path)] == 1]

check("No single-item leaves in categorized output", not single_item_leaves,
      f"{len(single_item_leaves)} found: {single_item_leaves[:2]}")

# ── 7. Dropped slugs did not survive ─────────────────────────────────────────

DROP_SLUGS = {"see-all-brands","see-all-rx-frames","see-all-eclipse-xt-frames",
              "see-all-try-before-you-buy","all-products","got-frames"}
drop_survivors = [(item["sku"], n["slug"])
                  for item in categorized
                  for path in item.get("categories", [])
                  for n in path if n["slug"] in DROP_SLUGS]
check("No dropped slugs survived into output", not drop_survivors,
      f"{drop_survivors[:3]}")

# ── 8. Merged slugs did not survive ──────────────────────────────────────────

MERGED_SLUGS = {"mirrored","small-medium-shop-by-head-size","low-nose-bridge-long-lashes-shades","bifocal-type"}
merge_survivors = [(item["sku"], n["slug"])
                   for item in categorized
                   for path in item.get("categories", [])
                   for n in path if n["slug"] in MERGED_SLUGS]
check("No merged slugs survived into output", not merge_survivors,
      f"{merge_survivors[:3]}")

# ── 9. Non-category fields unchanged ─────────────────────────────────────────

shaped_map = {item["sku"]: item for item in shaped}
field_changes = []
for item in categorized:
    original = shaped_map.get(item["sku"])
    if not original:
        continue
    for field in ["name","slug","minPriceCents","maxPriceCents","salePriceCents","sale","inStock","weight"]:
        if item.get(field) != original.get(field):
            field_changes.append(f"{item['sku']}.{field}")
check("Non-category fields unchanged during recategorization", not field_changes,
      f"{field_changes[:3]}")

# ── Report ────────────────────────────────────────────────────────────────────

print("=" * 60)
print("  CATEGORIZED ITEMS VERIFICATION")
print("=" * 60)
print(f"  Shaped:       {len(shaped)}")
print(f"  Categorized:  {len(categorized)}")
print(f"  No-category:  {len(no_cat)}")
print(f"  Single-leaf:  {len(single_leaf)}")
print(f"  Total:        {actual}")
print()
for name in ok:
    print(f"  ✓ {name}")
print()
if errors:
    print(f"  ✗ {len(errors)} check(s) failed:")
    for e in errors:
        print(f"    · {e}")
else:
    print("  ALL CHECKS PASSED")
