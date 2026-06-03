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

items = json.loads((data_dir / "categorize-items" / "items.json").read_text())

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur  = conn.cursor()

def count(table):
    cur.execute(f"SELECT COUNT(*) FROM {table};")
    return cur.fetchone()[0]

expected_products   = len(items)
expected_variations = sum(len(p.get("variations", [])) for p in items)

db_products   = count("products")
db_variations = count("variations")
db_categories = count("categories")
db_prod_cats  = count("product_categories")
db_prod_imgs  = count("product_images")
db_var_imgs   = count("variation_images")
db_desc_imgs  = count("description_images")

# Products with no images
cur.execute("""
    SELECT p.sku FROM products p
    WHERE NOT EXISTS (SELECT 1 FROM product_images pi WHERE pi.product_id = p.id)
    ORDER BY p.sku;
""")
no_images = [r[0] for r in cur.fetchall()]

# Products with no categories
cur.execute("""
    SELECT p.sku FROM products p
    WHERE NOT EXISTS (SELECT 1 FROM product_categories pc WHERE pc.product_id = p.id)
    ORDER BY p.sku;
""")
no_cats = [r[0] for r in cur.fetchall()]

# Duplicate SKUs
cur.execute("SELECT sku, COUNT(*) FROM products GROUP BY sku HAVING COUNT(*) > 1;")
dup_prod_skus = cur.fetchall()
cur.execute("SELECT sku, COUNT(*) FROM variations GROUP BY sku HAVING COUNT(*) > 1;")
dup_var_skus = cur.fetchall()

# Variations with no image
cur.execute("""
    SELECT COUNT(*) FROM variations v
    WHERE NOT EXISTS (SELECT 1 FROM variation_images vi WHERE vi.variation_id = v.id);
""")
vars_no_img = cur.fetchone()[0]

# Category tree depth distribution
cur.execute("""
    WITH RECURSIVE depth AS (
        SELECT id, 1 AS d FROM categories WHERE parent_id IS NULL
        UNION ALL
        SELECT c.id, d.d + 1 FROM categories c JOIN depth d ON c.parent_id = d.id
    )
    SELECT d, COUNT(*) FROM depth GROUP BY d ORDER BY d;
""")
depth_dist = cur.fetchall()

# Brands
cur.execute("SELECT name, slug FROM brands ORDER BY name;")
brands = cur.fetchall()

# Sort order range
cur.execute("SELECT MIN(sort_order), MAX(sort_order) FROM product_images;")
img_sort = cur.fetchone()

cur.close()
conn.close()

print(f"audit_import — {brand_name}")
print()
print("── ROW COUNTS ──")
print(f"  {'Table':<25} {'DB':>8}  {'Expected':>10}")
print(f"  {'-'*25}  {'-'*8}  {'-'*10}")
print(f"  {'products':<25} {db_products:>8}  {expected_products:>10}  {'✓' if db_products == expected_products else '✗'}")
print(f"  {'variations':<25} {db_variations:>8}  {expected_variations:>10}  {'✓' if db_variations == expected_variations else '✗'}")
print(f"  {'categories':<25} {db_categories:>8}")
print(f"  {'product_categories':<25} {db_prod_cats:>8}")
print(f"  {'product_images':<25} {db_prod_imgs:>8}")
print(f"  {'variation_images':<25} {db_var_imgs:>8}")
print(f"  {'description_images':<25} {db_desc_imgs:>8}")

print()
print("── BRANDS ──")
for name, s in brands:
    print(f"  {name} (slug={s})")

print()
print("── CATEGORY TREE DEPTH ──")
for depth, cnt in depth_dist:
    print(f"  depth {depth}: {cnt} categories")

print()
print("── DATA QUALITY ──")
print(f"  Products with no images:     {len(no_images)}")
print(f"  Products with no categories: {len(no_cats)}")
print(f"  Variations with no image:    {vars_no_img} (falls back to product images on frontend)")
print(f"  Duplicate product SKUs:      {len(dup_prod_skus)}")
print(f"  Duplicate variation SKUs:    {len(dup_var_skus)}")
print(f"  product_images sort_order:   min={img_sort[0]}, max={img_sort[1]}")

if no_images:
    print()
    print("── PRODUCTS WITH NO IMAGES ──")
    for sku in no_images[:10]:
        print(f"  {sku}")
    if len(no_images) > 10:
        print(f"  ... and {len(no_images) - 10} more")

if no_cats:
    print()
    print("── PRODUCTS WITH NO CATEGORIES ──")
    for sku in no_cats:
        print(f"  {sku}")
