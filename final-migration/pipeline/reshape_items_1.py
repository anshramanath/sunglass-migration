import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "slim-items" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run slim_items.py first. Not found: {in_path}")

items = json.loads(in_path.read_text())

out_dir = BASE / "data" / slug / "reshape-items"
out_dir.mkdir(parents=True, exist_ok=True)

def to_cents(val) -> int | None:
    try:
        return round(float(val) * 100) if val else None
    except (ValueError, TypeError):
        return None

def max_price_cents(*vals) -> int | None:
    candidates = [to_cents(v) for v in vals if to_cents(v) is not None]
    return max(candidates) if candidates else None

def extract_description_images(html: str) -> list:
    srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html or "")
    return [{"src": src, "name": src.rstrip("/").split("/")[-1], "sortOrder": i + 1} for i, src in enumerate(srcs)]

def clean_text(raw: str) -> str | None:
    text = re.sub(r'<[^>]+>', "", raw or "")
    text = html.unescape(text)
    text = re.sub(r'\s+', " ", text).strip().strip("‘’“”")
    return text or None

def clean_description(raw: str) -> str | None:
    return clean_text(raw)

def parse_summary(raw: str) -> list:
    if not raw:
        return []
    items = re.findall(r'<li[^>]*>(.*?)</li>', raw, re.DOTALL)
    if items:
        return [t for t in (clean_text(i) for i in items) if t]
    text = clean_text(raw)
    return [text] if text else []

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")

reshaped = []
for item in items:
    is_variable = bool(item.get("variations"))

    p = {
        "sku":               None if is_variable else item.get("sku"),
        "name":              item["name"],
        "slug":              slugify(item["name"]),
        "description":       clean_description(item.get("description")),
        "descriptionImages": extract_description_images(item.get("description")),
        "summary":           parse_summary(item.get("short_description")),
        "featured":          False,
        "stock":             None if is_variable else 0,
        "inStock":           False,
        "totalSales":        None if is_variable else 0,
        "maxPriceCents":     max_price_cents(item.get("price"), item.get("regular_price"), item.get("sale_price")),
        "minPriceCents":     max_price_cents(item.get("price"), item.get("regular_price"), item.get("sale_price")),
        "salePriceCents":    None,
        "sale":              False,
        "categories":        [],
        "productImages":     [{"src": img["src"], "name": img["name"], "sortOrder": i + 1} for i, img in enumerate(item.get("images", []))],
        "attribute":         [],
        "variations":        [
            {
                "sku":              v.get("sku"),
                "regularPriceCents": max_price_cents(v.get("price"), v.get("regular_price"), v.get("sale_price")),
                "salePriceCents":    None,
                "sale":              False,
                "stock":             0,
                "totalSales":        0,
                "variationImages":   [{"src": v["image"]["src"], "name": v["image"]["name"], "sortOrder": 1}] if v.get("image") else [],
                "attribute":        v.get("attributes", []),
            }
            for v in item.get("variations", [])
        ],
    }
    reshaped.append(p)

(out_dir / "items.json").write_text(json.dumps(reshaped, indent=2, ensure_ascii=False))
print(f"Saved {len(reshaped)} items → {out_dir / 'items.json'}")
