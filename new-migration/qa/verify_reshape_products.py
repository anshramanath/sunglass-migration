import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).parent.parent
load_dotenv(dotenv_path=BASE.parent / ".env")

BRAND_CONFIG = {
    "prosport": {"slug": "prosport"},
}

brand_name = os.getenv("BRAND")
config = BRAND_CONFIG.get(brand_name)
if not config:
    raise SystemExit(f"Unknown BRAND={brand_name!r}. Add it to BRAND_CONFIG.")

slug = config["slug"]
data_dir = BASE / "data" / slug

source   = json.loads((data_dir / "validate-products" / "products.json").read_text())
reshaped = json.loads((data_dir / "reshape-products" / "products.json").read_text())

source_map   = {p["id"]: p for p in source}
reshaped_map = {p["id"]: p for p in reshaped}

errors = []

def err(pid, msg):
    errors.append(f"id={pid} | {msg}")

TAG_RE = re.compile(r'<[^>]+>')

EXPECTED_FIELDS = {
    "id", "name", "slug", "oldLink", "type",
    "description", "descriptionImages", "shortDescription",
    "sku", "minPriceCents", "maxPriceCents", "salePriceCents", "sale",
    "featured", "totalSales", "stock", "weight", "dimensions",
    "categories", "images", "attributes", "variations",
}

DROPPED_FIELDS = {
    "status", "permalink", "price", "regular_price", "sale_price",
    "on_sale", "short_description", "stock_quantity", "stock_status",
}

def to_cents(val):
    if val in (None, ""):
        return None
    try:
        return round(float(val) * 100)
    except (TypeError, ValueError):
        return None

# ── ID coverage ───────────────────────────────────────────────────────────────
for pid in set(source_map) - set(reshaped_map):
    err(pid, "present in source but missing from reshaped")
for pid in set(reshaped_map) - set(source_map):
    err(pid, "present in reshaped but not in source")

