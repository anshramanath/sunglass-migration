import json
import os
import sys
from pathlib import Path
import psycopg2

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand


brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]
data_dir = BASE / "data" / slug

items        = json.loads((data_dir / "categorize-items" / "items.json").read_text())
download_map = json.loads((data_dir / "download-items"   / "download_map.json").read_text())
upload_map   = json.loads((data_dir / "upload-items"     / "upload_map.json").read_text())

def resolvable(src):
    local = download_map.get(src)
    return bool(local and upload_map.get(local))

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur  = conn.cursor()

errors = []
ok     = []

def check(name, passed, detail=""):
    (ok if passed else errors).append(f"{name}{': ' + detail if detail else ''}")

source_by_sku = {p["sku"]: p for p in items}

# 1. Product count
cur.execute("SELECT COUNT(*) FROM products;")
db_count = cur.fetchone()[0]
check(f"Product count matches ({db_count} in DB, {len(items)} expected)", db_count == len(items))

# 2. All source SKUs present, no extras
source_skus = set(source_by_sku)
cur.execute("SELECT sku FROM products;")
db_skus = {r[0] for r in cur.fetchall()}
check("All source SKUs present in DB", not (source_skus - db_skus),
      f"{len(source_skus - db_skus)} missing: {list(source_skus - db_skus)[:3]}")
check("No extra SKUs in DB", not (db_skus - source_skus),
      f"{list(db_skus - source_skus)[:3]}")

# 3. Variation count
expected_vars = sum(len(p.get("variations", [])) for p in items)
cur.execute("SELECT COUNT(*) FROM variations;")
db_vars = cur.fetchone()[0]
check(f"Variation count matches ({db_vars} in DB, {expected_vars} expected)", db_vars == expected_vars)

# 4. All variation SKUs present
source_var_skus = {v["sku"] for p in items for v in p.get("variations", [])}
cur.execute("SELECT sku FROM variations;")
db_var_skus = {r[0] for r in cur.fetchall()}
missing_vars = source_var_skus - db_var_skus
check("All variation SKUs present in DB", not missing_vars,
      f"{len(missing_vars)} missing: {list(missing_vars)[:3]}")

# 5. Key product fields match source
cur.execute("SELECT sku, name, slug, min_price_cents, max_price_cents, sale_price_cents, sale, stock, featured, total_sales FROM products;")
field_mismatches = []
for sku, name, sl, min_p, max_p, sale_cents, sale_flag, stock, featured, total_sales in cur.fetchall():
    src = source_by_sku.get(sku)
    if not src:
        continue
    if name       != src["name"]:                           field_mismatches.append(f"{sku}: name")
    if sl         != src["slug"]:                           field_mismatches.append(f"{sku}: slug")
    if min_p      != src["minPriceCents"]:                  field_mismatches.append(f"{sku}: min_price_cents")
    if max_p      != src["maxPriceCents"]:                  field_mismatches.append(f"{sku}: max_price_cents")
    if sale_cents != src.get("salePriceCents"):             field_mismatches.append(f"{sku}: sale_price_cents")
    if sale_flag  != src.get("sale", False):                field_mismatches.append(f"{sku}: sale")
    if stock      != src.get("stock", 1):                   field_mismatches.append(f"{sku}: stock")
    if featured   != src.get("featured", False):            field_mismatches.append(f"{sku}: featured")
    if total_sales != src.get("totalSales", 0):             field_mismatches.append(f"{sku}: total_sales")
check("All product fields match source", not field_mismatches,
      f"{len(field_mismatches)} mismatches: {field_mismatches[:3]}")

# 6. Key variation fields match source
source_var_by_sku = {v["sku"]: v for p in items for v in p.get("variations", [])}
cur.execute("SELECT sku, regular_price_cents, sale_price_cents, sale, stock FROM variations;")
var_mismatches = []
for sku, reg_p, sale_cents, sale_flag, stock in cur.fetchall():
    src = source_var_by_sku.get(sku)
    if not src:
        continue
    if reg_p      != src["regularPriceCents"]:   var_mismatches.append(f"{sku}: regular_price_cents")
    if sale_cents != src.get("salePriceCents"):  var_mismatches.append(f"{sku}: sale_price_cents")
    if sale_flag  != src.get("sale", False):     var_mismatches.append(f"{sku}: sale")
    if stock      != src.get("stock", 1):        var_mismatches.append(f"{sku}: stock")
check("All variation fields match source", not var_mismatches,
      f"{len(var_mismatches)} mismatches: {var_mismatches[:3]}")

# 7. Every product has at least one category
cur.execute("""
    SELECT COUNT(*) FROM products p
    WHERE NOT EXISTS (SELECT 1 FROM product_categories pc WHERE pc.product_id = p.id);
""")
check("Every product has at least one category", cur.fetchone()[0] == 0,
      f"{cur.fetchone()[0] if False else ''}")

# 8. Category leaf slugs match source
cur.execute("""
    SELECT p.sku, c.slug FROM products p
    JOIN product_categories pc ON pc.product_id = p.id
    JOIN categories c ON c.id = pc.category_id
    ORDER BY p.sku;
""")
db_cat_slugs = {}
for sku, cat_slug in cur.fetchall():
    db_cat_slugs.setdefault(sku, set()).add(cat_slug)

cat_mismatches = []
for p in items:
    expected_leaves = {path[-1]["slug"] for path in p.get("categories", [])}
    actual = db_cat_slugs.get(p["sku"], set())
    if expected_leaves != actual:
        cat_mismatches.append(f"{p['sku']}: expected {expected_leaves}, got {actual}")
check("Category leaf slugs match source for all products", not cat_mismatches,
      f"{len(cat_mismatches)} mismatches: {cat_mismatches[:2]}")

# 9. Product image count matches resolvable source images
expected_prod_imgs = sum(
    sum(1 for img in p.get("images", []) if resolvable(img["src"]))
    for p in items
)
cur.execute("SELECT COUNT(*) FROM product_images;")
db_prod_imgs = cur.fetchone()[0]
check(f"Product image count matches ({db_prod_imgs} in DB, {expected_prod_imgs} resolvable in source)",
      db_prod_imgs == expected_prod_imgs)

# 10. Variation image count matches resolvable source images
expected_var_imgs = sum(
    sum(1 for img in v.get("images", []) if resolvable(img["src"]))
    for p in items for v in p.get("variations", [])
)
cur.execute("SELECT COUNT(*) FROM variation_images;")
db_var_imgs = cur.fetchone()[0]
check(f"Variation image count matches ({db_var_imgs} in DB, {expected_var_imgs} resolvable in source)",
      db_var_imgs == expected_var_imgs)

# 11. No duplicate product slugs
cur.execute("SELECT slug, COUNT(*) FROM products GROUP BY slug HAVING COUNT(*) > 1;")
dup_slugs = cur.fetchall()
check("No duplicate product slugs", not dup_slugs,
      f"{[s for s, _ in dup_slugs[:3]]}")

cur.close()
conn.close()

print(f"verify_import — {brand_name}\n")
for name in ok:
    print(f"  ✓ {name}")
if errors:
    print()
    for e in errors:
        print(f"  ✗ {e}")
    print(f"\n  FAILED — {len(errors)} error(s)")
else:
    print(f"\n  PASSED — all checks clean")
