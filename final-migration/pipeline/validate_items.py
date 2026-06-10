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
    if not (img.get("src") or "").strip():
        errs.append(f"{label}: missing src")
    if not (img.get("name") or "").strip():
        errs.append(f"{label}: missing name")
    if not is_int(img.get("sortOrder")):
        errs.append(f"{label}: sortOrder must be int, got {type(img.get('sortOrder')).__name__}")
    elif img["sortOrder"] <= 0:
        errs.append(f"{label}: sortOrder must be > 0, got {img['sortOrder']}")
    return errs


clean   = []
flagged = []

for item in items:
    reasons = []
    is_variable = item.get("sku") is None
    is_simple   = not is_variable

    # name / slug
    if not (item.get("name") or "").strip():
        reasons.append("name is null or empty")
    if not (item.get("slug") or "").strip():
        reasons.append("slug is null or empty")

    # featured must be false
    if item.get("featured") is not False:
        reasons.append(f"featured must be false, got {item.get('featured')!r}")

    # sale must be false
    if item.get("sale") is not False:
        reasons.append(f"sale must be false, got {item.get('sale')!r}")

    # salePriceCents must be null
    if item.get("salePriceCents") is not None:
        reasons.append(f"salePriceCents must be null, got {item.get('salePriceCents')!r}")

    # inStock — boolean
    if not is_bool(item.get("inStock")):
        reasons.append(f"inStock must be bool, got {item.get('inStock')!r}")

    # categories must be empty array
    if item.get("categories") != []:
        reasons.append(f"categories must be empty array, got {item.get('categories')!r}")

    # min/max price — non-null int > 0, min <= max
    if not is_int(item.get("minPriceCents")):
        reasons.append(f"minPriceCents must be int, got {item.get('minPriceCents')!r}")
    elif item["minPriceCents"] <= 0:
        reasons.append(f"minPriceCents must be > 0, got {item['minPriceCents']}")

    if not is_int(item.get("maxPriceCents")):
        reasons.append(f"maxPriceCents must be int, got {item.get('maxPriceCents')!r}")
    elif item["maxPriceCents"] <= 0:
        reasons.append(f"maxPriceCents must be > 0, got {item['maxPriceCents']}")

    if is_int(item.get("minPriceCents")) and is_int(item.get("maxPriceCents")):
        if item["minPriceCents"] > item["maxPriceCents"]:
            reasons.append(f"minPriceCents ({item['minPriceCents']}) > maxPriceCents ({item['maxPriceCents']})")

    # productImages — must be non-empty; each entry valid
    if not item.get("productImages"):
        reasons.append("productImages must be non-empty")
    else:
        for i, img in enumerate(item["productImages"]):
            reasons.extend(check_image(img, f"productImages[{i}]"))

    # descriptionImages — each entry valid if present
    for i, img in enumerate(item.get("descriptionImages", [])):
        reasons.extend(check_image(img, f"descriptionImages[{i}]"))

    # simple-specific
    if is_simple:
        if not (item.get("sku") or "").strip():
            reasons.append("simple product sku is null or empty")
        if item.get("variations"):
            reasons.append("simple product has non-empty variations array")
        if not is_int(item.get("stock")):
            reasons.append(f"simple product stock must be int, got {item.get('stock')!r}")
        if item.get("totalSales") != 0:
            reasons.append(f"simple product totalSales must be 0, got {item.get('totalSales')!r}")

    # variable-specific
    if is_variable:
        if item.get("stock") is not None:
            reasons.append(f"variable product stock must be null, got {item['stock']!r}")
        if item.get("totalSales") is not None:
            reasons.append(f"variable product totalSales must be null, got {item['totalSales']!r}")

        # attributes — non-empty; each entry has non-empty name and at least one non-empty option
        attrs = item.get("attributes", [])
        if not attrs:
            reasons.append("variable product attributes must be non-empty")
        else:
            for j, a in enumerate(attrs):
                if not (a.get("name") or "").strip():
                    reasons.append(f"attributes[{j}]: name is null or empty")
                options = a.get("options", [])
                if not options:
                    reasons.append(f"attributes[{j}] '{a.get('name')}': options must be non-empty")
                else:
                    for k, opt in enumerate(options):
                        if not (opt or "").strip():
                            reasons.append(f"attributes[{j}] '{a.get('name')}' options[{k}]: must be non-empty string")

        variations = item.get("variations", [])
        if len(variations) < 2:
            reasons.append(f"variable product has fewer than 2 variations ({len(variations)})")

        var_combos: set[tuple] = set()
        for v in variations:
            v_sku = (v.get("sku") or "").strip()
            label = f"variation {v_sku!r}" if v_sku else "variation (no sku)"
            if not v_sku:
                reasons.append(f"{label}: sku is null or empty")
            if not is_int(v.get("regularPriceCents")):
                reasons.append(f"{label}: regularPriceCents must be int, got {v.get('regularPriceCents')!r}")
            elif v["regularPriceCents"] <= 0:
                reasons.append(f"{label}: regularPriceCents must be > 0, got {v['regularPriceCents']}")
            if v.get("salePriceCents") is not None:
                reasons.append(f"{label}: salePriceCents must be null, got {v.get('salePriceCents')!r}")
            if not is_int(v.get("stock")):
                reasons.append(f"{label}: stock must be int, got {v.get('stock')!r}")
            if v.get("totalSales") != 0:
                reasons.append(f"{label}: totalSales must be 0, got {v.get('totalSales')!r}")
            if v.get("sale") is not False:
                reasons.append(f"{label}: sale must be false, got {v.get('sale')!r}")
            attribute = v.get("attribute", [])
            if not attribute:
                reasons.append(f"{label}: attribute must be non-empty")
            else:
                for j, a in enumerate(attribute):
                    if not (a.get("name") or "").strip():
                        reasons.append(f"{label} attribute[{j}]: name is null or empty")
                    if not (a.get("option") or "").strip():
                        reasons.append(f"{label} attribute[{j}]: option is null or empty")
                combo = tuple(sorted(f"{a.get('name')}={a.get('option')}" for a in attribute))
                if combo in var_combos:
                    reasons.append(f"{label}: duplicate attribute combination")
                var_combos.add(combo)
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
