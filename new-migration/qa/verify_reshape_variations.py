import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).parent.parent
load_dotenv(dotenv_path=BASE.parent / ".env")

BRAND_CONFIG = {
    "proSPORT Sunglasses": {"slug": "prosport"},
}

brand_name = os.getenv("BRAND")
config = BRAND_CONFIG.get(brand_name)
if not config:
    raise SystemExit(f"Unknown BRAND={brand_name!r}. Add it to BRAND_CONFIG.")

slug = config["slug"]
data_dir = BASE / "data" / slug

source   = json.loads((data_dir / "validate-variations" / "variations.json").read_text())
reshaped = json.loads((data_dir / "reshape-variations" / "variations.json").read_text())

source_map   = {e["product_id"]: {v["id"]: v for v in e["variations"]} for e in source}
reshaped_map = {e["product_id"]: {v["id"]: v for v in e["variations"]} for e in reshaped}

errors = []

def err(vid, msg):
    errors.append(f"id={vid} | {msg}")

TAG_RE = re.compile(r'<[^>]+>')

EXPECTED_FIELDS = {
    "id", "parent_id", "name", "type", "oldLink", "description",
    "sku", "regularPriceCents", "salePriceCents", "sale",
    "stock", "weight", "dimensions", "images", "attributes",
}

DROPPED_FIELDS = {
    "status", "permalink", "price", "regular_price", "sale_price",
    "on_sale", "stock_quantity", "stock_status",
}

def to_cents(val):
    if val in (None, ""):
        return None
    try:
        return round(float(val) * 100)
    except (TypeError, ValueError):
        return None

def to_num(val):
    if val in (None, ""):
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

def clean_attr_name(name):
    name = re.sub(r'(?i)^choose\s+', '', name).strip()
    return name

# ── Product ID coverage ───────────────────────────────────────────────────────
for pid in set(source_map) - set(reshaped_map):
    err(pid, "product_id present in source but missing from reshaped")
for pid in set(reshaped_map) - set(source_map):
    err(pid, "product_id present in reshaped but not in source")

# ── Per-variation checks ──────────────────────────────────────────────────────
for pid, r_vars in reshaped_map.items():
    s_vars = source_map.get(pid, {})

    for vid, r in r_vars.items():
        s = s_vars.get(vid)
        if s is None:
            err(vid, f"variation present in reshaped but not in source (product_id={pid})")
            continue

        # expected fields present, old fields absent
        for f in EXPECTED_FIELDS:
            if f not in r:
                err(vid, f"missing expected field '{f}'")
        for f in DROPPED_FIELDS:
            if f in r:
                err(vid, f"old field '{f}' still present")

        # pass-through fields unchanged
        for f in ("id", "parent_id", "name", "type", "sku"):
            if r.get(f) != s.get(f):
                err(vid, f"'{f}' changed: {s.get(f)!r} → {r.get(f)!r}")

        # oldLink == source permalink
        if r.get("oldLink") != s.get("permalink"):
            err(vid, f"oldLink mismatch: {r.get('oldLink')!r} != {s.get('permalink')!r}")

        # images: array; src matches source image src; name derived from URL
        raw_img  = s.get("image")
        r_images = r.get("images", [])
        if not isinstance(r_images, list):
            err(vid, f"images is not a list: {r_images!r}")
        elif raw_img and raw_img.get("src"):
            if len(r_images) != 1 or r_images[0].get("src") != raw_img["src"]:
                err(vid, f"images src mismatch: expected [{raw_img['src']!r}]")
        else:
            if r_images:
                err(vid, f"source image is null but images={r_images!r}")

        # description: no HTML
        desc = r.get("description")
        if desc is not None and TAG_RE.search(desc):
            err(vid, "description still contains HTML tags")

        # pricing types: int or null
        for f in ("regularPriceCents", "salePriceCents"):
            v = r.get(f)
            if v is not None and not isinstance(v, int):
                err(vid, f"'{f}' is not an int: {v!r}")

        # regularPriceCents matches source
        if r.get("regularPriceCents") != to_cents(s.get("regular_price")):
            err(vid, f"regularPriceCents={r.get('regularPriceCents')} expected {to_cents(s.get('regular_price'))}")

        # salePriceCents matches source
        if r.get("salePriceCents") != to_cents(s.get("sale_price")):
            err(vid, f"salePriceCents={r.get('salePriceCents')} expected {to_cents(s.get('sale_price'))}")

        # sale matches source on_sale
        if r.get("sale") != s.get("on_sale"):
            err(vid, f"sale mismatch: source={s.get('on_sale')!r} reshaped={r.get('sale')!r}")

        # stock
        sq = s.get("stock_quantity")
        expected_stock = sq if sq is not None else (1 if s.get("stock_status") == "instock" else 0)
        if r.get("stock") != expected_stock:
            err(vid, f"stock={r.get('stock')} expected {expected_stock}")

        # weight: float or null, matches source
        w = r.get("weight")
        if w is not None and not isinstance(w, float):
            err(vid, f"weight is not a float: {w!r}")
        expected_w = to_num(s.get("weight"))
        if w != expected_w:
            err(vid, f"weight={w!r} expected {expected_w!r}")

        # dimensions: always a dict with length/width/height each float or null
        dims = r.get("dimensions")
        if not isinstance(dims, dict):
            err(vid, f"dimensions is not a dict: {dims!r}")
        else:
            for dim in ("length", "width", "height"):
                dv = dims.get(dim)
                if dv is not None and not isinstance(dv, float):
                    err(vid, f"dimensions.{dim} is not a float or null: {dv!r}")

        # attributes: name cleaned, Power options normalized
        def norm_power(name, option):
            if name == "Power":
                try:
                    return f"{float(option.replace('-', '.')):.2f}"
                except (ValueError, AttributeError):
                    pass
            return option

        expected_attrs = [
            {"name": clean_attr_name(a["name"]), "option": norm_power(clean_attr_name(a["name"]), a["option"])}
            for a in s.get("attributes", [])
        ]
        if r.get("attributes") != expected_attrs:
            err(vid, f"attributes mismatch")

    # check for variations in source missing from reshaped
    for vid in set(s_vars) - set(r_vars):
        err(vid, f"variation present in source but missing from reshaped (product_id={pid})")

# ── Summary ───────────────────────────────────────────────────────────────────
total_reshaped = sum(len(e["variations"]) for e in reshaped)
print(f"Verify: reshape-variations — {total_reshaped} variations across {len(reshaped)} products\n")

if errors:
    print(f"  FAILED — {len(errors)} error(s):\n")
    for e in errors:
        print(f"  [ERROR] {e}")
else:
    print(f"  PASSED — all checks clean")
