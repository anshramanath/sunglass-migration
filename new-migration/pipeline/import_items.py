import json
import os
import sys
import psycopg2
from psycopg2.extras import Json
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand


brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]

data_dir = BASE / "data" / slug

download_map = json.loads((data_dir / "download-items" / "download_map.json").read_text())
upload_map   = json.loads((data_dir / "upload-items"   / "upload_map.json").read_text())
items        = json.loads((data_dir / "categorize-items" / "items.json").read_text())

DATABASE_URL = os.getenv("DATABASE_URL")

def resolve_src(src):
    local_path = download_map.get(src)
    if not local_path:
        return None
    return upload_map.get(local_path)

conn = psycopg2.connect(DATABASE_URL)
cur  = conn.cursor()

print("Wiping existing data...")
cur.execute("TRUNCATE brands CASCADE;")
conn.commit()

print(f"Inserting brand: {brand_name}...")
cur.execute("INSERT INTO brands (name, slug) VALUES (%s, %s) RETURNING id;", (brand_name, slug))
brand_id = cur.fetchone()[0]
conn.commit()

# (parent_id, slug) → category uuid — built lazily as products are processed
category_id_map = {}

def ensure_category(path):
    parent_id = None
    for node in path:
        key = (parent_id, node["slug"])
        if key not in category_id_map:
            cur.execute(
                "INSERT INTO categories (brand_id, parent_id, name, slug, sort_order) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                (brand_id, parent_id, node["name"], node["slug"], node["sortOrder"]),
            )
            category_id_map[key] = cur.fetchone()[0]
        parent_id = category_id_map[key]
    return parent_id

print(f"Inserting {len(items)} products...")

for i, p in enumerate(items):
    dims = p.get("dimensions") or {}

    cur.execute(
        """
        INSERT INTO products (
            brand_id, name, slug, sku, old_url,
            description, summary, attributes,
            featured, total_sales,
            sale, min_price_cents, max_price_cents, sale_price_cents,
            stock, weight, weight_unit,
            length, width, height, dimension_unit
        ) VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s, %s
        ) RETURNING id;
        """,
        (
            brand_id,
            p["name"],
            p["slug"],
            p["sku"],
            p.get("oldUrl"),
            p.get("description"),
            p["summary"],
            Json(p.get("attributes", [])),
            p.get("featured", False),
            p["totalSales"],
            p["sale"],
            p["minPriceCents"],
            p["maxPriceCents"],
            p.get("salePriceCents"),
            p["stock"],
            p["weight"],
            p["weightUnit"],
            dims.get("length"),
            dims.get("width"),
            dims.get("height"),
            p["dimensionUnit"],
        ),
    )
    product_id = cur.fetchone()[0]

    # categories
    for path in p.get("categories", []):
        leaf_id = ensure_category(path)
        cur.execute(
            "INSERT INTO product_categories (product_id, category_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (product_id, leaf_id),
        )

    # product_images
    for img in p.get("images", []):
        src = resolve_src(img["src"])
        if src:
            cur.execute(
                "INSERT INTO product_images (product_id, src, name, sort_order) VALUES (%s, %s, %s, %s);",
                (product_id, src, img.get("name", ""), img["sortOrder"]),
            )

    # description_images
    for img in p.get("descriptionImages", []):
        src = resolve_src(img["src"])
        if src:
            cur.execute(
                "INSERT INTO description_images (product_id, src, name, sort_order) VALUES (%s, %s, %s, %s);",
                (product_id, src, img.get("name", ""), img["sortOrder"]),
            )

    # variations
    for v in p.get("variations", []):
        v_dims = v.get("dimensions") or {}

        cur.execute(
            """
            INSERT INTO variations (
                product_id, sku, old_url, description, attributes,
                sale, regular_price_cents, sale_price_cents,
                stock, weight, weight_unit,
                length, width, height, dimension_unit
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s
            ) RETURNING id;
            """,
            (
                product_id,
                v["sku"],
                v.get("oldUrl"),
                v.get("description"),
                Json(v.get("attributes", [])),
                v["sale"],
                v["regularPriceCents"],
                v.get("salePriceCents"),
                v["stock"],
                v["weight"],
                v["weightUnit"],
                v_dims.get("length"),
                v_dims.get("width"),
                v_dims.get("height"),
                v["dimensionUnit"],
            ),
        )
        variation_id = cur.fetchone()[0]

        # variation_images
        for img in v.get("images", []):
            src = resolve_src(img["src"])
            if src:
                cur.execute(
                    "INSERT INTO variation_images (variation_id, src, name, sort_order) VALUES (%s, %s, %s, %s);",
                    (variation_id, src, img.get("name", ""), img["sortOrder"]),
                )

    if (i + 1) % 50 == 0:
        conn.commit()
        print(f"  {i + 1}/{len(items)} committed...")

conn.commit()
cur.close()
conn.close()

print(f"\nDone. {len(items)} products imported.")
