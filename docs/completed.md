# Migration Audit — Full Pipeline
_Last updated: 2026-05-30_

Overall health check across all 7 pipeline steps. See linked docs for step-level detail.

---

## Pipeline Status

| Step | Script | Status | Detail |
|------|--------|--------|--------|
| 1 — Fetch products | `fetch_products.py` | ✅ | 647 products |
| 2 — Fetch variations | `fetch_variations.py` | ✅ | 6,064 variations across 486 parents |
| 3 — Reshape | `reshape_items.py` | ✅ | 586 clean, 61 flagged |
| 4 — Recategorize | `recategorize_items.py` | ✅ | 581 ready, 5 held for review |
| 5 — Download images | `download_images.py` | ✅ | 2,531 downloaded, 30 permanent 404s |
| 6 — Upload images | `upload_images.py` | ✅ | 2,531 uploaded, 0 broken |
| 7 — Import | `import_items.py` | ✅ | 581 products in DB, all checks passed |

---

## Numbers at a Glance

| Metric | Count |
|--------|------:|
| Raw WooCommerce products | 647 |
| Shaped (clean) | 586 |
| Categorized (ready for import) | 581 |
| Flagged for owner review | 66 |
| Unique image URLs | 2,561 |
| Images downloaded | 2,531 |
| Images uploaded to Supabase | 2,531 |
| Permanent 404s (not recoverable) | 30 |
| Products in DB | 581 |
| Variations in DB | 5,649 |
| Categories in DB | 54 |
| Product images in DB | 2,618 |
| Description images in DB | 935 |

---

## Step 3 — Reshape

**Source:** `items/products.json` + `items/variations/variations.json`
**QA:** [audit](shaped-items/audit.md) · [verify](shaped-items/verify.md)

| Bucket | Count | Status |
|--------|------:|--------|
| `shaped_items.json` | 586 | ✅ Passed all checks |
| `invalid_sku_items.json` | 22 | ⚠️ Owner review |
| `no_weight_items.json` | 14 | ⚠️ Owner review |
| `zero_price_items.json` | 8 | ⚠️ Owner review |
| `missing_attributes_items.json` | 7 | ⚠️ Owner review |
| `duplicate_name_items.json` | 6 | ⚠️ Owner review |
| `no_image_items.json` | 3 | ⚠️ Owner review |
| `multiple_variation_images_items.json` | 1 | ⚠️ Owner review |

Zero critical issues in the shaped bucket. All 647 products accounted for across buckets.

---

## Step 4 — Recategorize

**Source:** `reshaped/shaped_items.json`
**QA:** [audit](step4-recategorize/audit.md) · [verify](step4-recategorize/verify.md)

| Bucket | Count | Status |
|--------|------:|--------|
| `categorized_items.json` | 581 | ✅ All paths end at leaf nodes |
| `no_category_items.json` | 2 | ⚠️ Owner review |
| `single_leaf_items.json` | 3 | ⚠️ Owner review |

8 category trees, max depth 3, products only at leaves. All 586 shaped items accounted for.

---

## Step 5 — Download Images

**Source:** `recategorized/categorized_items.json`
**QA:** [audit](downloaded-images/audit.md) · [verify](downloaded-images/verify.md)

| Type | Downloaded | Failed | Total |
|------|----------:|-------:|------:|
| Product images | 1,450 | 0 | 1,450 |
| Variation images | 1,315 | 24 | 1,339 |
| Description images | 33 | 6 | 39 |
| Variation description images | 1 | 0 | 1 |

All 30 failures are confirmed HTTP 404 — permanently deleted from server (mostly 2018 era). No product is left imageless. 86 variations have no downloadable image; frontend falls back to parent product.

---

## Step 6 — Upload Images

**Source:** `images/local/` → Supabase `bikershades` bucket
**QA:** [audit](uploaded-images/audit.md) · [verify](uploaded-images/verify.md)

| Metric | Count |
|--------|------:|
| Uploaded | 2,531 |
| Broken chain | 0 |
| Bad URLs | 0 |

Full resolution chain intact: `bikershades URL → url_map → local path → upload_map → Supabase URL` resolves for all 2,531 images.

---

## Step 7 — Import

**Source:** `recategorized/categorized_items.json` + both image maps
**QA:** [audit](imported-items/audit.md) · [verify](imported-items/verify.md)

| Check | Result |
|-------|--------|
| Product count matches source | ✅ 581 / 581 |
| Variation count matches source | ✅ 5,649 / 5,649 |
| All SKUs present in DB | ✅ 0 missing |
| All field values match source | ✅ 0 mismatches |
| Every product has at least one category | ✅ |
| Category leaf slugs match source paths | ✅ 0 mismatches |
| No duplicate slugs or SKUs | ✅ |

---

## Outstanding

| Item | Count | Next step |
|------|------:|-----------|
| Flagged reshape buckets | 61 | Share `reshaped-problems/treatment.md` with owner |
| No-category items | 2 | Owner decides — drop or recategorize |
| Single-leaf items | 3 | Owner decides — drop or merge into parent |
| **Total pending owner review** | **66** | |
