import json
import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

BASE = Path(__file__).parent.parent  # migration/
load_dotenv(dotenv_path=BASE.parent / ".env")

with open(BASE / "recategorized/categorized_items.json") as f:
    items = json.load(f)

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

errors = []
ok = []

def check(name, passed, detail=""):
    (ok if passed else errors).append(f"{name}{': ' + detail if detail else ''}")

# ── 1. Product count matches ──────────────────────────────────────────────────

cur.execute("SELECT COUNT(*) FROM products;")
db_count = cur.fetchone()[0]
check(f"Product count matches ({db_count} in DB, {len(items)} expected)",
      db_count == len(items))

# ── 2. Every SKU in categorized_items is in DB ────────────────────────────────

source_skus = {i["sku"] for i in items}
cur.execute("SELECT sku FROM products;")
db_skus = {row[0] for row in cur.fetchall()}

missing = source_skus - db_skus
extra = db_skus - source_skus
check("All source SKUs present in DB", not missing, f"{len(missing)} missing: {list(missing)[:3]}")
check("No extra SKUs in DB", not extra, f"{list(extra)[:3]}")

# ── 3. Spot-check price and name on first 5 items ────────────────────────────

mismatches = []
for item in items[:5]:
    cur.execute("SELECT name, regular_price_cents, sale_price_cents FROM products WHERE sku = %s;", (item["sku"],))
    row = cur.fetchone()
    if not row:
        mismatches.append(f"{item['sku']}: not found")
        continue
    name, reg, sale = row
    if name != item["name"]:
        mismatches.append(f"{item['sku']}: name mismatch (db={name!r}, src={item['name']!r})")
    if reg != item["regularPriceInCents"]:
        mismatches.append(f"{item['sku']}: price mismatch (db={reg}, src={item['regularPriceInCents']})")
check("Spot-check: name and price match for first 5 items", not mismatches,
      "; ".join(mismatches))

# ── 4. Every product has at least one category ────────────────────────────────

cur.execute("""
    SELECT COUNT(*) FROM products p
    WHERE NOT EXISTS (SELECT 1 FROM product_categories pc WHERE pc.product_id = p.id);
""")
no_cat_count = cur.fetchone()[0]
check("Every product has at least one category", no_cat_count == 0,
      f"{no_cat_count} products with no category")

# ── 5. Variation count matches ────────────────────────────────────────────────

expected_vars = sum(len(i.get("variations", [])) for i in items)
cur.execute("SELECT COUNT(*) FROM variations;")
db_vars = cur.fetchone()[0]
check(f"Variation count matches ({db_vars} in DB, {expected_vars} expected)",
      db_vars == expected_vars)

cur.close()
conn.close()

print("=" * 60)
print("  IMPORT VERIFICATION")
print("=" * 60)
print()
for name in ok:
    print(f"  ✓ {name}")
if errors:
    print()
    for e in errors:
        print(f"  ✗ {e}")
else:
    print()
    print("  ALL CHECKS PASSED")

print()
print("  → Update docs/imported-items/verify.md with these results.")
