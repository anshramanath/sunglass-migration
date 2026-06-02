import json
import os
from collections import Counter
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

items   = json.loads((data_dir / "create-items" / "items.json").read_text())
flagged = json.loads((data_dir / "create-items" / "flagged.json").read_text())

variables = [p for p in items if p["type"] == "variable"]
simples   = [p for p in items if p["type"] == "simple"]
all_vars  = [v for p in variables for v in p.get("variations", [])]

def pct(n, total):
    return f"{n}/{total} ({100*n/total:.1f}%)" if total else "0/0"

def filled(v):
    if v is None: return False
    if isinstance(v, list): return len(v) > 0
    return True

print(f"{'='*60}")
print(f"  CREATE ITEMS AUDIT — {brand_name}")
print(f"{'='*60}")
print(f"  Items:    {len(items)}  (variable: {len(variables)}, simple: {len(simples)})")
print(f"  Flagged:  {len(flagged)}")
print(f"  Variations embedded: {len(all_vars)}")

# ── Pricing ───────────────────────────────────────────────────────────────────
print(f"\n── Pricing (variable products) ──")
min_prices = [p["minPriceCents"] for p in variables if p.get("minPriceCents")]
max_prices = [p["maxPriceCents"] for p in variables if p.get("maxPriceCents")]
print(f"  minPriceCents range: {min(min_prices)}–{max(min_prices)} (${min(min_prices)/100:.2f}–${max(min_prices)/100:.2f})")
print(f"  maxPriceCents range: {min(max_prices)}–{max(max_prices)} (${min(max_prices)/100:.2f}–${max(max_prices)/100:.2f})")
var_sale = sum(1 for p in variables if p.get("sale"))
print(f"  sale=True: {pct(var_sale, len(variables))}")

print(f"\n── Pricing (simple products) ──")
print(f"  sale=True: {sum(1 for p in simples if p.get('sale'))}/{len(simples)}")
if simples:
    sp = [p["minPriceCents"] for p in simples if p.get("minPriceCents")]
    print(f"  minPriceCents range: {min(sp)}–{max(sp)} (${min(sp)/100:.2f}–${max(sp)/100:.2f})")

# ── Variations ────────────────────────────────────────────────────────────────
print(f"\n── Variations per product ──")
vcounts = sorted(len(p["variations"]) for p in variables)
print(f"  min: {min(vcounts)}  max: {max(vcounts)}  avg: {sum(vcounts)/len(vcounts):.1f}")

# ── Image dedup ───────────────────────────────────────────────────────────────
print(f"\n── Variation image dedup ──")
nulled   = sum(1 for v in all_vars if v.get("image") is None)
has_img  = sum(1 for v in all_vars if v.get("image") is not None)
print(f"  image=null (deduped or none): {nulled}")
print(f"  image present:                {has_img}")

# ── Attributes ────────────────────────────────────────────────────────────────
print(f"\n── Product attributes (post-expansion + prune) ──")
attr_counter = Counter(a["name"] for p in items for a in p.get("attributes", []))
for name, count in attr_counter.most_common():
    opts = {o for p in items for a in p.get("attributes", []) if a["name"] == name for o in a.get("options", [])}
    print(f"  {name:<14} {count:>4} products  {len(opts):>4} unique options")

print(f"\n── Variation attributes ──")
vattr_counter = Counter(a["name"] for v in all_vars for a in v.get("attributes", []))
for name, count in vattr_counter.most_common():
    opts = {a["option"] for v in all_vars for a in v.get("attributes", []) if a["name"] == name}
    print(f"  {name:<14} {count:>6} variations  {len(opts):>4} unique options")

# ── Stock ─────────────────────────────────────────────────────────────────────
print(f"\n── Product stock ──")
print(f"  stock=0:  {sum(1 for p in items if p.get('stock') == 0)}")
print(f"  stock=1:  {sum(1 for p in items if p.get('stock') == 1)}")
print(f"  stock>1:  {sum(1 for p in items if isinstance(p.get('stock'), int) and p['stock'] > 1)}")

print(f"\n── Variation stock ──")
print(f"  stock=0:  {sum(1 for v in all_vars if v.get('stock') == 0)}")
print(f"  stock=1:  {sum(1 for v in all_vars if v.get('stock') == 1)}")
print(f"  stock>1:  {sum(1 for v in all_vars if isinstance(v.get('stock'), int) and v['stock'] > 1)}")

# ── Flagged ───────────────────────────────────────────────────────────────────
if flagged:
    print(f"\n── Flagged products ──")
    for entry in flagged:
        p = entry["product"]
        print(f"  id={p['id']} {p.get('name','')[:45]}")
        for r in entry["reasons"]:
            print(f"    · {r}")
