import html
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
data = json.loads((BASE / "data" / slug / "slim-products" / "products.json").read_text())

out_dir = BASE / "data" / slug / "validate-products"
out_dir.mkdir(parents=True, exist_ok=True)

product_errors = {}
seen_ids = set()
seen_skus = {}  # sku -> pid, for duplicate detection

def err(pid, msg):
    product_errors.setdefault(pid, []).append(msg)

def is_num(v):
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False

def slugify(s):
    s = html.unescape(s).lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    return re.sub(r'-+', '-', s)

for p in data:
    pid = p.get("id")
    is_variable = bool(p.get("variations"))

    # id: number, unique
    if not isinstance(pid, (int, float)):
        err(pid, "id is not a number")
    elif pid in seen_ids:
        err(pid, "id is not unique")
    else:
        seen_ids.add(pid)

    # name: non-empty string
    if not isinstance(p.get("name"), str) or not p["name"].strip():
        err(pid, "name is not a valid non-empty string")

    # slug: non-empty string
    if not isinstance(p.get("slug"), str) or not p["slug"].strip():
        err(pid, "slug is not a valid non-empty string")

    # permalink: non-empty string
    if not isinstance(p.get("permalink"), str) or not p["permalink"].strip():
        err(pid, "permalink is not a valid non-empty string")

    # type: variable or simple
    if p.get("type") not in ("variable", "simple"):
        err(pid, f"type must be 'variable' or 'simple', got {p.get('type')!r}")

    # type vs variations consistency
    if p.get("type") == "variable" and not p.get("variations"):
        err(pid, "type=variable but variations is empty")
    if p.get("type") == "simple" and p.get("variations"):
        err(pid, "type=simple but has variation IDs")

    # status: publish or draft; draft is an error
    if p.get("status") not in ("publish", "draft"):
        err(pid, f"status must be 'publish' or 'draft', got {p.get('status')!r}")
    elif p.get("status") == "draft":
        err(pid, "status=draft")

    # description: string or null
    if p.get("description") is not None and not isinstance(p["description"], str):
        err(pid, "description must be a string or null")

    # short_description: string or null
    if p.get("short_description") is not None and not isinstance(p["short_description"], str):
        err(pid, "short_description must be a string or null")

    # sku: non-empty string, no spaces, unique
    sku = p.get("sku")
    if not isinstance(sku, str) or not sku.strip():
        err(pid, "sku is not a valid non-empty string")
    elif " " in sku:
        err(pid, f"sku contains spaces: {sku!r}")
    elif sku in seen_skus:
        err(pid, f"duplicate sku {sku!r} already seen on id={seen_skus[sku]}")
    else:
        seen_skus[sku] = pid

    # price: valid number greater than zero
    price = p.get("price")
    if not isinstance(price, str) or not price.strip():
        err(pid, "price is missing or empty")
    elif not is_num(price):
        err(pid, f"price is not a valid number: {price!r}")
    elif float(price) <= 0:
        err(pid, f"price must be greater than zero, got {price}")

    # regular_price: null or empty string OK; if non-empty must be a valid number
    rp = p.get("regular_price")
    if rp not in (None, "") and not is_num(rp):
        err(pid, f"regular_price is not a valid number: {rp!r}")

    # sale_price: same
    sp = p.get("sale_price")
    if sp not in (None, "") and not is_num(sp):
        err(pid, f"sale_price is not a valid number: {sp!r}")

    # sale_price < regular_price when both present
    if rp not in (None, "") and sp not in (None, ""):
        if float(sp) >= float(rp):
            err(pid, f"sale_price ({sp}) >= regular_price ({rp})")

    # on_sale: boolean
    if not isinstance(p.get("on_sale"), bool):
        err(pid, f"on_sale must be a boolean, got {p.get('on_sale')!r}")

    # on_sale vs sale_price consistency (simple products only — reliable signal)
    if not is_variable:
        if p.get("on_sale") and sp in (None, ""):
            err(pid, "on_sale=True but no sale_price (simple product)")
        if sp not in (None, "") and not p.get("on_sale"):
            err(pid, "sale_price set but on_sale=False (simple product)")

        # when no sale_price: price must equal regular_price
        if sp in (None, "") and rp not in (None, "") and is_num(price) and is_num(rp):
            if price != rp:
                err(pid, f"no sale_price but price ({price}) != regular_price ({rp})")

    # featured: boolean
    if not isinstance(p.get("featured"), bool):
        err(pid, f"featured must be a boolean, got {p.get('featured')!r}")

    # total_sales: number or null
    ts = p.get("total_sales")
    if ts is not None and not isinstance(ts, (int, float)):
        err(pid, f"total_sales must be a number or null, got {ts!r}")

    # stock_quantity: number or null
    sq = p.get("stock_quantity")
    if sq is not None and not isinstance(sq, (int, float)):
        err(pid, f"stock_quantity must be a number or null, got {sq!r}")

    # stock_status: required, must be instock or outofstock
    ss = p.get("stock_status")
    if not ss:
        err(pid, "stock_status is missing")
    elif ss not in ("instock", "outofstock"):
        err(pid, f"stock_status must be 'instock' or 'outofstock', got {ss!r}")

    # weight: null or valid number
    w = p.get("weight")
    if w not in (None, "") and not is_num(w):
        err(pid, f"weight is not a valid number: {w!r}")

    # dimensions: each subfield null/empty or valid number
    dims = p.get("dimensions") or {}
    for dim in ("length", "width", "height"):
        v = dims.get(dim)
        if v not in (None, "") and not is_num(v):
            err(pid, f"dimensions.{dim} is not a valid number: {v!r}")

    # categories: name and slug non-empty; slugify(name)==slug
    for c in p.get("categories", []):
        cname = c.get("name")
        cslug = c.get("slug")
        if not isinstance(cname, str) or not cname.strip():
            err(pid, f"category name is not a valid non-empty string: {c}")
        if not isinstance(cslug, str) or not cslug.strip():
            err(pid, f"category slug is not a valid non-empty string: {c}")
        if isinstance(cname, str) and isinstance(cslug, str):
            expected = slugify(cname)
            if expected != cslug:
                err(pid, f"category slug mismatch: name={cname!r} expected={expected!r} got={cslug!r}")

    # images: at least one required
    if not p.get("images"):
        err(pid, "images is empty — product must have at least one image")

    # images: src starts with http, name non-empty string
    for i, img in enumerate(p.get("images", [])):
        src = img.get("src")
        if not isinstance(src, str) or not src.strip():
            err(pid, f"image[{i}] src is not a valid non-empty string")
        elif not src.startswith("http"):
            err(pid, f"image[{i}] src is not a valid URL: {src!r}")
        if not isinstance(img.get("name"), str) or not img["name"].strip():
            err(pid, f"image[{i}] name is not a valid non-empty string")

    # attributes: name non-empty string; each option non-empty string
    for a in p.get("attributes", []):
        if not isinstance(a.get("name"), str) or not a["name"].strip():
            err(pid, f"attribute name is not a valid non-empty string: {a}")
        for opt in a.get("options", []):
            if not isinstance(opt, str) or not opt.strip():
                err(pid, f"attribute '{a.get('name')}' has empty option: {opt!r}")

    # variations: list of numbers
    for v in p.get("variations", []):
        if not isinstance(v, (int, float)):
            err(pid, f"variation ID is not a number: {v!r}")


