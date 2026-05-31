import json
import sys
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(line_buffering=True)

BASE = Path(__file__).parent.parent  # migration/

with open(BASE / "recategorized/categorized_items.json", encoding="utf-8") as f:
    items = json.load(f)

with open(BASE / "recategorized/no_category_items.json", encoding="utf-8") as f:
    no_cat = json.load(f)

total = len(items)
issues = defaultdict(list)

def flag(field, sku, detail=""):
    issues[field].append((sku, detail))

for item in items:
    sku = item.get("sku", "UNKNOWN")
    categories = item.get("categories", [])

    # Must have at least one category path
    if not categories:
        flag("categories[empty]", sku)
        continue

    for i, path in enumerate(categories):
        # Each path must be a non-empty list
        if not isinstance(path, list) or not path:
            flag("categories[path_empty]", sku, f"path index {i}")
            continue

        # Levels must be sequential starting at 1
        expected_levels = list(range(1, len(path) + 1))
        actual_levels = [node.get("level") for node in path]
        if actual_levels != expected_levels:
            flag("categories[bad_levels]", sku, f"expected {expected_levels} got {actual_levels}")

        for node in path:
            if not node.get("name"):
                flag("categories[node_name_blank]", sku, f"level {node.get('level')}")
            if not node.get("slug"):
                flag("categories[node_slug_blank]", sku, f"level {node.get('level')}")

    # Check for duplicate paths
    path_tuples = [tuple(n.get("slug") for n in p) for p in categories]
    if len(path_tuples) != len(set(path_tuples)):
        flag("categories[duplicate_paths]", sku)

# ── Report ────────────────────────────────────────────────────────────────────

print("=" * 60)
print("  CATEGORIZED ITEMS AUDIT")
print("=" * 60)
print(f"  Categorized items:   {total}")
print(f"  No-category items:   {len(no_cat)}")
print()

if not issues:
    print("  ✓ No issues found")
else:
    print("── ISSUES ──")
    for field, entries in sorted(issues.items()):
        print(f"\n  {field}")
        print(f"  {len(entries)} affected")
        for sku, detail in entries[:5]:
            print(f"    · {sku}" + (f"  {detail}" if detail else ""))
        if len(entries) > 5:
            print(f"    ... and {len(entries) - 5} more")

print()
print("── CATEGORY TREE STATS ──")

# Count items per root (level 1 slug)
root_counts = defaultdict(int)
depth_counts = defaultdict(int)

for item in items:
    for path in item.get("categories", []):
        root_counts[path[0]["slug"]] += 1
        depth_counts[len(path)] += 1

print("\n  Items per root category:")
for slug, count in sorted(root_counts.items(), key=lambda x: -x[1]):
    print(f"    {slug:<35}  {count}")

print("\n  Path depth distribution:")
for depth, count in sorted(depth_counts.items()):
    print(f"    depth {depth}: {count} assignments")

print()
print("── NO-CATEGORY ITEMS ──")
if no_cat:
    for item in no_cat:
        print(f"  [{item.get('sku')}] {item.get('name')}")
else:
    print("  None")
