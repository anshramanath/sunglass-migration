import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand


brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]
data_dir = BASE / "data" / slug

items   = json.loads((data_dir / "veeqo-items" / "items.json").read_text())
flagged = json.loads((data_dir / "veeqo-items" / "flagged.json").read_text())

SEP  = "=" * 68
DASH = "─" * 68

def cents(c):
    return f"${c/100:.2f}" if c is not None else "null"

variables = [p for p in items if p["type"] == "variable"]
simples   = [p for p in items if p["type"] == "simple"]
all_vars  = [v for p in variables for v in p.get("variations", []) if isinstance(v, dict)]

flagged_products = [e["product"] for e in flagged]
flagged_variable = [p for p in flagged_products if p["type"] == "variable"]
flagged_simple   = [p for p in flagged_products if p["type"] == "simple"]

print(SEP)
print(f"  VEEQO ITEMS — ANALYSIS   {brand_name}")
print(SEP)
print(f"\n  Passed:  {len(items)}  (variable: {len(variables)}, simple: {len(simples)})")
print(f"  Flagged: {len(flagged)}  (variable: {len(flagged_variable)}, simple: {len(flagged_simple)})")
print(f"  Variations in passed items: {len(all_vars)}")

# ── Passed items overview ─────────────────────────────────────────────────────
print(f"\n{DASH}")
print(f"  PASSED — overview")
print(DASH)

reg_prices = [v["regularPriceCents"] for v in all_vars if v.get("regularPriceCents")]
if reg_prices:
    print(f"  Variation regularPriceCents: {min(reg_prices)}–{max(reg_prices)}  ({cents(min(reg_prices))}–{cents(max(reg_prices))})")

stock_vals = [v["stock"] for v in all_vars if v.get("stock") is not None]
print(f"  Variation stock=0 (out of stock): {sum(1 for s in stock_vals if s == 0)}")
print(f"  Variation stock>0:               {sum(1 for s in stock_vals if isinstance(s, int) and s > 0)}")

simple_prices = [p["minPriceCents"] for p in simples if p.get("minPriceCents")]
if simple_prices:
    print(f"  Simple product price range: {cents(min(simple_prices))}–{cents(max(simple_prices))}")

attr_counter = Counter(a["name"] for p in items for a in p.get("attributes", []))
print(f"\n  Product attributes (top 5):")
for name, count in attr_counter.most_common(5):
    print(f"    {name:<20} {count} products")

# ── Flagged items detail ──────────────────────────────────────────────────────
print(f"\n{DASH}")
print(f"  FLAGGED — detail")
print(DASH)

if not flagged:
    print(f"  None.")
else:
    all_missing = []
    for entry in flagged:
        p    = entry["product"]
        reasons = entry["reasons"]
        missing_skus = [r.split("'")[1] for r in reasons if "not in Veeqo" in r]
        all_missing.extend(missing_skus)

        total_vars = len([v for v in p.get("variations", []) if isinstance(v, dict)])
        pct_missing = f"{100*len(missing_skus)/total_vars:.0f}%" if total_vars else "—"

        print(f"\n  id={p['id']}  {p['name']}")
        print(f"    type: {p['type']}  |  total variations: {total_vars}  |  missing: {len(missing_skus)} ({pct_missing})")

        if total_vars and len(missing_skus) == total_vars:
            print(f"    → entirely absent from Veeqo")
        else:
            present = total_vars - len(missing_skus)
            print(f"    → {present} variations present in Veeqo, {len(missing_skus)} missing")

        # show power/suffix pattern of missing SKUs
        suffixes = sorted({sku.rsplit("-", 2)[-2] for sku in missing_skus
                           if sku.endswith("-MFS") or sku.endswith("-MFB")}, key=lambda x: (len(x), x))
        if suffixes:
            print(f"    missing powers: {suffixes}")
        else:
            suffixes_raw = sorted({sku.split("-")[-1] for sku in missing_skus})
            print(f"    missing SKU suffixes: {suffixes_raw}")

        print(f"    categories: {[c['name'] for c in p.get('categories', [])]}")

    # ── Aggregate missing SKU stats ───────────────────────────────────────────
    print(f"\n{DASH}")
    print(f"  FLAGGED — aggregate")
    print(DASH)
    print(f"  Total missing SKUs across all flagged products: {len(all_missing)}")

    entirely_absent = sum(1 for e in flagged
                          if len([r for r in e["reasons"] if "not in Veeqo" in r]) ==
                             len([v for v in e["product"].get("variations", []) if isinstance(v, dict)]))
    partial = len(flagged) - entirely_absent
    print(f"  Entirely absent from Veeqo (all variations missing): {entirely_absent}")
    print(f"  Partially missing (some variations present):         {partial}")

    power_suffixes = Counter()
    for sku in all_missing:
        parts = sku.split("-")
        if sku.endswith("-MFS") or sku.endswith("-MFB"):
            power_suffixes[parts[-2]] += 1
    if power_suffixes:
        print(f"\n  Missing SKU power breakdown:")
        for power, count in sorted(power_suffixes.items(), key=lambda x: (len(x[0]), x[0])):
            print(f"    {power:<6} {count} SKUs")

print(f"\n{SEP}")
print(f"  END OF ANALYSIS")
print(SEP)
