import copy
import html
import json
import os
from collections import Counter
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).parent.parent
load_dotenv(dotenv_path=BASE.parent / ".env")

BRAND_CONFIG = {
    "proSPORT Sunglasses": {"slug": "prosport"},
}

brand_name = os.getenv("BRAND")
config = BRAND_CONFIG.get(brand_name)
if not config:
    raise SystemExit(f"Unknown BRAND={brand_name!r}. Add it to BRAND_CONFIG.")

slug = config["slug"]
data_dir = BASE / "data" / slug

in_path = data_dir / "create-items" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run create_items.py first. Not found: {in_path}")

items_raw = json.loads(in_path.read_text())

out_dir = data_dir / "categorize-items"
out_dir.mkdir(parents=True, exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

def slugify(name):
    return name.lower().replace(" ", "-")

def namify(s):
    return " ".join(w if w == "and" else w.capitalize() for w in s.replace("-", " ").split())


# ── Config ────────────────────────────────────────────────────────────────────

# After html.unescape(): old WC name → (new name, new slug) or None to drop
RENAME_MAP = {
    "Uncategorized":       None,
    "BIG & TALL":          None,
    "BIFOCALS":            ("Bifocals",            "bifocals"),
    "CLEAR & YELLOW":      ("Clear and Yellow",    "clear-and-yellow"),
    "FULL LENS":           ("Full Lens",           "full-lens"),
    "HD COPPER":           ("Hd Copper",           "hd-copper"),
    "METALS & AVIATORS":   ("Metal and Aviators",  "metal-and-aviators"),
    "METAL & AVIATORS":    ("Metal and Aviators",  "metal-and-aviators"),
    "POLARIZED":           ("Polarized",           "polarized"),
    "READERS SPECIAL FIT": ("Readers Special Fit", "readers-special-fit"),
    "SPORT":               ("Sport",               "sport"),
    "STREET":              ("Street",              "street"),
}

# Leaf slug → (parent name, parent slug) or None for root-level leaves
TREE = {
    "bifocals":            ("Readers Special Fit", "readers-special-fit"),
    "full-lens":           ("Readers Special Fit", "readers-special-fit"),
    "sport":               ("Shop By Style",       "shop-by-style"),
    "street":              ("Shop By Style",       "shop-by-style"),
    "metal-and-aviators":  ("Shop By Style",       "shop-by-style"),
    "polarized":           ("Lens Color",          "lens-color"),
    "hd-copper":           ("Lens Color",          "lens-color"),
    "clear-and-yellow":    ("Lens Color",          "lens-color"),
    "accessories":         None,
}

LEAF_SLUGS   = set(TREE.keys())
PARENT_SLUGS = {v[1] for v in TREE.values() if v}

# proSPORT-specific: id → leaf slug for uncategorized products
HARDCODED = {
    # sunglasses
    2887: "full-lens",
    1160: "metal-and-aviators",
    1184: "metal-and-aviators",
    1165: "metal-and-aviators",
    1224: "metal-and-aviators",
    1179: "street",
    1189: "street",
    1170: "street",
    1175: "street",
    # cases & accessories
    2905: "accessories",
    2904: "accessories",
    2899: "accessories",
    2898: "accessories",
    2778: "accessories",
    2773: "accessories",
    2772: "accessories",
    2768: "accessories",
    2749: "accessories",
    2748: "accessories",
    2747: "accessories",
    2746: "accessories",
}


# ── Process ───────────────────────────────────────────────────────────────────

items = copy.deepcopy(items_raw)
unknown_names = set()

for item in items:
    pid = item["id"]

    # Pass 1: HTML decode + rename → collect normalized leaf slugs
    norm_slugs = set()
    for cat in item.get("categories", []):
        decoded = html.unescape(cat["name"])
        if decoded not in RENAME_MAP:
            unknown_names.add(decoded)
            continue
        mapped = RENAME_MAP[decoded]
        if mapped is None:
            continue
        norm_slugs.add(mapped[1])

    # Keep only leaf slugs — parent slugs (e.g. readers-special-fit from WC) are discarded
    leaf_slugs = norm_slugs & LEAF_SLUGS

    # Pass 2: hardcoded assignments for uncategorized products
    if pid in HARDCODED:
        leaf_slugs.add(HARDCODED[pid])

    # Pass 3: build path arrays
    paths = []
    for leaf_slug in sorted(leaf_slugs):
        leaf_name = namify(leaf_slug)
        parent = TREE[leaf_slug]
        if parent:
            parent_name, parent_slug = parent
            path = [
                {"level": 1, "name": parent_name, "slug": parent_slug},
                {"level": 2, "name": leaf_name,   "slug": leaf_slug},
            ]
        else:
            path = [
                {"level": 1, "name": leaf_name, "slug": leaf_slug},
            ]
        paths.append(path)

    item["categories"] = paths


# ── Checks ────────────────────────────────────────────────────────────────────

errors = []

# Unknown WC category names encountered
if unknown_names:
    for name in sorted(unknown_names):
        errors.append(f"Unknown WC category name (add to RENAME_MAP): {name!r}")

# Every input product is in output
input_ids  = {p["id"] for p in items_raw}
output_ids = {p["id"] for p in items}
for pid in sorted(input_ids - output_ids):
    errors.append(f"id={pid} missing from output")

# Every product has at least one category path
for p in items:
    if not p["categories"]:
        errors.append(f"id={p['id']} {p['name'][:45]!r} has no categories")

# Only leaves at the deepest level of each path — no product ends at a parent
for p in items:
    for path in p["categories"]:
        deepest = path[-1]["slug"]
        if deepest not in LEAF_SLUGS:
            errors.append(f"id={p['id']}: path ends at non-leaf {deepest!r}")
        if deepest in PARENT_SLUGS:
            errors.append(f"id={p['id']}: path ends at parent slug {deepest!r}")

# No duplicate leaf slugs within a single product
for p in items:
    seen = [path[-1]["slug"] for path in p["categories"]]
    if len(seen) != len(set(seen)):
        dupes = [s for s in set(seen) if seen.count(s) > 1]
        errors.append(f"id={p['id']}: duplicate leaf slugs {dupes}")

# Round-trip: namify(slug) == name for every category entry
for p in items:
    for path in p["categories"]:
        for entry in path:
            expected = namify(entry["slug"])
            if expected != entry["name"]:
                errors.append(
                    f"id={p['id']}: namify({entry['slug']!r}) = {expected!r} != {entry['name']!r}"
                )

if errors:
    print("CHECKS FAILED:")
    for e in errors:
        print(f"  {e}")
    raise SystemExit(1)


# ── Write output ──────────────────────────────────────────────────────────────

(out_dir / "items.json").write_text(json.dumps(items, indent=2, ensure_ascii=False))


# ── Summary ───────────────────────────────────────────────────────────────────

leaf_counts = Counter(
    path[-1]["slug"]
    for p in items
    for path in p["categories"]
)

print(f"Categorized {len(items)} items → {out_dir / 'items.json'}\n")
print("Leaf category counts:")
for leaf_slug, count in sorted(leaf_counts.items(), key=lambda x: -x[1]):
    print(f"  {namify(leaf_slug):<25} {count}")
print(f"\nTotal leaf assignments: {sum(leaf_counts.values())} (can exceed {len(items)} — multi-leaf products counted once per leaf)")
