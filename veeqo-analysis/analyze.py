import csv
import re
from collections import defaultdict
from pathlib import Path

VEEQO_DIR = Path(__file__).parent


def load_rows(path):
    if path.suffix == ".xlsx":
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb.active
        raw_rows = list(ws.iter_rows(values_only=True))
        headers  = [str(h).strip() if h is not None else "" for h in raw_rows[0]]
        return [
            dict(zip(headers, (str(v).strip() if v is not None else "" for v in row)))
            for row in raw_rows[1:]
        ]
    else:
        with open(path, newline="", encoding="utf-8-sig") as f:
            return list(csv.DictReader(f))


xlsx_files = sorted(VEEQO_DIR.glob("*.xlsx"))
csv_files  = sorted(VEEQO_DIR.glob("sellables_export*.csv"))

if xlsx_files:
    path = xlsx_files[-1]
elif csv_files:
    path = csv_files[-1]
else:
    raise SystemExit(f"No export file (.xlsx or sellables_export*.csv) found in {VEEQO_DIR}")

rows = load_rows(path)

# ── Partition rows ─────────────────────────────────────────────────────────────

rows_no_sku   = [r for r in rows if not r.get("sku_code", "").strip()]
rows_with_sku = [r for r in rows if r.get("sku_code", "").strip()]

def get_sku(r):
    return r.get("sku_code", "").strip()

def parse_price(r):
    raw = r.get("sales_price", "").strip()
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None

# ── Per-SKU groups ─────────────────────────────────────────────────────────────

sku_groups = defaultdict(list)
for r in rows_with_sku:
    sku_groups[get_sku(r)].append(r)

# ── Findings counts ────────────────────────────────────────────────────────────

PLACEHOLDER_RE = re.compile(r'^none\d*$', re.IGNORECASE)
ALL_DIGITS_RE  = re.compile(r'^\d+$')

skus_with_spaces    = sum(1 for s in sku_groups if ' ' in s)
skus_placeholder    = sum(1 for s in sku_groups if PLACEHOLDER_RE.match(s) or ALL_DIGITS_RE.match(s))
skus_dup_total      = sum(1 for g in sku_groups.values() if len(g) > 1)
skus_dup_price_diff = 0
skus_zero_price     = 0

for s, group in sku_groups.items():
    prices = [p for p in (parse_price(r) for r in group) if p is not None]
    if len(set(prices)) > 1:
        skus_dup_price_diff += 1
    if any(p == 0.0 for p in prices):
        skus_zero_price += 1

# ── Issues per SKU ─────────────────────────────────────────────────────────────

sku_issues = defaultdict(list)

for s, group in sku_groups.items():
    if PLACEHOLDER_RE.match(s):
        sku_issues[s].append("[PLACEHOLDER]      matches 'none*' Amazon placeholder pattern — reused across unrelated products")
    elif ALL_DIGITS_RE.match(s):
        sku_issues[s].append(f"[PLACEHOLDER]      all-digit SKU ({s!r}) — likely a vendor/supplier code, not a product SKU")

    prices = [p for p in (parse_price(r) for r in group) if p is not None]

    if any(p == 0.0 for p in prices):
        zero_count = sum(1 for p in prices if p == 0.0)
        sku_issues[s].append(f"[ZERO PRICE]       {zero_count} of {len(group)} rows priced at $0.00")

    if len(group) > 1:
        unique_prices = sorted(set(prices))
        if len(unique_prices) > 1:
            price_str = "  ".join(f"${p:.2f}" for p in unique_prices)
            highest   = max(unique_prices)
            sku_issues[s].append(
                f"[PRICE CONFLICT]   {len(group)} rows — prices: {price_str}  ← highest: ${highest:.2f}"
            )

# ── Print findings ─────────────────────────────────────────────────────────────

W = 62
print(f"Veeqo Export Analysis — {path.name}")
print("═" * W)

print(f"\n── Overview ──")
print(f"  Total rows:               {len(rows):>7,}")
print(f"  Rows with SKU:            {len(rows_with_sku):>7,}")
print(f"  Rows without SKU:         {len(rows_no_sku):>7,}  ← recommend assigning or deleting")
print(f"  Unique SKUs:              {len(sku_groups):>7,}")

print(f"\n── SKU quality ──")
print(f"  Clean:                    {len(sku_groups) - skus_with_spaces - skus_placeholder:>7,}")
print(f"  Contain spaces:           {skus_with_spaces:>7,}  (not flagged — acknowledged, they connect and work)")
print(f"  Placeholders:             {skus_placeholder:>7,}  (flagged)")

print(f"\n── Duplicates ──")
print(f"  SKUs appearing 2+ times:  {skus_dup_total:>7,}")
print(f"  Of which, price differs:  {skus_dup_price_diff:>7,}  (flagged)")
print(f"  Same price duplicates:    {skus_dup_total - skus_dup_price_diff:>7,}  (not flagged — same SKU on multiple channels is expected)")

print(f"\n── Price ──")
all_prices = [p for g in sku_groups.values() for p in (parse_price(r) for r in g) if p is not None and p > 0]
print(f"  Non-zero price rows:      {len(all_prices):>7,}")
print(f"  Zero price SKUs:          {skus_zero_price:>7,}  (flagged)")
if all_prices:
    print(f"  Range: ${min(all_prices):.2f} – ${max(all_prices):.2f}   Mean: ${sum(all_prices)/len(all_prices):.2f}")

print(f"\n── Stock ──")
stock_vals = []
for r in rows_with_sku:
    raw = r.get("qty_on_hand", "").strip()
    try:
        f = float(raw)
        stock_vals.append(int(f) if f != float("inf") else 0)
    except (ValueError, TypeError):
        stock_vals.append(0)
zero_stock = sum(1 for s in stock_vals if s == 0)
pos_stock  = sum(1 for s in stock_vals if s > 0)
print(f"  Zero stock rows:          {zero_stock:>7,}  ({zero_stock/len(rows_with_sku)*100:.1f}%)")
print(f"  Positive stock rows:      {pos_stock:>7,}  ({pos_stock/len(rows_with_sku)*100:.1f}%)")
print(f"  Total qty on hand:        {sum(stock_vals):>7,}")

# ── Print issues ───────────────────────────────────────────────────────────────

print(f"\n{'═' * W}")
actionable   = {s: issues for s, issues in sku_issues.items() if issues}
total_issues = sum(len(v) for v in actionable.values())
print(f"\n── Issues — {len(actionable)} SKUs, {total_issues} total problems ──\n")

for s in sorted(actionable):
    print(f"  SKU: {s}")
    for issue in actionable[s]:
        print(f"    {issue}")
    print()

# ── Rows without SKU ──────────────────────────────────────────────────────────

print(f"{'═' * W}")
print(f"\n── Rows without SKU ({len(rows_no_sku)}) ── recommend assigning an SKU or deleting\n")

for i, r in enumerate(rows_no_sku, 1):
    title   = r.get("product_title", "").strip()[:50]
    variant = r.get("variant_title", "").strip()[:30]
    price   = r.get("sales_price", "").strip()
    label   = title + (f" / {variant}" if variant else "")
    print(f"  {i:>3}.  {label}  (${price})")
