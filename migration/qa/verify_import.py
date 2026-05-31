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

source_by_sku = {i["sku"]: i for i in items}

# ── 1. Product count ──────────────────────────────────────────────────────────

cur.execute("SELECT COUNT(*) FROM products;")
db_count = cur.fetchone()[0]
check(f"Product count matches ({db_count} in DB, {len(items)} expected)",
      db_count == len(items))

# ── 2. All source SKUs present, no extras ─────────────────────────────────────

source_skus = set(source_by_sku.keys())
cur.execute("SELECT sku FROM products;")
db_skus = {r[0] for r in cur.fetchall()}

check("All source SKUs present in DB", not (source_skus - db_skus),
      f"{len(source_skus - db_skus)} missing: {list(source_skus - db_skus)[:3]}")
check("No extra SKUs in DB", not (db_skus - source_skus),
      f"{list(db_skus - source_skus)[:3]}")

# ── 3. Variation count ────────────────────────────────────────────────────────

expected_vars = sum(len(i.get("variations", [])) for i in items)
cur.execute("SELECT COUNT(*) FROM variations;")
db_vars = cur.fetchone()[0]
check(f"Variation count matches ({db_vars} in DB, {expected_vars} expected)",
      db_vars == expected_vars)

# ── 4. All variation SKUs present ────────────────────────────────────────────

source_var_skus = {ve["variation"]["sku"] for i in items for ve in i.get("variations", []) if ve.get("variation", {}).get("sku")}
cur.execute("SELECT sku FROM variations;")
db_var_skus = {r[0] for r in cur.fetchall()}
missing_vars = source_var_skus - db_var_skus
check("All variation SKUs present in DB", not missing_vars,
      f"{len(missing_vars)} missing: {list(missing_vars)[:3]}")

# ── 5. Key fields match across all products ───────────────────────────────────

cur.execute("SELECT sku, name, min_price_cents, max_price_cents, sale_price_cents, sale, in_stock, slug FROM products;")
field_mismatches = []
for sku, name, min_p, max_p, sale_cents, sale_flag, in_stock, slug in cur.fetchall():
    src = source_by_sku.get(sku)
    if not src:
        continue
    if name != src["name"]:
        field_mismatches.append(f"{sku}: name")
    if min_p != src["minPriceCents"]:
        field_mismatches.append(f"{sku}: min_price_cents")
    if max_p != src["maxPriceCents"]:
        field_mismatches.append(f"{sku}: max_price_cents")
    if sale_cents != src.get("salePriceCents"):
        field_mismatches.append(f"{sku}: sale_price_cents")
    if sale_flag != src.get("sale", False):
        field_mismatches.append(f"{sku}: sale")
    if in_stock != src.get("inStock", True):
        field_mismatches.append(f"{sku}: in_stock")
    if slug != src["slug"]:
        field_mismatches.append(f"{sku}: slug")
check("All product fields match source (name, price, sale, stock, slug)", not field_mismatches,
      f"{len(field_mismatches)} mismatches: {field_mismatches[:3]}")

# ── 6. Every product has at least one category ────────────────────────────────

cur.execute("""
    SELECT COUNT(*) FROM products p
    WHERE NOT EXISTS (SELECT 1 FROM product_categories pc WHERE pc.product_id = p.id);
""")
no_cat = cur.fetchone()[0]
check("Every product has at least one category", no_cat == 0,
      f"{no_cat} products with no category")

# ── 7. No duplicate slugs ────────────────────────────────────────────────────

cur.execute("SELECT slug, COUNT(*) FROM products GROUP BY slug HAVING COUNT(*) > 1;")
dup_slugs = cur.fetchall()
check("No duplicate product slugs", not dup_slugs,
      f"{[s for s, _ in dup_slugs[:3]]}")

# ── 8. Category leaf slugs match source paths ─────────────────────────────────

cur.execute("""
    SELECT p.sku, c.slug FROM products p
    JOIN product_categories pc ON pc.product_id = p.id
    JOIN categories c ON c.id = pc.category_id
    ORDER BY p.sku;
""")
db_cat_slugs = {}
for sku, slug in cur.fetchall():
    db_cat_slugs.setdefault(sku, set()).add(slug)

cat_mismatches = []
for item in items:
    sku = item["sku"]
    expected_leaves = {path[-1]["slug"] for path in item.get("categories", [])}
    actual = db_cat_slugs.get(sku, set())
    if expected_leaves != actual:
        cat_mismatches.append(f"{sku}: expected {expected_leaves}, got {actual}")
check("Category leaf slugs match source for all products", not cat_mismatches,
      f"{len(cat_mismatches)} mismatches: {cat_mismatches[:2]}")

cur.close()
conn.close()

# ── Report ────────────────────────────────────────────────────────────────────

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
print("  → Write a summary of these results in docs/imported-items/verify.md")
