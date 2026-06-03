import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand


brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]
data_dir = BASE / "data" / slug

items = json.loads((data_dir / "categorize-items" / "items.json").read_text())

def pct(n, total):
    return f"{n}/{total} ({100*n/total:.1f}%)" if total else "0/0"

SEP  = "=" * 60
DASH = "─" * 60

print(SEP)
print(f"  CATEGORIZE ITEMS AUDIT — {brand_name}")
print(SEP)
print(f"  Items: {len(items)}")

# ── Leaf counts ───────────────────────────────────────────────────────────────
print(f"\n── Leaf category counts ──")
leaf_counter = Counter(
    path[-1]["slug"]
    for p in items
    for path in p["categories"]
)
for leaf_slug, count in sorted(leaf_counter.items(), key=lambda x: -x[1]):
    leaf_name = path[-1]["name"] if False else next(
        path[-1]["name"] for p in items for path in p["categories"] if path[-1]["slug"] == leaf_slug
    )
    print(f"  {leaf_name:<25} {count:>4} products")
print(f"\n  Total leaf assignments : {sum(leaf_counter.values())}")
print(f"  Unique leaves used     : {len(leaf_counter)}")

# ── Parent counts ─────────────────────────────────────────────────────────────
print(f"\n── Parent category counts ──")
parent_counter = Counter(
    path[0]["slug"]
    for p in items
    for path in p["categories"]
    if len(path) == 2
)
for parent_slug, count in sorted(parent_counter.items(), key=lambda x: -x[1]):
    parent_name = next(
        path[0]["name"] for p in items for path in p["categories"]
        if len(path) == 2 and path[0]["slug"] == parent_slug
    )
    print(f"  {parent_name:<25} {count:>4} products")

# ── Path count distribution ───────────────────────────────────────────────────
print(f"\n── Paths per product ──")
path_counts = Counter(len(p["categories"]) for p in items)
for n, count in sorted(path_counts.items()):
    print(f"  {n} path(s): {count} products")

# ── Multi-leaf products ───────────────────────────────────────────────────────
multi = [(p["id"], p["name"], [path[-1]["name"] for path in p["categories"]]) for p in items if len(p["categories"]) > 1]
print(f"\n── Multi-leaf products ({len(multi)}) ──")
combo_counter = Counter(tuple(sorted(leaves)) for _, _, leaves in multi)
print(f"  Unique leaf combinations: {len(combo_counter)}")
for combo, count in combo_counter.most_common():
    print(f"  {count:>3}x  {' + '.join(combo)}")

# ── Path depth distribution ───────────────────────────────────────────────────
print(f"\n── Path depth distribution ──")
depth_counter = Counter(
    len(path)
    for p in items
    for path in p["categories"]
)
for depth, count in sorted(depth_counter.items()):
    label = "root-level (no parent)" if depth == 1 else "child (has parent)"
    print(f"  depth {depth} — {label}: {count} paths")

# ── Products with no categories ───────────────────────────────────────────────
no_cat = [p for p in items if not p["categories"]]
print(f"\n── Products with no categories: {len(no_cat)} ──")

# ── Per-leaf product list ─────────────────────────────────────────────────────
print(f"\n── Products per leaf ──")
leaf_products = defaultdict(list)
for p in items:
    for path in p["categories"]:
        leaf_products[path[-1]["name"]].append(f"id={p['id']} {p['name'][:45]}")
for leaf_name in sorted(leaf_products):
    print(f"\n  [{leaf_name}] ({len(leaf_products[leaf_name])} products)")
    for entry in sorted(leaf_products[leaf_name]):
        print(f"    {entry}")
