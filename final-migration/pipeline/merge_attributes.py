import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "remove-items" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run remove_items.py first. Not found: {in_path}")

items = json.loads(in_path.read_text())

out_dir = BASE / "data" / slug / "merge-attributes"
out_dir.mkdir(parents=True, exist_ok=True)

ATTR_MERGE = {
    "Choose Color (REQUIRED)":    "color",
    "Choose Color":               "color",
    "Color":                      "color",
    "Choose Frame Color (Required)": "color",
    "Choose Bandana Color":       "color",
    "Choose Power":               "power",
    "Qty":                        "quantity",
    "Choose Quantity":            "quantity",
    "Cleaner Spray Bottle QTY":   "quantity",
    "Qty (packs of 3)":           "quantity",
    "Choose Transition Type":     "transition",
    "Choose Size":                "size",
}

# option rewrite only for Qty (packs of 3)
QTY_OPTION_REWRITE = {
    "1 pack (3 masks total)":   "3 masks",
    "2 packs (6 masks total)":  "6 masks",
    "5 packs (15 masks total)": "15 masks",
    "10 packs (30 masks total)":"30 masks",
}

def merge_name(name):
    return ATTR_MERGE.get(name, name)

def rewrite_option(attr_name, option):
    if attr_name == "Qty (packs of 3)":
        return QTY_OPTION_REWRITE.get(option, option)
    return option

def merge_product_attrs(attrs):
    merged = {}
    for a in attrs:
        new_name = merge_name(a["name"])
        options = [rewrite_option(a["name"], opt) for opt in a.get("options", [])]
        if new_name not in merged:
            merged[new_name] = []
        for opt in options:
            if opt not in merged[new_name]:
                merged[new_name].append(opt)
    return [{"name": name, "options": opts} for name, opts in merged.items()]

def merge_variation_attr(attribute, original_name):
    return {
        **attribute,
        "name":   merge_name(original_name),
        "option": rewrite_option(original_name, attribute.get("option", "")),
    }

merged_items = []
for item in items:
    # product-level attributes (variable products)
    if item.get("attributes"):
        item = {**item, "attributes": merge_product_attrs(item["attributes"])}

    # variation-level attribute
    if item.get("variations"):
        updated_variations = []
        for v in item["variations"]:
            merged_attr = [
                merge_variation_attr(a, a["name"])
                for a in v.get("attribute", [])
            ]
            updated_variations.append({**v, "attribute": merged_attr})
        item = {**item, "variations": updated_variations}

    merged_items.append(item)

(out_dir / "items.json").write_text(json.dumps(merged_items, indent=2, ensure_ascii=False))
print(f"Saved {len(merged_items)} items → {out_dir / 'items.json'}")
