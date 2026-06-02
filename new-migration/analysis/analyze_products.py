import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).parent.parent
data = json.loads((BASE / "data/prosport/fetch-items/products.json").read_text())

total = len(data)
print(f"=== Products ({total} total) ===\n")

# --- Type breakdown ---
types = Counter(p["type"] for p in data)
print("Types:")
for t, n in types.most_common():
    print(f"  {t}: {n}")

# --- Status breakdown ---
statuses = Counter(p["status"] for p in data)
print("\nStatuses:")
for s, n in statuses.most_common():
    print(f"  {s}: {n}")

# --- Variation ID counts ---
variable = [p for p in data if p["type"] == "variable"]
variation_counts = [len(p["variations"]) for p in variable]
print(f"\nVariable products: {len(variable)}")
print(f"  Variation IDs total: {sum(variation_counts)}")
print(f"  Per-product: min={min(variation_counts)} max={max(variation_counts)} avg={sum(variation_counts)/len(variation_counts):.1f}")

# --- Simple products ---
simple = [p for p in data if p["type"] == "simple"]
print(f"\nSimple products: {len(simple)}")
with_sku = sum(1 for p in simple if p.get("sku"))
print(f"  With SKU: {with_sku} / {len(simple)}")

# --- SKUs ---
all_skus = [p["sku"] for p in data if p.get("sku")]
dup_skus = {sku for sku, n in Counter(all_skus).items() if n > 1}
print(f"\nSKUs: {len(all_skus)} total, {len(set(all_skus))} unique, {len(dup_skus)} duplicates")
if dup_skus:
    for s in sorted(dup_skus)[:5]:
        print(f"  dup: {s}")

# --- Images ---
no_img = [p for p in data if not p.get("images")]
multi_img = [p for p in data if len(p.get("images", [])) > 1]
img_counts = Counter(len(p.get("images", [])) for p in data)
print(f"\nProduct images:")
print(f"  No images: {len(no_img)}")
print(f"  Multiple images: {len(multi_img)}")
print(f"  Count distribution: {dict(sorted(img_counts.items()))}")

# --- Categories ---
all_cats = [(c["id"], c["name"]) for p in data for c in p.get("categories", [])]
unique_cats = dict(all_cats)
cat_usage = Counter(c["name"] for p in data for c in p.get("categories", []))
no_cat = [p for p in data if not p.get("categories")]
print(f"\nCategories: {len(unique_cats)} unique")
print(f"  Products with no category: {len(no_cat)}")
print(f"  Top categories:")
for name, n in cat_usage.most_common(10):
    print(f"    {name}: {n}")

# --- Attributes ---
attr_usage = Counter(a["name"] for p in data for a in p.get("attributes", []))
no_attr = [p for p in data if not p.get("attributes")]
print(f"\nAttributes: {len(attr_usage)} unique names")
print(f"  Products with no attributes: {len(no_attr)}")
for name, n in attr_usage.most_common():
    print(f"    {name}: {n} products")

# --- Pricing (parent level, mainly informational) ---
has_price = [p for p in data if p.get("price")]
has_regular = [p for p in data if p.get("regular_price")]
on_sale = [p for p in data if p.get("on_sale")]
print(f"\nPricing (parent-level):")
print(f"  Has price: {len(has_price)}")
print(f"  Has regular_price: {len(has_regular)}")
print(f"  on_sale=True: {len(on_sale)}")

# --- Stock (parent level) ---
manage_stock = [p for p in data if p.get("manage_stock")]
stock_statuses = Counter(p.get("stock_status") for p in data)
print(f"\nStock (parent-level):")
print(f"  manage_stock=True: {len(manage_stock)}")
print(f"  stock_status distribution: {dict(stock_statuses)}")

# --- Descriptions ---
has_desc = sum(1 for p in data if p.get("description", "").strip())
has_short = sum(1 for p in data if p.get("short_description", "").strip())
print(f"\nDescriptions:")
print(f"  Has description: {has_desc} / {total}")
print(f"  Has short_description: {has_short} / {total}")

# --- Flags ---
draft_with_vars = [p for p in variable if p["status"] == "draft"]
print(f"\nFlags:")
print(f"  Draft variable products: {len(draft_with_vars)}")
print(f"  Published variable products: {sum(1 for p in variable if p['status'] == 'publish')}")
print(f"  Published simple products: {sum(1 for p in simple if p['status'] == 'publish')}")
