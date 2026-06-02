import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).parent.parent
data = json.loads((BASE / "data/prosport/fetch-products/products.json").read_text())

total = len(data)
variable = [p for p in data if p["type"] == "variable"]
simple   = [p for p in data if p["type"] == "simple"]

# ── Overview ──────────────────────────────────────────────────────────────────
print(f"=== Products ({total} total) ===\n")

types = Counter(p["type"] for p in data)
print("Types:")
for t, n in types.most_common():
    print(f"  {t}: {n}")

statuses = Counter(p["status"] for p in data)
print("\nStatuses:")
for s, n in statuses.most_common():
    print(f"  {s}: {n}")

# ── Variations ────────────────────────────────────────────────────────────────
var_counts = [len(p["variations"]) for p in variable]
print(f"\nVariable products: {len(variable)}")
print(f"  Variation IDs total: {sum(var_counts)}")
print(f"  Per-product: min={min(var_counts)} max={max(var_counts)} avg={sum(var_counts)/len(var_counts):.1f}")

simple_var_counts = [len(p.get("variations", [])) for p in simple]
print(f"\nSimple products: {len(simple)}")
print(f"  Variation IDs total: {sum(simple_var_counts)}")
print(f"  With SKU: {sum(1 for p in simple if p.get('sku'))} / {len(simple)}")

# ── SKUs ──────────────────────────────────────────────────────────────────────
all_skus = [p["sku"] for p in data if p.get("sku")]
dup_skus = {sku for sku, n in Counter(all_skus).items() if n > 1}
print(f"\nSKUs: {len(all_skus)} total, {len(set(all_skus))} unique, {len(dup_skus)} duplicates")
for s in sorted(dup_skus)[:5]:
    print(f"  dup: {s}")

# ── Images ────────────────────────────────────────────────────────────────────
img_counts = Counter(len(p.get("images", [])) for p in data)
print(f"\nProduct images:")
print(f"  No images: {sum(1 for p in data if not p.get('images'))}")
print(f"  Multiple images: {sum(1 for p in data if len(p.get('images', [])) > 1)}")
print(f"  Count distribution: {dict(sorted(img_counts.items()))}")

# ── Categories ────────────────────────────────────────────────────────────────
unique_cats = dict((c["id"], c["name"]) for p in data for c in p.get("categories", []))
cat_usage = Counter(c["name"] for p in data for c in p.get("categories", []))
print(f"\nCategories: {len(unique_cats)} unique")
print(f"  Products with no category: {sum(1 for p in data if not p.get('categories'))}")
for name, n in cat_usage.most_common():
    print(f"    {name}: {n}")

# ── Attributes ────────────────────────────────────────────────────────────────
attr_usage = Counter(a["name"] for p in data for a in p.get("attributes", []))
print(f"\nAttributes: {len(attr_usage)} unique names")
print(f"  Products with no attributes: {sum(1 for p in data if not p.get('attributes'))}")
for name, n in attr_usage.most_common():
    print(f"    {name}: {n} products")

# ── Pricing ───────────────────────────────────────────────────────────────────
print(f"\nPricing (parent-level):")
print(f"  Has price:         {sum(1 for p in data if p.get('price'))}")
print(f"  Has regular_price: {sum(1 for p in data if p.get('regular_price'))}")
print(f"  Has sale_price:    {sum(1 for p in data if p.get('sale_price'))}")
on_sale_no_price = [p for p in data if p.get("on_sale") and not p.get("sale_price")]
print(f"  on_sale=True but no sale_price: {len(on_sale_no_price)} (all type=variable, WC quirk)")

# ── Stock ─────────────────────────────────────────────────────────────────────
print(f"\nStock (parent-level):")
print(f"  manage_stock=True: {sum(1 for p in data if p.get('manage_stock'))}")
print(f"  stock_status: {dict(Counter(p.get('stock_status') for p in data))}")

# ── Dimensions ────────────────────────────────────────────────────────────────
def dims_filled(p):
    d = p.get("dimensions", {})
    return all(d.get(k, "") not in ("", None) for k in ("length", "width", "height"))

print(f"\nDimensions:")
print(f"  All subfields populated: {sum(1 for p in data if dims_filled(p))} / {total}")

# ── Descriptions ──────────────────────────────────────────────────────────────
print(f"\nDescriptions:")
print(f"  Has description:       {sum(1 for p in data if p.get('description', '').strip())} / {total}")
print(f"  Has short_description: {sum(1 for p in data if p.get('short_description', '').strip())} / {total}")

# ── total_sales & featured ─────────────────────────────────────────────────────
print(f"\ntotal_sales:")
print(f"  > 0:  {sum(1 for p in data if p.get('total_sales'))}")
print(f"  = 0:  {sum(1 for p in data if p.get('total_sales') == 0)}")
top_sales = Counter(p.get("total_sales") for p in data if p.get("total_sales")).most_common(5)
print(f"  Top values: {top_sales}")

featured = [p for p in data if p.get("featured")]
print(f"\nFeatured: {len(featured)}")
for p in featured:
    print(f"  [{p['id']}] {p['name']}")

# ── Flags ─────────────────────────────────────────────────────────────────────
print(f"\nFlags:")
drafts = [p for p in data if p["status"] == "draft"]
no_sku = [p for p in data if not p.get("sku")]
for p in drafts:
    print(f"  draft:  [{p['id']}] {p['name']}")
for p in no_sku:
    print(f"  no sku: [{p['id']}] {p['name']} (type={p['type']})")

# ── Field coverage ────────────────────────────────────────────────────────────
def is_meaningful(field, val):
    if val is None:
        return False
    if field == "dimensions":
        return isinstance(val, dict) and all(val.get(k, "") not in ("", None) for k in ("length", "width", "height"))
    if val in ("", [], {}, 0, "0.00", "taxable"):
        return False
    if isinstance(val, bool):
        return val
    return True

def summarize(val):
    if val is None:
        return "null"
    if isinstance(val, list):
        return f"list[{len(val)}]" if val else "[]"
    if isinstance(val, dict):
        return "{...}" if val else "{}"
    if isinstance(val, bool):
        return str(val)
    s = str(val).strip()
    if not s:
        return '""'
    return s[:60] + ("…" if len(s) > 60 else "")

SKIP = {"_links", "price_html"}
fields = [k for k in data[0].keys() if k not in SKIP]

print(f"\n\n=== Field coverage ({total} products) ===\n")
print(f"{'field':<30} {'filled':>6}  {'%':>5}  top values")
print("-" * 90)

for field in fields:
    values = [p.get(field) for p in data]
    filled = sum(1 for v in values if is_meaningful(field, v))
    pct = filled / total * 100
    top = Counter(summarize(v) for v in values).most_common(4)
    top_str = "  ".join(f"{label}×{n}" for label, n in top)
    print(f"{field:<30} {filled:>6}  {pct:>4.0f}%  {top_str}")
