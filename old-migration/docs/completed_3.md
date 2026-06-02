# Migration Audit — Full Pipeline (Run 3)
_Last updated: 2026-06-01_

Third full run after post-run-2 schema overhaul: `variation_images` table, global SKU uniqueness, `duplicate_sku` bucket, nullable sale prices, weight/dimension cleanup, `multiple_variation_images` bucket removed. See `completed_2.md` for previous run.

---

## Pipeline Status

| Step | Script | Status | Detail |
|------|--------|--------|--------|
| 1 — Fetch products | `fetch_products.py` | ✅ | 647 products (unchanged) |
| 2 — Fetch variations | `fetch_variations.py` | ✅ | 6,064 variations (unchanged) |
| 3 — Reshape | `reshape_items.py` | ✅ | 577 clean, 70 flagged |
| 4 — Recategorize | `recategorize_items.py` | ✅ | 573 ready, 4 held for review |
| 5 — Download images | `download_images.py` | ✅ | 2,465 downloaded, 11 permanent 404s |
| 6 — Upload images | `upload_images.py` | ✅ | 2,465 uploaded, 0 broken chain |
| 7 — Import | `import_items.py` | ✅ | 573 products in DB, all checks passed |

---

## Numbers at a Glance

| Metric | Count |
|--------|------:|
| Raw WooCommerce products | 647 |
| Shaped (clean) | 577 |
| Categorized (ready for import) | 573 |
| Flagged for owner review | 70 |
| Unique image URLs | 2,476 |
| Images downloaded | 2,465 |
| Images uploaded to Supabase | 2,465 |
| Permanent 404s (not recoverable) | 11 |
| Products in DB | 573 |
| Variations in DB | 5,296 |
| Categories in DB | 56 |
| Product images in DB | 2,530 |
| Variation images in DB | 1,899 |
| Description images in DB | 912 |

---

## Step 3 — Reshape

**Source:** `items/products.json` + `items/variations.json`
**QA:** [audit](shaped-items/audit.md) · [verify](shaped-items/verify.md)

| Bucket | Count | Status |
|--------|------:|--------|
| `shaped_items.json` | 577 | ✅ Passed all checks |
| `mismatched_attr_items.json` | 22 | ⚠️ Owner review |
| `invalid_sku_items.json` | 21 | ⚠️ Owner review |
| `duplicate_name_items.json` | 6 | ⚠️ Owner review |
| `duplicate_sku_items.json` | 5 | ⚠️ Owner review |
| `missing_attributes_items.json` | 5 | ⚠️ Owner review |
| `no_image_items.json` | 3 | ⚠️ Owner review |
| `zero_price_items.json` | 8 | ⚠️ Owner review |

All 647 products accounted for across buckets. Global SKU uniqueness verified on shaped bucket (product + variation SKUs pooled).

---

## Step 4 — Recategorize

**Source:** `reshaped/shaped_items.json`
**QA:** [audit](categorized-items/audit.md) · [verify](categorized-items/verify.md)

| Bucket | Count | Status |
|--------|------:|--------|
| `categorized_items.json` | 573 | ✅ All paths end at leaf nodes |
| `no_category_items.json` | 2 | ⚠️ Owner review |
| `single_leaf_items.json` | 2 | ⚠️ Owner review |

8 category trees, max depth 3, products only at leaves. All 577 shaped items accounted for.

---

## Step 5 — Download Images

**Source:** `recategorized/categorized_items.json`
**QA:** [audit](downloaded-images/audit.md) · [verify](downloaded-images/verify.md)

| Type | Downloaded | Failed | Total |
|------|----------:|-------:|------:|
| Product images | 1,421 | 0 | 1,421 |
| Variation images | 1,025 | 5 | 1,030 |
| Description images | 35 | 6 | 41 |

All 11 failures are confirmed HTTP 404 — permanently deleted from server. No product is left imageless. 10 variations have no downloadable image; frontend falls back to parent product.

---

## Step 6 — Upload Images

**Source:** `images/local/` → Supabase `bikershades` bucket
**QA:** [audit](uploaded-images/audit.md) · [verify](uploaded-images/verify.md)

| Metric | Count |
|--------|------:|
| Uploaded | 2,465 |
| Broken chain | 0 |
| Bad URLs | 0 |

Full resolution chain intact for all 2,465 images. One timeout on first run; re-run recovered cleanly.

---

## Step 7 — Import

**Source:** `recategorized/categorized_items.json` + both image maps
**QA:** [audit](imported-items/audit.md) · [verify](imported-items/verify.md)

| Check | Result |
|-------|--------|
| Product count matches source | ✅ 573 / 573 |
| Variation count matches source | ✅ 5,296 / 5,296 |
| All SKUs present in DB | ✅ 0 missing |
| All field values match source | ✅ 0 mismatches |
| Every product has at least one category | ✅ |
| Variation image count matches (resolvable) | ✅ 1,899 / 1,899 |
| Category leaf slugs match source paths | ✅ 0 mismatches |
| No duplicate slugs or SKUs | ✅ |

---

## Schema Changes vs Run 2

| Change | Detail |
|--------|--------|
| `variation_images` table | Replaces `image_src`/`image_name` columns on variations. `variation_id`, `src`, `name`, `sort_order`. Supports multiple images per variation. |
| `description_images` | Now product-only (`product_id not null`). Variation description images dropped — always duplicates of parent. |
| `variations.attribute` | `variation text[]` → `attribute text[] not null default '{}'` |
| Sale price nullable | `sale_price_cents` nullable on variations. Null = not on sale; value = on sale (always < `regular_price_cents`). |
| Weight/dimension nullable | `weight_unit`, `dimension_unit`, `sale_price_cents` on variations now nullable. Null weight/dims silently tolerated. |
| Global SKU uniqueness | New post-processing pass in reshape catches products where any SKU (product or variation) conflicts with any previously-seen SKU. New `duplicate_sku_items` bucket. |
| `multiple_variation_images` removed | Schema supports multiple variation images natively; restriction lifted. |

---

## Outstanding

| Item | Count | Next step |
|------|------:|-----------|
| `mismatched_attr_items.json` | 22 | Owner review — variation attribute slugs not in parent attribute terms |
| `invalid_sku_items.json` | 21 | Owner review — blank/malformed SKUs |
| `duplicate_name_items.json` | 6 | Owner review — identical product names |
| `duplicate_sku_items.json` | 5 | Owner review — global SKU collision |
| `missing_attributes_items.json` | 5 | Owner review — variations with empty attribute list |
| `no_image_items.json` | 3 | Owner review — no product images |
| `zero_price_items.json` | 8 | Owner review — internal/zero-price products |
| `no_category_items.json` | 2 | Owner decides — drop or recategorize |
| `single_leaf_items.json` | 2 | Owner decides — drop or merge into parent |
| **Total pending owner review** | **74** | |
