import json
import os
import sys
import psycopg2
from psycopg2.extras import Json
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)
from dotenv import load_dotenv

BASE = Path(__file__).parent.parent  # migration/
load_dotenv(dotenv_path=BASE.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

IMAGES_DIR = BASE / "images"

with open(IMAGES_DIR / "url_map.json") as f:
    url_map = json.load(f)

with open(IMAGES_DIR / "upload_map.json") as f:
    upload_map = json.load(f)

with open(BASE / "recategorized/categorized_items.json") as f:
    products = json.load(f)


def resolve_src(src):
    local_path = url_map.get(src)
    if not local_path:
        return None
    return upload_map.get(local_path)


conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Wipe all product data (cascades to all child tables)
print("Wiping existing data...")
cur.execute("TRUNCATE brands CASCADE;")
conn.commit()

# Brand
print("Inserting brand...")
cur.execute("INSERT INTO brands (name, slug) VALUES (%s, %s) RETURNING id;", ("BikerShades", "bikershades"))
brand_id = cur.fetchone()[0]
conn.commit()

# Category tree: (parent_id, slug) → uuid
# Built lazily as products are processed
category_id_map = {}

def ensure_category(path):
    """Walk a root-to-leaf path, insert any missing nodes, return leaf id."""
    parent_id = None
    for node in path:
        key = (parent_id, node["slug"])
        if key not in category_id_map:
            cur.execute(
                "INSERT INTO categories (brand_id, parent_id, name, slug) VALUES (%s, %s, %s, %s) RETURNING id;",
                (brand_id, parent_id, node["name"], node["slug"]),
            )
            category_id_map[key] = cur.fetchone()[0]
        parent_id = category_id_map[key]
    return parent_id

# Products
print(f"Inserting {len(products)} products...")

for i, product in enumerate(products):
    dims = product.get("dimensions") or {}

    cur.execute(
        """
        INSERT INTO products (
            brand_id, name, slug, sku, wp_url, product_url,
            description, summary, attributes,
            sale, min_price_cents, max_price_cents, sale_price_cents,
            stock, weight, weight_unit, length, width, height, dimension_unit
        ) VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s
        ) RETURNING id;
        """,
        (
            brand_id,
            product["name"],
            product["slug"],
            product["sku"],
            product.get("wpUrl"),
            product.get("productUrl"),
            product.get("description"),
            product.get("summary"),
            Json(product.get("attributes", [])),
            product.get("sale", False),
            product["minPriceCents"],
            product["maxPriceCents"],
            product.get("salePriceCents"),
            product.get("stock", 1),
            product.get("weight"),
            product.get("weightUnit"),
            dims.get("length"),
            dims.get("width"),
            dims.get("height"),
            product.get("dimensionUnit"),
        ),
    )
    product_id = cur.fetchone()[0]

    # product_categories — categories is [[{level, name, slug}]]
    for path in product.get("categories", []):
        leaf_id = ensure_category(path)
        cur.execute(
            "INSERT INTO product_categories (product_id, category_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (product_id, leaf_id),
        )

    # product_images
    for j, img in enumerate(product.get("images", [])):
        src = resolve_src(img["src"])
        if src:
            cur.execute(
                "INSERT INTO product_images (product_id, src, name, sort_order) VALUES (%s, %s, %s, %s);",
                (product_id, src, img.get("name", ""), j),
            )

    # description_images (product-level)
    for j, img_url in enumerate(product.get("descriptionImgs", [])):
        src = resolve_src(img_url)
        if src:
            cur.execute(
                "INSERT INTO description_images (product_id, src, name, sort_order) VALUES (%s, %s, %s, %s);",
                (product_id, src, Path(img_url).name, j),
            )

    # variations
    for var_entry in product.get("variations", []):
        var = var_entry.get("variation", {})
        var_dims = var.get("dimensions") or {}

        cur.execute(
            """
            INSERT INTO variations (
                product_id, slug, sku, attribute,
                wp_url, product_url, description,
                sale, regular_price_cents, sale_price_cents,
                stock, weight, weight_unit,
                length, width, height, dimension_unit
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s
            ) RETURNING id;
            """,
            (
                product_id,
                var.get("slug"),
                var.get("sku"),
                var_entry.get("attribute", []),
                var.get("wpUrl"),
                var.get("productUrl"),
                var.get("description"),
                var.get("sale", False),
                var.get("regularPriceCents", 0),
                var.get("salePriceCents", 0),
                var.get("stock", 1),
                var.get("weight"),
                var.get("weightUnit"),
                var_dims.get("length"),
                var_dims.get("width"),
                var_dims.get("height"),
                var.get("dimensionUnit"),
            ),
        )
        variation_id = cur.fetchone()[0]

        # variation_images
        for j, img in enumerate(var.get("images", [])):
            src = resolve_src(img["src"])
            if src:
                cur.execute(
                    "INSERT INTO variation_images (variation_id, src, name, sort_order) VALUES (%s, %s, %s, %s);",
                    (variation_id, src, img.get("name", ""), j),
                )


    if (i + 1) % 50 == 0:
        conn.commit()
        print(f"  {i + 1}/{len(products)} committed...")

conn.commit()
cur.close()
conn.close()

print(f"\nDone. {len(products)} products imported into Supabase.")
print()
print("  → Run QA: python migration/qa/audit_import.py")
print("  → Run QA: python migration/qa/verify_import.py")
