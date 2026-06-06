import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "reshape-items-2" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run reshape_items_2.py first. Not found: {in_path}")

items = json.loads(in_path.read_text())

out_dir = BASE / "data" / slug / "validate-items"
out_dir.mkdir(parents=True, exist_ok=True)


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)

def is_bool(x):
    return isinstance(x, bool)

def check_image(img, label):
    errs = []
    if not img.get("src"):
        errs.append(f"{label}: missing src")
    if not img.get("name"):
        errs.append(f"{label}: missing name")
    if not is_int(img.get("sortOrder")):
        errs.append(f"{label}: sortOrder must be int, got {type(img.get('sortOrder')).__name__}")
    return errs


clean   = []
flagged = []

for item in items:
    reasons = []
    is_variable = item.get("sku") is None
    is_simple   = not is_variable

    # name / slug — text not null
    if not (item.get("name") or "").strip():
        reasons.append("name is null or empty")
    if not (item.get("slug") or "").strip():
        reasons.append("slug is null or empty")

    # price — int not null (description/summary/categories deferred)
    if not is_int(item.get("minPriceCents")):
        reasons.append(f"minPriceCents must be int, got {item.get('minPriceCents')!r}")
    if not is_int(item.get("maxPriceCents")):
        reasons.append(f"maxPriceCents must be int, got {item.get('maxPriceCents')!r}")
    if is_int(item.get("minPriceCents")) and is_int(item.get("maxPriceCents")):
        if item["minPriceCents"] > item["maxPriceCents"]:
            reasons.append(f"minPriceCents ({item['minPriceCents']}) > maxPriceCents ({item['maxPriceCents']})")

    # sale_price_cents — int or null
    if item.get("salePriceCents") is not None and not is_int(item.get("salePriceCents")):
        reasons.append(f"salePriceCents must be int or null, got {item.get('salePriceCents')!r}")

    # featured, sale, inStock — boolean not null
    if not is_bool(item.get("featured")):
        reasons.append(f"featured must be bool, got {item.get('featured')!r}")
    if not is_bool(item.get("sale")):
        reasons.append(f"sale must be bool, got {item.get('sale')!r}")
    if not is_bool(item.get("inStock")):
        reasons.append(f"inStock must be bool, got {item.get('inStock')!r}")

    # attributes — jsonb not null (list)
    if not isinstance(item.get("attributes"), list):
        reasons.append(f"attributes must be a list, got {type(item.get('attributes')).__name__}")

    # productImages — product_images table: src/name/sort_order all not null
    for i, img in enumerate(item.get("productImages", [])):
        reasons.extend(check_image(img, f"productImages[{i}]"))

    # descriptionImages — description_images table
    for i, img in enumerate(item.get("descriptionImages", [])):
        reasons.extend(check_image(img, f"descriptionImages[{i}]"))

    # simple-specific
    if is_simple:
        if not item.get("sku"):
            reasons.append("simple product sku is null or empty")
        if item.get("variations"):
            reasons.append("simple product has non-empty variations array")
        if not is_int(item.get("stock")):
            reasons.append(f"simple product stock must be int, got {item.get('stock')!r}")
        if not is_int(item.get("totalSales")):
            reasons.append(f"simple product totalSales must be int, got {item.get('totalSales')!r}")

    # variable-specific
    if is_variable:
        if item.get("stock") is not None:
            reasons.append(f"variable product stock must be null, got {item['stock']!r}")
        if item.get("totalSales") is not None:
            reasons.append(f"variable product totalSales must be null, got {item['totalSales']!r}")

        variations = item.get("variations", [])
        if len(variations) < 2:
            reasons.append(f"variable product has fewer than 2 variations ({len(variations)})")

        for v in variations:
            v_sku = v.get("sku") or ""
            label = f"variation {v_sku!r}" if v_sku else "variation (no sku)"
            if not v_sku:
                reasons.append(f"{label}: sku is null or empty")
            if not is_int(v.get("regularPriceCents")):
                reasons.append(f"{label}: regularPriceCents must be int, got {v.get('regularPriceCents')!r}")
            if v.get("salePriceCents") is not None and not is_int(v.get("salePriceCents")):
                reasons.append(f"{label}: salePriceCents must be int or null")
            if not is_int(v.get("stock")):
                reasons.append(f"{label}: stock must be int, got {v.get('stock')!r}")
            if not is_int(v.get("totalSales")):
                reasons.append(f"{label}: totalSales must be int, got {v.get('totalSales')!r}")
            if not is_bool(v.get("sale")):
                reasons.append(f"{label}: sale must be bool, got {v.get('sale')!r}")
            if not isinstance(v.get("attribute"), list) or not v.get("attribute"):
                reasons.append(f"{label}: attribute must be a non-empty list")
            for i, img in enumerate(v.get("variationImages", [])):
                reasons.extend(check_image(img, f"{label} variationImages[{i}]"))

    if reasons:
        flagged.append({"reasons": reasons, "item": item})
    else:
        clean.append(item)

(out_dir / "items.json").write_text(json.dumps(clean, indent=2, ensure_ascii=False))
(out_dir / "flagged.json").write_text(json.dumps(flagged, indent=2, ensure_ascii=False))
print(f"Clean: {len(clean)}  Flagged: {len(flagged)}")
for f in flagged:
    print(f"  {f['item'].get('name')}: {f['reasons']}")
