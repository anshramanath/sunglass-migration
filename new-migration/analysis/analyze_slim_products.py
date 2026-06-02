import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).parent.parent
data = json.loads((BASE / "data/prosport/slim-products/products.json").read_text())
N = len(data)

print(f"=== Slim Products ({N} total) ===\n")

# ── Field presence ─────────────────────────────────────────────────────────────
def filled(p, field):
    v = p.get(field)
    if field == "dimensions":
        return isinstance(v, dict) and all(v.get(k, "") not in ("", None) for k in ("length", "width", "height"))
    if field == "categories":
        return isinstance(v, list) and len(v) > 0
    if field == "images":
        return isinstance(v, list) and len(v) > 0
    return v not in (None, "", [], {}, "0.00")

print("Field presence:")
for field in data[0].keys():
    n = sum(1 for p in data if filled(p, field))
    missing = N - n
    print(f"  {field:<20} {n:>4}/{N}  {'OK' if n == N else f'MISSING {missing}'}")

# ── Flags ──────────────────────────────────────────────────────────────────────
print("\n--- flags ---")
drafts  = [p for p in data if p.get("status") == "draft"]
no_sku  = [p for p in data if not p.get("sku")]
print(f"  Draft products:   {len(drafts)}")
for p in drafts:
    print(f"    [{p['id']}] {p['name']}")
print(f"  No SKU:           {len(no_sku)}")
for p in no_sku:
    print(f"    [{p['id']}] {p['name']}")

# ── type vs variations consistency ────────────────────────────────────────────
print("\n--- type vs variations ---")
variable = [p for p in data if p["type"] == "variable"]
simple   = [p for p in data if p["type"] == "simple"]

var_no_variations     = [p for p in variable if not p["variations"]]
simple_has_variations = [p for p in simple if p["variations"]]

print(f"  variable with no variations:   {len(var_no_variations)}")
for p in var_no_variations:
    print(f"    {p['name']} (id={p['id']})")
print(f"  simple with variations:        {len(simple_has_variations)}")
for p in simple_has_variations:
    print(f"    {p['name']} (id={p['id']})")

# ── on_sale truthfulness ──────────────────────────────────────────────────────
print("\n--- on_sale vs sale_price ---")
on_sale_no_price  = [p for p in data if p.get("on_sale") and not p.get("sale_price")]
has_price_no_sale = [p for p in data if p.get("sale_price") and not p.get("on_sale")]
print(f"  on_sale=True but no sale_price:  {len(on_sale_no_price)}")
for p in on_sale_no_price[:10]:
    print(f"    [{p['id']}] {p['name']}  type={p['type']}  price={p.get('price')}  regular={p.get('regular_price')}")
print(f"  has sale_price but on_sale=False: {len(has_price_no_sale)}")
for p in has_price_no_sale:
    print(f"    [{p['id']}] {p['name']}")

# ── stock_quantity vs stock_status ────────────────────────────────────────────
print("\n--- stock_quantity vs stock_status ---")
combos = Counter(
    (p["stock_quantity"] is not None, p["stock_status"])
    for p in data
)
print("  (has_qty, stock_status):")
for (has_qty, status), n in sorted(combos.items()):
    print(f"    has_qty={has_qty}  stock_status={status:<12}  {n} products")

no_qty_out = [p for p in data if p["stock_quantity"] is None and p["stock_status"] == "outofstock"]
print(f"\n  no quantity + outofstock: {len(no_qty_out)}")
for p in no_qty_out:
    print(f"    {p['name']}")

# ── featured & total_sales ───────────────────────────────────────────────────
print("\n--- featured ---")
featured = [p for p in data if p.get("featured")]
print(f"  Featured products: {len(featured)}")
for p in featured:
    print(f"    [{p['id']}] {p['name']}")

print("\n--- total_sales ---")
has_sales   = [p for p in data if p.get("total_sales")]
zero_sales  = [p for p in data if p.get("total_sales") == 0]
null_sales  = [p for p in data if p.get("total_sales") is None]
sale_counts = Counter(p["total_sales"] for p in data if p.get("total_sales"))
print(f"  Has sales (>0):   {len(has_sales)}")
print(f"  Zero sales:       {len(zero_sales)}")
print(f"  Null:             {len(null_sales)}")
print(f"  Top values:       {sale_counts.most_common(5)}")

# ── categories ────────────────────────────────────────────────────────────────
print("\n--- categories ---")
unique_cats = dict((c["slug"], c["name"]) for p in data for c in p["categories"])
cat_usage = Counter(c["name"] for p in data for c in p["categories"])
print(f"  Unique categories: {len(unique_cats)}")
for name, n in cat_usage.most_common():
    print(f"    {name}: {n}")

# ── related_ids ───────────────────────────────────────────────────────────────
print("\n--- related_ids ---")
all_related   = [rid for p in data for rid in p["related_ids"]]
unique_related = set(all_related)
known_ids      = {p["id"] for p in data}
external       = [rid for rid in unique_related if rid not in known_ids]
counts         = Counter(len(p["related_ids"]) for p in data)
print(f"  Products with related_ids:    {sum(1 for p in data if p['related_ids'])} / {N}")
print(f"  Total entries:                {len(all_related)}")
print(f"  Unique IDs:                   {len(unique_related)}")
print(f"  IDs outside this set:         {len(external)}")
print(f"  Count distribution:           {dict(sorted(counts.items()))}")
