import json
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent.parent  # migration/

with open(BASE / "reshaped/shaped_items.json") as f:
    products = json.load(f)

total = len(products)
total_variations = sum(len(p.get("variations", [])) for p in products)

# ── helpers ──────────────────────────────────────────────────────────────────

def is_blank(v):
    if v is None: return True
    if isinstance(v, str) and not v.strip(): return True
    if isinstance(v, list) and len(v) == 0: return True
    return False

issues = defaultdict(list)  # field → list of (sku, detail)

def flag(field, sku, detail=""):
    issues[field].append((sku, detail))

# ── product-level audit ───────────────────────────────────────────────────────

for p in products:
    sku = p.get("sku", "UNKNOWN")

    # Required non-blank strings
    for field in ["name", "slug", "sku", "wpUrl", "productUrl"]:
        if is_blank(p.get(field)):
            flag(f"product.{field}", sku)

    # Price integrity
    is_variable = bool(p.get("variations"))
    min_p = p.get("minPriceCents", 0)
    max_p = p.get("maxPriceCents", 0)
    sale_p = p.get("salePriceCents")
    if not min_p or min_p <= 0:
        flag("product.minPriceCents", sku, f"value={min_p}")
    if max_p < min_p:
        flag("product.maxPriceCents", sku, f"max={max_p} < min={min_p}")
    if not is_variable and p.get("sale") and (not sale_p or sale_p <= 0 or sale_p >= min_p):
        flag("product.salePriceCents[sale=true]", sku, f"sale={sale_p} min={min_p}")

    # Stock value must be 0 or 1
    if p.get("stock") not in (0, 1):
        flag("product.stock", sku, f"value={p.get('stock')}")

    # Optional but tracked
    if is_blank(p.get("description")):
        flag("product.description[empty]", sku)
    if is_blank(p.get("summary")):
        flag("product.summary[empty]", sku)
    if is_blank(p.get("categories")):
        flag("product.categories[empty]", sku)
    if is_blank(p.get("descriptionImgs")):
        flag("product.descriptionImgs[empty]", sku)

    # Weight (should be set — this is the clean bucket)
    if p.get("weight") is None:
        flag("product.weight[null]", sku)
    elif p.get("weight") <= 0:
        flag("product.weight[zero]", sku, f"value={p.get('weight')}")

    # Dimensions
    dims = p.get("dimensions") or {}
    for axis in ["length", "width", "height"]:
        if dims.get(axis) is None:
            flag(f"product.dimensions.{axis}[null]", sku)

    # Images
    if is_blank(p.get("images")):
        flag("product.images[empty]", sku)
    else:
        for img in p.get("images", []):
            if is_blank(img.get("src")):
                flag("product.images[].src[blank]", sku)
            if is_blank(img.get("name")):
                flag("product.images[].name[blank]", sku)

    # Attributes
    if is_blank(p.get("attributes")):
        flag("product.attributes[empty]", sku)
    else:
        for attr in p.get("attributes", []):
            if is_blank(attr.get("name")):
                flag("product.attributes[].name[blank]", sku)
            if is_blank(attr.get("terms")):
                flag("product.attributes[].terms[empty]", sku)

    # ── variation-level audit ─────────────────────────────────────────────────

    for ve in p.get("variations", []):
        v = ve.get("variation", {})
        vsku = v.get("sku") or f"{sku}[no-vsku]"

        if is_blank(ve.get("attribute")):
            flag("variation.attribute[empty]", vsku, f"parent={sku}")

        for field in ["slug", "sku", "wpUrl", "productUrl"]:
            if is_blank(v.get(field)):
                flag(f"variation.{field}", vsku, f"parent={sku}")

        if v.get("stock") not in (0, 1):
            flag("variation.stock", vsku, f"value={v.get('stock')} parent={sku}")

        vreg = v.get("regularPriceCents", 0)
        vsale = v.get("salePriceCents", 0)
        if not vreg or vreg <= 0:
            flag("variation.regularPriceCents", vsku, f"value={vreg} parent={sku}")
        if v.get("sale") and (vsale <= 0 or vsale >= vreg):
            flag("variation.salePriceCents[sale=true]", vsku, f"sale={vsale} reg={vreg} parent={sku}")

        if v.get("weight") is None:
            flag("variation.weight[null]", vsku, f"parent={sku}")

        vdims = v.get("dimensions") or {}
        for axis in ["length", "width", "height"]:
            if vdims.get(axis) is None:
                flag(f"variation.dimensions.{axis}[null]", vsku, f"parent={sku}")

        if is_blank(v.get("images")):
            flag("variation.images[empty]", vsku, f"parent={sku}")

        if is_blank(v.get("description")):
            flag("variation.description[empty]", vsku, f"parent={sku}")

        if "descriptionImgs" in v:
            flag("variation.descriptionImgs[should_not_exist]", vsku, f"parent={sku}")

