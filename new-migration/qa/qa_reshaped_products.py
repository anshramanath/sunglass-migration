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

# ── ID coverage ───────────────────────────────────────────────────────────────
source_ids   = set(source_map)
reshaped_ids = set(reshaped_map)

for pid in source_ids - reshaped_ids:
    err(pid, "present in source but missing from reshaped")
for pid in reshaped_ids - source_ids:
    err(pid, "present in reshaped but not in source")

# ── Per-product checks ────────────────────────────────────────────────────────
for pid, r in reshaped_map.items():
    s = source_map.get(pid)
    if s is None:
        continue

    is_variable = r.get("type") == "variable"

    # fields present / absent
    for f in EXPECTED_FIELDS:
        if f not in r:
            err(pid, f"missing expected field '{f}'")
    for f in DROPPED_FIELDS:
        if f in r:
            err(pid, f"old field '{f}' still present")

    # pass-through fields unchanged
    for f in ("id", "name", "slug", "type", "sku", "featured", "categories", "attributes", "variations"):
        if r.get(f) != s.get(f):
            err(pid, f"'{f}' changed: {s.get(f)!r} → {r.get(f)!r}")

    # oldLink == source permalink
    if r.get("oldLink") != s.get("permalink"):
        err(pid, f"oldLink mismatch: {r.get('oldLink')!r} != {s.get('permalink')!r}")

    # images: src/name objects unchanged
    if r.get("images") != s.get("images"):
        err(pid, "images array changed")

    # totalSales unchanged
    if r.get("totalSales") != s.get("total_sales"):
        err(pid, f"totalSales changed: {s.get('total_sales')!r} → {r.get('totalSales')!r}")

    # description: no HTML tags remaining
    desc = r.get("description")
    if desc is not None:
        if TAG_RE.search(desc):
            err(pid, f"description still contains HTML tags")

    # descriptionImages: list of strings or null
    di = r.get("descriptionImages")
    if di is not None:
        if not isinstance(di, list) or not all(isinstance(u, str) and u.startswith("http") for u in di):
            err(pid, f"descriptionImages is not a list of URLs: {di!r}")

    # shortDescription: list of plain strings or null
    sd = r.get("shortDescription")
    if sd is not None:
        if not isinstance(sd, list) or not sd:
            err(pid, "shortDescription is not a non-empty list")
        else:
            for item in sd:
                if not isinstance(item, str) or TAG_RE.search(item):
                    err(pid, f"shortDescription item contains HTML or is not a string: {item!r}")

    # pricing types: cents must be int or null
    for f in ("minPriceCents", "maxPriceCents", "salePriceCents"):
        v = r.get(f)
        if v is not None and not isinstance(v, int):
            err(pid, f"'{f}' is not an int: {v!r}")

    if is_variable:
        # variable: min/max/salePrice all null
        for f in ("minPriceCents", "maxPriceCents", "salePriceCents"):
            if r.get(f) is not None:
                err(pid, f"variable product '{f}' should be null, got {r[f]}")
        # sale = source on_sale
        if r.get("sale") != s.get("on_sale"):
            err(pid, f"sale mismatch: source on_sale={s.get('on_sale')!r} reshaped sale={r.get('sale')!r}")
    else:
        # simple: min == max
        if r.get("minPriceCents") != r.get("maxPriceCents"):
            err(pid, f"simple product minPriceCents ({r.get('minPriceCents')}) != maxPriceCents ({r.get('maxPriceCents')})")

        # min == regularPrice cents if set, else price cents
        def to_cents(val):
            if val in (None, ""):
                return None
            try:
                return round(float(val) * 100)
            except (TypeError, ValueError):
                return None

        rp = to_cents(s.get("regular_price"))
        expected_base = rp if rp is not None else to_cents(s.get("price"))
        if r.get("minPriceCents") != expected_base:
            err(pid, f"simple minPriceCents={r.get('minPriceCents')} expected {expected_base}")

        # salePriceCents == source sale_price cents
        expected_sp = to_cents(s.get("sale_price"))
        if r.get("salePriceCents") != expected_sp:
            err(pid, f"salePriceCents={r.get('salePriceCents')} expected {expected_sp}")

        # sale == source on_sale
        if r.get("sale") != s.get("on_sale"):
            err(pid, f"sale mismatch: source on_sale={s.get('on_sale')!r} reshaped sale={r.get('sale')!r}")

    # stock
    sq = s.get("stock_quantity")
    expected_stock = sq if sq is not None else (1 if s.get("stock_status") == "instock" else 0)
    if r.get("stock") != expected_stock:
        err(pid, f"stock={r.get('stock')} expected {expected_stock}")

    # weight: float or null; matches source
    w = r.get("weight")
    if w is not None and not isinstance(w, float):
        err(pid, f"weight is not a float: {w!r}")
    src_w = s.get("weight")
    expected_w = None if src_w in (None, "") else float(src_w)
    if w != expected_w:
        err(pid, f"weight={w!r} expected {expected_w!r}")

    # dimensions: null or all-three-present object with floats
    dims = r.get("dimensions")
    if dims is not None:
        if not isinstance(dims, dict):
            err(pid, "dimensions is not a dict")
        else:
            for dim in ("length", "width", "height"):
                v = dims.get(dim)
                if v is None or not isinstance(v, float):
                    err(pid, f"dimensions.{dim} is not a float: {v!r}")

# ── Summary ───────────────────────────────────────────────────────────────────
print(f"QA: reshaped products — {len(reshaped)} products checked\n")

if errors:
    print(f"  FAILED — {len(errors)} error(s):\n")
    for e in errors:
        print(f"  [ERROR] {e}")
else:
    print(f"  PASSED — all checks clean")
