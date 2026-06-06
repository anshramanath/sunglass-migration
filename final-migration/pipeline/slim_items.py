import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "create-items" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run create_items.py first. Not found: {in_path}")

items = json.loads(in_path.read_text())

out_dir = BASE / "data" / slug / "slim-items"
out_dir.mkdir(parents=True, exist_ok=True)

PRODUCT_FIELDS   = {"name", "description", "short_description", "sku", "price", "regular_price", "sale_price", "images"}
VARIATION_FIELDS = {"sku", "image", "attributes", "price", "regular_price", "sale_price"}

slimmed = []
for item in items:
    p = {k: v for k, v in item.items() if k in PRODUCT_FIELDS}
    p["images"] = [{"src": img["src"], "name": img["name"]} for img in item.get("images", [])]
    slimmed_variations = []
    for var in item.get("variations", []):
        v = {k: val for k, val in var.items() if k in VARIATION_FIELDS}
        if "image" in v and isinstance(v["image"], dict):
            v["image"] = {"src": v["image"].get("src"), "name": v["image"].get("name")}
        if "attributes" in v:
            v["attributes"] = [{"name": a.get("name"), "option": a.get("option")} for a in v["attributes"]]
        slimmed_variations.append(v)
    p["variations"] = slimmed_variations
    slimmed.append(p)

(out_dir / "items.json").write_text(json.dumps(slimmed, indent=2, ensure_ascii=False))
print(f"Saved {len(slimmed)} items → {out_dir / 'items.json'}")
