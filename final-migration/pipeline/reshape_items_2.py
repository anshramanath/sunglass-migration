import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "reshape-items" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run reshape_items_1.py first. Not found: {in_path}")

items = json.loads(in_path.read_text())

# load veeqo prices: sku -> highest sales_price in cents; stock: sku -> lowest qty_on_hand
_csv = sorted(Path(__file__).parent.glob("sellables_export*.csv"))
if not _csv:
    raise SystemExit("No sellables_export*.csv found in pipeline/")

veeqo_prices = {}
veeqo_stock  = {}
with open(_csv[0], newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        sku = row.get("sku_code", "").strip()
        if not sku:
            continue
        try:
            sales = round(float(row.get("sales_price") or 0) * 100)
            if sku not in veeqo_prices or sales > veeqo_prices[sku]:
                veeqo_prices[sku] = sales
        except (ValueError, TypeError):
            pass
        try:
            qty_f = float(row.get("qty_on_hand") or 0)
            if qty_f != float("inf") and qty_f != float("-inf"):
                qty = int(qty_f)
                if sku not in veeqo_stock or qty < veeqo_stock[sku]:
                    veeqo_stock[sku] = qty
        except (ValueError, TypeError):
            pass

out_dir = BASE / "data" / slug / "reshape-items-2"
out_dir.mkdir(parents=True, exist_ok=True)

reshaped = []
for item in items:
    is_simple = item.get("sku") is not None and not item.get("variations")

    if is_simple:
        sku = item["sku"]
        updates = {}
        if sku in veeqo_prices:
            updates["maxPriceCents"] = veeqo_prices[sku]
            updates["minPriceCents"] = veeqo_prices[sku]
        if sku in veeqo_stock:
            updates["stock"] = veeqo_stock[sku]
        if updates:
            item = {**item, **updates}
        if item.get("stock", 0) > 0:
            item = {**item, "inStock": True}
    else:
        updated_variations = []
        for v in item.get("variations", []):
            sku = v.get("sku", "")
            updates = {}
            if sku in veeqo_prices:
                updates["regularPriceCents"] = veeqo_prices[sku]
            if sku in veeqo_stock:
                updates["stock"] = veeqo_stock[sku]
            if updates:
                v = {**v, **updates}
            updated_variations.append(v)
        updated_variations = [
            v for v in updated_variations
            if v.get("regularPriceCents") is not None and v.get("attribute")
        ]
        prices = [
            v["salePriceCents"] if v.get("sale") and v.get("salePriceCents") is not None else v["regularPriceCents"]
            for v in updated_variations if v.get("regularPriceCents") is not None
        ]
        in_stock = any(v.get("stock", 0) > 0 for v in updated_variations)

        attr_map = {}
        for v in updated_variations:
            for a in v.get("attribute", []):
                name   = a.get("name", "")
                option = a.get("option", "")
                if name not in attr_map:
                    attr_map[name] = []
                if option not in attr_map[name]:
                    attr_map[name].append(option)
        attributes = [{"name": name, "options": options} for name, options in attr_map.items()]

        item = {
            **item,
            "variations":    updated_variations,
            "minPriceCents": min(prices) if prices else item.get("minPriceCents"),
            "maxPriceCents": max(prices) if prices else item.get("maxPriceCents"),
            "inStock":       in_stock,
            "attributes":    attributes,
        }

    reshaped.append(item)

(out_dir / "items.json").write_text(json.dumps(reshaped, indent=2, ensure_ascii=False))
print(f"Saved {len(reshaped)} items → {out_dir / 'items.json'}")
