import json
import os
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).parent.parent
load_dotenv(dotenv_path=BASE.parent / ".env")

BRAND_CONFIG = {
    "proSPORT Sunglasses": {
        "slug": "prosport",
    },
}

brand_name = os.getenv("BRAND")
config = BRAND_CONFIG.get(brand_name)
if not config:
    raise SystemExit(f"Unknown BRAND={brand_name!r}. Add it to BRAND_CONFIG.")

slug = config["slug"]
in_path = BASE / "data" / slug / "fetch-variations" / "variations.json"
out_dir = BASE / "data" / slug / "slim-variations"
out_dir.mkdir(parents=True, exist_ok=True)

raw = json.loads(in_path.read_text())
total_in = sum(len(e["variations"]) for e in raw)
print(f"Brand: {brand_name} ({slug})")
print(f"Slimming {total_in} variations across {len(raw)} products...\n")

def slim(v):
    return {
        "id": v["id"],
        "parent_id": v["parent_id"],
        "name": v.get("name"),
        "type": v.get("type"),
        "status": v.get("status"),
        "description": v.get("description"),
        "permalink": v.get("permalink"),
        "sku": v.get("sku"),
        "price": v.get("price"),
        "regular_price": v.get("regular_price"),
        "sale_price": v.get("sale_price"),
        "on_sale": v.get("on_sale"),
        "stock_quantity": v.get("stock_quantity"),
        "stock_status": v.get("stock_status"),
        "weight": v.get("weight"),
        "dimensions": v.get("dimensions"),
        "image": {"src": v["image"]["src"], "name": v["image"]["name"]} if v.get("image") else None,
        "attributes": [{"name": a["name"], "option": a["option"]} for a in v.get("attributes", [])],
    }

slimmed = [
    {"product_id": e["product_id"], "variations": [slim(v) for v in e["variations"]]}
    for e in raw
]

total_out = sum(len(e["variations"]) for e in slimmed)

out = out_dir / "variations.json"
out.write_text(json.dumps(slimmed, indent=2, ensure_ascii=False))

print(f"Saved {total_out} slimmed variations → {out}")
print(f"\n  → Next: python pipeline/validate_variations.py")
