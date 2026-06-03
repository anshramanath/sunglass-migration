import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand


brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]
in_path = BASE / "data" / slug / "fetch-products" / "products.json"
out_dir = BASE / "data" / slug / "slim-products"
out_dir.mkdir(parents=True, exist_ok=True)

raw = json.loads(in_path.read_text())
print(f"Brand: {brand_name} ({slug})")
print(f"Slimming {len(raw)} products...\n")

def slim(p):
    return {
        "id": p["id"],
        "name": p.get("name"),
        "slug": p.get("slug"),
        "permalink": p.get("permalink"),
        "type": p.get("type"),
        "status": p.get("status"),
        "description": p.get("description"),
        "short_description": p.get("short_description"),
        "sku": p.get("sku"),
        "price": p.get("price"),
        "regular_price": p.get("regular_price"),
        "sale_price": p.get("sale_price"),
        "on_sale": p.get("on_sale"),
        "featured": p.get("featured"),
        "total_sales": p.get("total_sales"),
        "stock_quantity": p.get("stock_quantity"),
        "stock_status": p.get("stock_status"),
        "weight": p.get("weight"),
        "dimensions": p.get("dimensions"),
        "categories": [{"name": c["name"], "slug": c["slug"]} for c in p.get("categories", [])],
        "images": [{"src": i["src"], "name": i["name"]} for i in p.get("images", [])],
        "attributes": [{"name": a["name"], "options": a["options"]} for a in p.get("attributes", [])],
        "variations": p.get("variations", []),
    }

slimmed = [slim(p) for p in raw]

out = out_dir / "products.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(slimmed, f, indent=2, ensure_ascii=False)

print(f"Saved {len(slimmed)} slimmed products → {out}")
print(f"\n  → Next: python pipeline/validate_products.py")
