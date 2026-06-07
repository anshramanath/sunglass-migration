import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "validate-items" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run validate_items.py first. Not found: {in_path}")

# parse remove_items.md — map brand name to slug
brand_slug_map = {
    "BikerShades": "bikershades",
    "Monster":     "monster",
    "proSPORT":    "prosport",
}

remove_md = BASE.parent / "final-migration" / "docs" / "remove_items.md"
if not remove_md.exists():
    remove_md = BASE / "docs" / "remove_items.md"

remove_simple   = set()  # SKUs of simple products to drop
remove_variable = set()  # slugs of variable products to drop
remove_variation = set() # SKUs of variations to drop

for line in remove_md.read_text().splitlines():
    if not line.startswith("|") or "---|" in line or "Identifier" in line:
        continue
    parts = [p.strip() for p in line.strip("|").split("|")]
    if len(parts) < 3:
        continue
    identifier, type_, brand = parts[0], parts[1], parts[2]
    if brand_slug_map.get(brand) != slug:
        continue
    if type_ == "Simple":
        remove_simple.add(identifier)
    elif type_ == "Variable product":
        remove_variable.add(identifier)
    elif type_ == "Variation":
        remove_variation.add(identifier)

items = json.loads(in_path.read_text())

out_dir = BASE / "data" / slug / "remove-items"
out_dir.mkdir(parents=True, exist_ok=True)

kept    = []
removed = []

for item in items:
    is_simple = item.get("sku") is not None

    if is_simple:
        if item["sku"] in remove_simple:
            removed.append(item["name"])
            continue
        kept.append(item)
    else:
        if item["slug"] in remove_variable:
            removed.append(item["name"])
            continue

        # drop flagged variations; re-check minimum count
        surviving = [v for v in item.get("variations", []) if v["sku"] not in remove_variation]
        if len(surviving) < len(item.get("variations", [])):
            if len(surviving) < 2:
                removed.append(item["name"])
                continue
            item = {**item, "variations": surviving}

        kept.append(item)

(out_dir / "items.json").write_text(json.dumps(kept, indent=2, ensure_ascii=False))
print(f"Kept: {len(kept)}  Removed: {len(removed)}")
for name in removed:
    print(f"  - {name}")
