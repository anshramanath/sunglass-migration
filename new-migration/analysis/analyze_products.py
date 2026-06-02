import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).parent.parent
data = json.loads((BASE / "data/prosport/fetch-products/products.json").read_text())

total = len(data)
variable = [p for p in data if p["type"] == "variable"]
simple = [p for p in data if p["type"] == "simple"]

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
print(f"  Top categories:")
for name, n in cat_usage.most_common(10):
    print(f"    {name}: {n}")

# ── Attributes ────────────────────────────────────────────────────────────────
attr_usage = Counter(a["name"] for p in data for a in p.get("attributes", []))
print(f"\nAttributes: {len(attr_usage)} unique names")
print(f"  Products with no attributes: {sum(1 for p in data if not p.get('attributes'))}")
for name, n in attr_usage.most_common():
    print(f"    {name}: {n} products")

# ── Pricing ───────────────────────────────────────────────────────────────────
print(f"\nPricing (parent-level):")
print(f"  Has price: {sum(1 for p in data if p.get('price'))}")
print(f"  Has regular_price: {sum(1 for p in data if p.get('regular_price'))}")
print(f"  on_sale=True: {sum(1 for p in data if p.get('on_sale'))}")

# ── Stock ─────────────────────────────────────────────────────────────────────
print(f"\nStock (parent-level):")
print(f"  manage_stock=True: {sum(1 for p in data if p.get('manage_stock'))}")
print(f"  stock_status: {dict(Counter(p.get('stock_status') for p in data))}")

# ── Descriptions ──────────────────────────────────────────────────────────────
print(f"\nDescriptions:")
print(f"  Has description: {sum(1 for p in data if p.get('description', '').strip())} / {total}")
print(f"  Has short_description: {sum(1 for p in data if p.get('short_description', '').strip())} / {total}")

# ── Flags ─────────────────────────────────────────────────────────────────────
print(f"\nFlags:")
print(f"  Draft variable products: {sum(1 for p in variable if p['status'] == 'draft')}")
print(f"  Published variable products: {sum(1 for p in variable if p['status'] == 'publish')}")
print(f"  Published simple products: {sum(1 for p in simple if p['status'] == 'publish')}")

# ── Field coverage ────────────────────────────────────────────────────────────
def is_meaningful(val):
    if val is None:
        return False
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
        return "object" if val else "{}"
    if isinstance(val, bool):
        return str(val)
    s = str(val).strip()
    return s if s else '""'

SKIP = {"_links", "price_html"}
fields = [k for k in data[0].keys() if k not in SKIP]

print(f"\n\n=== Field coverage ({total} products) ===\n")
print(f"{'field':<30} {'filled':>6}  {'%':>5}  top values")
print("-" * 90)

for field in fields:
    values = [p.get(field) for p in data]
    filled = sum(1 for v in values if is_meaningful(v))
    pct = filled / total * 100
    top = Counter(summarize(v) for v in values).most_common(4)
    top_str = "  ".join(f"{label}×{n}" for label, n in top)
    print(f"{field:<30} {filled:>6}  {pct:>4.0f}%  {top_str}")
