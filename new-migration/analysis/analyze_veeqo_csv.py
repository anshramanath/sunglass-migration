import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE


csv_candidates = sorted((BASE.parent).glob("sellables_export*.csv"))
if not csv_candidates:
    raise SystemExit(f"No sellables_export*.csv found in {BASE.parent}")
csv_path = csv_candidates[0]

rows = []
with open(csv_path, newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        rows.append(row)

total_rows    = len(rows)
rows_with_sku = [r for r in rows if r.get("sku_code", "").strip()]
rows_no_sku   = total_rows - len(rows_with_sku)
n             = len(rows_with_sku)

# ── SKU collisions ────────────────────────────────────────────────────────────

sku_counts = Counter(r["sku_code"].strip() for r in rows_with_sku)
unique_skus = len(sku_counts)
dup_skus    = {sku: c for sku, c in sku_counts.items() if c > 1}
dup_freq    = Counter(dup_skus.values())
extra_rows  = sum(c - 1 for c in dup_skus.values())

# ── Unique products ───────────────────────────────────────────────────────────

product_ids = {r.get("product_id", "").strip() for r in rows_with_sku if r.get("product_id", "").strip()}

# ── Price ─────────────────────────────────────────────────────────────────────

prices     = []
zero_price = 0
no_price   = 0
for r in rows_with_sku:
    raw = r.get("sales_price", "").strip()
    if not raw:
        no_price += 1
    else:
        try:
            p = float(raw)
            if p == 0:
                zero_price += 1
            else:
                prices.append(p)
        except ValueError:
            no_price += 1

sku_prices = defaultdict(set)
for r in rows_with_sku:
    sku = r["sku_code"].strip()
    raw = r.get("sales_price", "").strip()
    if sku and raw:
        try:
            sku_prices[sku].add(float(raw))
        except ValueError:
            pass

conflicting = {sku: sorted(ps) for sku, ps in sku_prices.items() if len(ps) > 1}

# ── Stock ─────────────────────────────────────────────────────────────────────

stock_values = []
for r in rows_with_sku:
    raw = r.get("qty_on_hand", "").strip()
    try:
        f = float(raw)
        stock_values.append(int(f) if f != float("inf") else 0)
    except (ValueError, TypeError):
        stock_values.append(0)

zero_stock     = sum(1 for s in stock_values if s == 0)
positive_stock = sum(1 for s in stock_values if s > 0)
total_stock    = sum(stock_values)

# ── Field coverage ────────────────────────────────────────────────────────────

has_description = sum(1 for r in rows_with_sku if r.get("description", "").strip())
has_image       = sum(1 for r in rows_with_sku if r.get("image_url", "").strip())
has_brand       = sum(1 for r in rows_with_sku if r.get("brand", "").strip())
has_upc         = sum(1 for r in rows_with_sku if r.get("upc_code", "").strip())

# ── Images ────────────────────────────────────────────────────────────────────

no_image  = sum(1 for r in rows_with_sku if not r.get("image_url", "").strip())
has_image = n - no_image

# ── Print ─────────────────────────────────────────────────────────────────────

print(f"Veeqo CSV analysis — {csv_path.name}")
print(f"{'─' * 60}")

print(f"\n── Overview ──")
print(f"  Total rows:         {total_rows:>7,}")
print(f"  Rows with SKU:      {n:>7,}")
print(f"  Rows without SKU:   {rows_no_sku:>7,}")
print(f"  Unique SKUs:        {unique_skus:>7,}")
print(f"  Unique product IDs: {len(product_ids):>7,}")

print(f"\n── SKU collisions ──")
print(f"  SKUs appearing once:     {unique_skus - len(dup_skus):>6,}")
print(f"  SKUs appearing 2+ times: {len(dup_skus):>6,}")
print(f"  Extra rows from dupes:   {extra_rows:>6,}")
for freq in sorted(dup_freq.keys(), reverse=True):
    print(f"    {freq}x: {dup_freq[freq]:,} SKUs")

print(f"\n── Price ──")
print(f"  With non-zero price: {len(prices):>7,}  ({len(prices)/n*100:.1f}%)")
print(f"  Zero price:          {zero_price:>7,}  ({zero_price/n*100:.1f}%)")
print(f"  No price:            {no_price:>7,}  ({no_price/n*100:.1f}%)")
if prices:
    print(f"  Min:  ${min(prices):.2f}")
    print(f"  Max:  ${max(prices):.2f}")
    print(f"  Mean: ${sum(prices)/len(prices):.2f}")
print(f"  Conflicting prices on dupe SKUs: {len(conflicting):,}")
if conflicting:
    for sku, ps in list(conflicting.items())[:5]:
        print(f"    {sku}: {[f'${p:.2f}' for p in ps]}")
    if len(conflicting) > 5:
        print(f"    ... and {len(conflicting) - 5} more")

print(f"\n── Stock ──")
print(f"  Zero stock:     {zero_stock:>7,}  ({zero_stock/n*100:.1f}%)")
print(f"  Positive stock: {positive_stock:>7,}  ({positive_stock/n*100:.1f}%)")
print(f"  Total qty:      {total_stock:>7,}")

print(f"\n── Images ──")
print(f"  With image:    {has_image:>7,}  ({has_image/n*100:.1f}%)")
print(f"  Without image: {no_image:>7,}  ({no_image/n*100:.1f}%)")
print(f"  (1 image_url field per row — max 1 image per variant)")

print(f"\n── Field coverage ──")
print(f"  Description: {has_description:,} / {n:,}  ({has_description/n*100:.1f}%)")
print(f"  Brand:       {has_brand:,} / {n:,}  ({has_brand/n*100:.1f}%)")
print(f"  UPC:         {has_upc:,} / {n:,}  ({has_upc/n*100:.1f}%)")
