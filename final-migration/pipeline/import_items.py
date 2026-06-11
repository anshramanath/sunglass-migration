import json
import os
import sys
from pathlib import Path

import psycopg2
from psycopg2.extras import Json

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]
brand_slug = config["brand_slug"]

data_dir = BASE / "data" / slug

items        = json.loads((data_dir / "validate-items-final" / "items.json").read_text())
download_map = json.loads((data_dir / "download-items"       / "download_map.json").read_text())
upload_map   = json.loads((data_dir / "upload-items"         / "upload_map.json").read_text())


def resolve_src(src):
    local = download_map.get(src)
    if not local:
        return None
    return upload_map.get(local)


conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur  = conn.cursor()

print(f"Wiping existing data for brand '{brand_slug}'...")
cur.execute("DELETE FROM brands WHERE slug = %s;", (brand_slug,))
conn.commit()

print(f"Inserting brand: {brand_name}...")
cur.execute(
    "INSERT INTO brands (name, slug) VALUES (%s, %s) RETURNING id;",
    (brand_name, brand_slug),
)
brand_id = cur.fetchone()[0]
conn.commit()

# (parent_id, slug) → category uuid — built lazily as products are processed
category_id_map: dict[tuple, str] = {}
desc_image_id_map: dict[str, str] = {}  # src → description_images.id


def ensure_category(path):
    parent_id = None
    for node in path:
        key = (parent_id, node["slug"])
        if key not in category_id_map:
            cur.execute(
                "INSERT INTO categories (brand_id, parent_id, name, slug, sort_order) "
                "VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                (brand_id, parent_id, node["name"], node["slug"], node["sortOrder"]),
            )
            category_id_map[key] = cur.fetchone()[0]
        parent_id = category_id_map[key]
    return parent_id  # leaf id


unresolved_images = 0
print(f"Inserting {len(items)} products...")

for i, p in enumerate(items):
    cur.execute(
        """
        INSERT INTO products (
            brand_id, name, slug, sku,
            description, summary, attributes,
            featured, total_sales,
            sale, min_price_cents, max_price_cents, sale_price_cents,
            stock, in_stock
        ) VALUES (
            %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s,
            %s, %s, %s, %s,
            %s, %s
        ) RETURNING id;
        """,
        (
            brand_id,
            p["name"],
            p["slug"],
            p["sku"],
            p["description"],
            p["summary"],
            Json(p["attributes"]),
            p["featured"],
            p["totalSales"],
            p["sale"],
            p["minPriceCents"],
            p["maxPriceCents"],
            p["salePriceCents"],
            p["stock"],
            p["inStock"],
        ),
    )
    product_id = cur.fetchone()[0]

    for path in p["categories"]:
        leaf_id = ensure_category(path)
        cur.execute(
            "INSERT INTO product_categories (product_id, category_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (product_id, leaf_id),
        )

    for img in p["productImages"]:
        src = resolve_src(img["src"])
        if not src:
            print(f"  WARN unresolved productImage: {img['src']}")
            unresolved_images += 1
            continue
        cur.execute(
            "INSERT INTO product_images (product_id, src, name, sort_order) VALUES (%s, %s, %s, %s);",
            (product_id, src, img["name"], img["sortOrder"]),
        )

    for img in p["descriptionImages"]:
        src = resolve_src(img["src"])
        if not src:
            print(f"  WARN unresolved descriptionImage: {img['src']}")
            unresolved_images += 1
            continue
        if src not in desc_image_id_map:
            cur.execute(
                "INSERT INTO description_images (brand_id, src, name) VALUES (%s, %s, %s) "
                "ON CONFLICT (brand_id, src) DO UPDATE SET name = EXCLUDED.name RETURNING id;",
                (brand_id, src, img["name"]),
            )
            desc_image_id_map[src] = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO product_description_images (product_id, image_id) VALUES (%s, %s);",
            (product_id, desc_image_id_map[src]),
        )

    for v in p["variations"]:
        cur.execute(
            """
            INSERT INTO variations (
                product_id, sku, attribute,
                sale, regular_price_cents, sale_price_cents,
                stock, total_sales
            ) VALUES (
                %s, %s, %s,
                %s, %s, %s,
                %s, %s
            ) RETURNING id;
            """,
            (
                product_id,
                v["sku"],
                Json(v["attribute"]),
                v["sale"],
                v["regularPriceCents"],
                v["salePriceCents"],
                v["stock"],
                v["totalSales"],
            ),
        )
        variation_id = cur.fetchone()[0]

        for img in v["variationImages"]:
            src = resolve_src(img["src"])
            if not src:
                print(f"  WARN unresolved variationImage: {img['src']}")
                unresolved_images += 1
                continue
            cur.execute(
                "INSERT INTO variation_images (variation_id, src, name, sort_order) VALUES (%s, %s, %s, %s);",
                (variation_id, src, img["name"], img["sortOrder"]),
            )

    if (i + 1) % 50 == 0:
        conn.commit()
        print(f"  {i + 1}/{len(items)} committed...")

conn.commit()
cur.close()
conn.close()

print(f"\nDone. {len(items)} products imported.")
if unresolved_images:
    print(f"  {unresolved_images} images skipped (failed to download — check download-items/flagged.json)")