# ── Outputs ───────────────────────────────────────────────────────────────────
valid   = [p for p in data if p["id"] not in product_errors]
flagged = [
    {"reasons": product_errors[p["id"]], "product": p}
    for p in data if p["id"] in product_errors
]

with open(out_dir / "products.json", "w", encoding="utf-8") as f:
    json.dump(valid, f, indent=2, ensure_ascii=False)

with open(out_dir / "flagged.json", "w", encoding="utf-8") as f:
    json.dump(flagged, f, indent=2, ensure_ascii=False)

# ── Console summary ───────────────────────────────────────────────────────────
total_issues = sum(len(v) for v in product_errors.values())

print(f"Validated {len(data)} products\n")
print(f"  Passed:  {len(valid)}")
print(f"  Flagged: {len(flagged)}  ({total_issues} issues)\n")

for p in data:
    pid = p["id"]
    name = (p.get("name") or "")[:45]
    for e in product_errors.get(pid, []):
        print(f"  [ERROR] id={pid} | {name} | {e}")

print(f"\nSaved → {out_dir / 'products.json'} ({len(valid)} products)")
print(f"Saved → {out_dir / 'flagged.json'} ({len(flagged)} flagged)")

if not product_errors:
    print(f"\n  → Next: python pipeline/fetch_variations.py")
