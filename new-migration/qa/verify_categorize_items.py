import json
import os
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).parent.parent
load_dotenv(dotenv_path=BASE.parent / ".env")

BRAND_CONFIG = {
    "prosport": {"slug": "prosport"},
}

brand_name = os.getenv("BRAND")
config = BRAND_CONFIG.get(brand_name)
if not config:
    raise SystemExit(f"Unknown BRAND={brand_name!r}. Add it to BRAND_CONFIG.")

slug = config["slug"]
data_dir = BASE / "data" / slug

source = json.loads((data_dir / "create-items"    / "items.json").read_text())
output = json.loads((data_dir / "categorize-items" / "items.json").read_text())

LEAF_SLUGS = {
    "bifocals", "full-lens", "sport", "street", "metal-and-aviators",
    "polarized", "hd-copper", "clear-and-yellow", "accessories",
}
PARENT_SLUGS = {"readers-special-fit", "shop-by-style", "lens-color"}

HARDCODED = {
    2887: "full-lens",
    1160: "metal-and-aviators", 1184: "metal-and-aviators",
    1165: "metal-and-aviators", 1224: "metal-and-aviators",
    1179: "street", 1189: "street", 1170: "street", 1175: "street",
    2905: "accessories", 2904: "accessories", 2899: "accessories",
    2898: "accessories", 2778: "accessories", 2773: "accessories",
    2772: "accessories", 2768: "accessories", 2749: "accessories",
    2748: "accessories", 2747: "accessories", 2746: "accessories",
}

def namify(s):
    return " ".join(w if w == "and" else w.capitalize() for w in s.replace("-", " ").split())

errors = []

def err(msg):
    errors.append(msg)

# ── Coverage ──────────────────────────────────────────────────────────────────
source_ids = {p["id"] for p in source}
output_ids = {p["id"] for p in output}

for pid in sorted(source_ids - output_ids):
    err(f"id={pid} present in source but missing from output")
for pid in sorted(output_ids - source_ids):
    err(f"id={pid} present in output but not in source")

# ── Per-product checks ────────────────────────────────────────────────────────
source_by_id = {p["id"]: p for p in source}

for p in output:
    pid = p["id"]
    s   = source_by_id.get(pid)

    # Every product has at least one category path
    if not p["categories"]:
        err(f"id={pid} has no categories")
        continue

    leaf_slugs_seen = []
    for path in p["categories"]:

        # Each path is a non-empty list
        if not path:
            err(f"id={pid}: empty path in categories")
            continue

        # Deepest entry is a leaf, not a parent
        deepest = path[-1]["slug"]
        if deepest not in LEAF_SLUGS:
            err(f"id={pid}: path ends at non-leaf {deepest!r}")
        if deepest in PARENT_SLUGS:
            err(f"id={pid}: path ends at parent slug {deepest!r}")
        leaf_slugs_seen.append(deepest)

        # Level values are correct and ordered
        for i, entry in enumerate(path):
            expected_level = i + 1
            if entry["level"] != expected_level:
                err(f"id={pid}: entry {entry['slug']!r} has level={entry['level']}, expected {expected_level}")

        # Parent entry (if present) is NOT a leaf
        if len(path) == 2:
            parent_slug = path[0]["slug"]
            if parent_slug in LEAF_SLUGS:
                err(f"id={pid}: parent slug {parent_slug!r} is also a leaf slug")
            if parent_slug not in PARENT_SLUGS:
                err(f"id={pid}: path[0] slug {parent_slug!r} not a known parent")

        # namify(slug) == name for every entry
        for entry in path:
            expected_name = namify(entry["slug"])
            if entry["name"] != expected_name:
                err(f"id={pid}: namify({entry['slug']!r}) = {expected_name!r} but name={entry['name']!r}")

    # No duplicate leaf slugs within one product
    if len(leaf_slugs_seen) != len(set(leaf_slugs_seen)):
        dupes = [s for s in set(leaf_slugs_seen) if leaf_slugs_seen.count(s) > 1]
        err(f"id={pid}: duplicate leaf slugs {dupes}")

    # Hardcoded products got their assigned leaf
    if pid in HARDCODED:
        assigned = HARDCODED[pid]
        if assigned not in leaf_slugs_seen:
            err(f"id={pid}: hardcoded leaf {assigned!r} not found in categories")

    # All non-category fields are unchanged
    for field in p:
        if field == "categories":
            continue
        if p[field] != s.get(field):
            err(f"id={pid}: field {field!r} changed — was {s.get(field)!r}, now {p[field]!r}")

# ── Products that had only Uncategorized now have a real category ─────────────
was_only_uncat = {
    p["id"] for p in source
    if p.get("categories") and all(c["name"] == "Uncategorized" for c in p["categories"])
}
for pid in was_only_uncat:
    p = next((x for x in output if x["id"] == pid), None)
    if not p or not p["categories"]:
        err(f"id={pid}: was uncategorized-only, still has no category in output")

# ── Uncategorized and Big and Tall are fully gone ─────────────────────────────
bad_names = {"Uncategorized", "Big and Tall"}
for p in output:
    for path in p["categories"]:
        for entry in path:
            if entry["name"] in bad_names:
                err(f"id={p['id']}: dropped tag {entry['name']!r} still present")

# ── Report ────────────────────────────────────────────────────────────────────
print(f"verify_categorize_items — {brand_name}")
print(f"  source : {len(source)} items")
print(f"  output : {len(output)} items\n")

if errors:
    print(f"FAILED — {len(errors)} error(s):")
    for e in errors:
        print(f"  [ERROR] {e}")
else:
    print("PASSED — all checks clean")
