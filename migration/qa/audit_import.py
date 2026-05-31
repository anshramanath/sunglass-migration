import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

BASE = Path(__file__).parent.parent  # migration/
load_dotenv(dotenv_path=BASE.parent / ".env")

with open(BASE / "recategorized/categorized_items.json") as f:
    items = json.load(f)

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

def count(table):
    cur.execute(f"SELECT COUNT(*) FROM {table};")
    return cur.fetchone()[0]

db_products    = count("products")
db_variations  = count("variations")
db_categories  = count("categories")
db_prod_cats   = count("product_categories")
db_prod_imgs   = count("product_images")
db_desc_imgs   = count("description_images")

expected_products   = len(items)
expected_variations = sum(len(i.get("variations", [])) for i in items)

print("=" * 60)
print("  IMPORT AUDIT")
print("=" * 60)
print(f"  {'Table':<25} {'DB':>8}  {'Expected':>10}")
print(f"  {'-'*25}  {'-'*8}  {'-'*10}")
print(f"  {'products':<25} {db_products:>8}  {expected_products:>10}  {'✓' if db_products == expected_products else '✗'}")
print(f"  {'variations':<25} {db_variations:>8}  {expected_variations:>10}  {'✓' if db_variations == expected_variations else '✗'}")
print(f"  {'categories':<25} {db_categories:>8}")
print(f"  {'product_categories':<25} {db_prod_cats:>8}")
print(f"  {'product_images':<25} {db_prod_imgs:>8}")
print(f"  {'description_images':<25} {db_desc_imgs:>8}")

cur.close()
conn.close()

print()
print("  → Update docs/imported-items/audit.md with these results.")