# ── report ────────────────────────────────────────────────────────────────────

print(f"{'='*60}")
print(f"  CLEAN PRODUCTS AUDIT")
print(f"{'='*60}")
print(f"  Products:   {total}")
print(f"  Variations: {total_variations}")
print()

# Separate critical (required fields) from informational (optional/empty)
critical_keywords = [
    "product.name", "product.slug", "product.sku", "product.wpUrl", "product.productUrl",
    "product.minPriceCents", "product.maxPriceCents", "product.salePriceCents[sale=true]",
    "product.weight[null]", "product.weight[zero]",
    "variation.slug", "variation.sku", "variation.wpUrl", "variation.productUrl",
    "variation.regularPriceCents", "variation.salePriceCents[sale=true]",
    "variation.attribute[empty]",
]

critical = {k: v for k, v in issues.items() if any(k.startswith(c) for c in critical_keywords)}
informational = {k: v for k, v in issues.items() if k not in critical}

print("── CRITICAL ISSUES (required fields missing or invalid) ──")
if not critical:
    print("  ✓ None")
else:
    for field, entries in sorted(critical.items()):
        pct = len(entries) / (total_variations if "variation." in field else total) * 100
        print(f"\n  {field}")
        print(f"  {len(entries)} affected ({pct:.1f}%)")
        for sku, detail in entries[:5]:
            print(f"    · {sku}" + (f"  {detail}" if detail else ""))
        if len(entries) > 5:
            print(f"    ... and {len(entries) - 5} more")

print()
print("── INFORMATIONAL (empty optional fields) ──")
for field, entries in sorted(informational.items()):
    base = total_variations if "variation." in field else total
    pct = len(entries) / base * 100
    print(f"  {field:<50}  {len(entries):>5} / {base}  ({pct:.1f}%)")

print()
print("── SUMMARY TABLE ──")
print(f"  {'Field':<50}  {'Missing':>7}  {'/ Total':>8}  {'%':>6}")
print(f"  {'-'*50}  {'-'*7}  {'-'*8}  {'-'*6}")
all_issues = {**critical, **informational}
for field, entries in sorted(all_issues.items()):
    base = total_variations if "variation." in field else total
    pct = len(entries) / base * 100
    marker = " !" if field in critical else "  "
    print(f"{marker} {field:<50}  {len(entries):>7}  / {base:<6}  {pct:>5.1f}%")

print()
print("  ! = critical field")

print()
print("── ATTRIBUTE STATS ──")
from collections import Counter
attr_product_counts = Counter()
attr_term_counts = {}
for p in products:
    for attr in p.get("attributes", []):
        name = attr["name"]
        attr_product_counts[name] += 1
        if name not in attr_term_counts:
            attr_term_counts[name] = set()
        for t in attr.get("terms", []):
            attr_term_counts[name].add(t["slug"])
for name, count in attr_product_counts.most_common():
    print(f"  {name:<30}  {count:>4} products  {len(attr_term_counts[name]):>4} unique terms")

print()
print("── CATEGORY LINK COUNTS (pre-recategorize) ──")
cat_counts = Counter()
for p in products:
    for cat in p.get("categories", []):
        slug = cat.rstrip("/").split("product-category/")[-1]
        cat_counts[slug] += 1
print(f"  Unique links: {len(cat_counts)} | Total assignments: {sum(cat_counts.values())} | Items with no categories: {sum(1 for p in products if not p.get('categories'))}")
for slug, count in cat_counts.most_common():
    print(f"  {count:>4}  {slug}")

print()
print("  → Write a summary of these results in docs/shaped-items/audit.md")
print("  → Update docs/shaped-items/attributes.md with attribute stats above")
print("  → Update docs/shaped-items/categories.md with category link counts above")