# ── Per-product checks ────────────────────────────────────────────────────────
for pid, r in reshaped_map.items():
    s = source_map.get(pid)
    if s is None:
        continue

    is_variable = r.get("type") == "variable"

    # expected fields present, old fields absent
    for f in EXPECTED_FIELDS:
        if f not in r:
            err(pid, f"missing expected field '{f}'")
    for f in DROPPED_FIELDS:
        if f in r:
            err(pid, f"old field '{f}' still present")

    # pass-through fields unchanged
    for f in ("id", "name", "slug", "type", "sku", "featured", "categories", "variations"):
        if r.get(f) != s.get(f):
            err(pid, f"'{f}' changed: {s.get(f)!r} → {r.get(f)!r}")

    # attributes: names cleaned (Choose prefix + for Filter suffix stripped); options unchanged
    def clean_attr_name(n):
        import re as _re
        n = _re.sub(r'(?i)\s+for\s+filter$', '', n).strip()
        n = _re.sub(r'(?i)^choose\s+', '', n).strip()
        return n
    expected_attrs = [{**a, 'name': clean_attr_name(a['name'])} for a in s.get('attributes', [])]
    if r.get('attributes') != expected_attrs:
        err(pid, f"attributes mismatch")

    # oldLink == source permalink
    if r.get("oldLink") != s.get("permalink"):
        err(pid, f"oldLink mismatch: {r.get('oldLink')!r} != {s.get('permalink')!r}")

    # images unchanged
    if r.get("images") != s.get("images"):
        err(pid, "images array changed")

    # totalSales unchanged
    if r.get("totalSales") != s.get("total_sales"):
        err(pid, f"totalSales changed: {s.get('total_sales')!r} → {r.get('totalSales')!r}")

    # description: no HTML tags
    desc = r.get("description")
    if desc is not None and TAG_RE.search(desc):
        err(pid, "description still contains HTML tags")

    # descriptionImages: list of {src, name} objects (never null)
    di = r.get("descriptionImages")
    if not isinstance(di, list):
        err(pid, f"descriptionImages is not a list: {di!r}")
    else:
        for entry in di:
            if not isinstance(entry, dict):
                err(pid, f"descriptionImages entry is not an object: {entry!r}")
            elif not isinstance(entry.get("src"), str) or not entry["src"].startswith("http"):
                err(pid, f"descriptionImages entry missing valid src: {entry!r}")
            elif not isinstance(entry.get("name"), str) or not entry["name"]:
                err(pid, f"descriptionImages entry missing name: {entry!r}")

    # shortDescription: list of plain strings (never null)
    sd = r.get("shortDescription")
    if not isinstance(sd, list):
        err(pid, f"shortDescription is not a list: {sd!r}")
    else:
        for item in sd:
            if not isinstance(item, str) or TAG_RE.search(item):
                err(pid, f"shortDescription item contains HTML or is not a string: {item!r}")

    # price fields: int or null
    for f in ("minPriceCents", "maxPriceCents", "salePriceCents"):
        v = r.get(f)
        if v is not None and not isinstance(v, int):
            err(pid, f"'{f}' is not an int: {v!r}")

    if is_variable:
        for f in ("minPriceCents", "maxPriceCents", "salePriceCents"):
            if r.get(f) is not None:
                err(pid, f"variable '{f}' should be null, got {r[f]}")
        if r.get("sale") != s.get("on_sale"):
            err(pid, f"sale mismatch: source on_sale={s.get('on_sale')!r} reshaped sale={r.get('sale')!r}")
    else:
        # min == max
        if r.get("minPriceCents") != r.get("maxPriceCents"):
            err(pid, f"simple minPriceCents ({r.get('minPriceCents')}) != maxPriceCents ({r.get('maxPriceCents')})")
        # min == regularPrice cents if set, else price cents
        rp = to_cents(s.get("regular_price"))
        expected_base = rp if rp is not None else to_cents(s.get("price"))
        if r.get("minPriceCents") != expected_base:
            err(pid, f"minPriceCents={r.get('minPriceCents')} expected {expected_base}")
        # salePriceCents matches source sale_price
        if r.get("salePriceCents") != to_cents(s.get("sale_price")):
            err(pid, f"salePriceCents={r.get('salePriceCents')} expected {to_cents(s.get('sale_price'))}")
        # sale matches source on_sale
        if r.get("sale") != s.get("on_sale"):
            err(pid, f"sale mismatch: source on_sale={s.get('on_sale')!r} reshaped sale={r.get('sale')!r}")

    # stock
    sq = s.get("stock_quantity")
    expected_stock = sq if sq is not None else (1 if s.get("stock_status") == "instock" else 0)
    if r.get("stock") != expected_stock:
        err(pid, f"stock={r.get('stock')} expected {expected_stock}")

    # weight: float or null, matches source
    w = r.get("weight")
    if w is not None and not isinstance(w, float):
        err(pid, f"weight is not a float: {w!r}")
    src_w = s.get("weight")
    expected_w = None if src_w in (None, "") else float(src_w)
    if w != expected_w:
        err(pid, f"weight={w!r} expected {expected_w!r}")

    # dimensions: always a dict with length/width/height each float or null
    dims = r.get("dimensions")
    if not isinstance(dims, dict):
        err(pid, f"dimensions is not a dict: {dims!r}")
    else:
        for dim in ("length", "width", "height"):
            v = dims.get(dim)
            if v is not None and not isinstance(v, float):
                err(pid, f"dimensions.{dim} is not a float or null: {v!r}")

# ── Summary ───────────────────────────────────────────────────────────────────
print(f"Verify: reshape-products — {len(reshaped)} products\n")

if errors:
    print(f"  FAILED — {len(errors)} error(s):\n")
    for e in errors:
        print(f"  [ERROR] {e}")
else:
    print(f"  PASSED — all checks clean")
