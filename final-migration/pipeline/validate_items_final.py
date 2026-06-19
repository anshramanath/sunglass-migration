import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "remove-stock" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run remove_stock.py first. Not found: {in_path}")

items = json.loads(in_path.read_text())

out_dir = BASE / "data" / slug / "validate-items-final"
out_dir.mkdir(parents=True, exist_ok=True)


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)

def is_bool(x):
    return isinstance(x, bool)

SLUG_RE   = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
URL_RE    = re.compile(r'^https?://')
ENTITY_RE = re.compile(r'&[a-zA-Z]+;|&#\d+;')


def check_no_entities(value, label):
    if isinstance(value, str) and ENTITY_RE.search(value):
        return [f"{label}: contains unescaped HTML entity: {value!r}"]
    return []


def check_image(img, label):
    errs = []
    src = (img.get("src") or "").strip()
    if not src:
        errs.append(f"{label}: missing src")
    elif not URL_RE.match(src):
        errs.append(f"{label}: src must be http(s) URL, got {src!r}")
    if not (img.get("name") or "").strip():
        errs.append(f"{label}: missing name")
    so = img.get("sortOrder")
    if not is_int(so):
        errs.append(f"{label}: sortOrder must be int, got {type(so).__name__}")
    elif so <= 0:
        errs.append(f"{label}: sortOrder must be > 0, got {so}")
    return errs


def check_image_sort_unique(imgs, label):
    orders = [img["sortOrder"] for img in imgs if is_int(img.get("sortOrder"))]
    if len(orders) != len(set(orders)):
        return [f"{label}: duplicate sortOrder values {sorted(orders)}"]
    return []


def check_categories(cats):
    errs = []
    if not isinstance(cats, list) or not cats:
        errs.append("categories must be non-empty array")
        return errs
    seen_leaves = set()
    for pi, path in enumerate(cats):
        plabel = f"categories[{pi}]"
        if not isinstance(path, list) or not path:
            errs.append(f"{plabel}: must be non-empty array of nodes")
            continue
        for ni, node in enumerate(path):
            nlabel = f"{plabel}[{ni}]"
            if not isinstance(node, dict):
                errs.append(f"{nlabel}: must be object")
                continue
            if not (node.get("name") or "").strip():
                errs.append(f"{nlabel}: name is null or empty")
            nslug = (node.get("slug") or "").strip()
            if not nslug:
                errs.append(f"{nlabel}: slug is null or empty")
            level = node.get("level")
            if not is_int(level):
                errs.append(f"{nlabel}: level must be int")
            elif level != ni + 1:
                errs.append(f"{nlabel}: level must be {ni + 1}, got {level}")
            so = node.get("sortOrder")
            if not is_int(so):
                errs.append(f"{nlabel}: sortOrder must be int")
            elif so <= 0:
                errs.append(f"{nlabel}: sortOrder must be > 0")
        leaf_slug = (path[-1].get("slug") or "").strip() if path else ""
        if leaf_slug:
            if leaf_slug in seen_leaves:
                errs.append(f"duplicate leaf category slug: {leaf_slug!r}")
            seen_leaves.add(leaf_slug)
    return errs


# Pre-scan for duplicate slugs across all items
slug_counts: dict[str, int] = {}
for item in items:
    s = (item.get("slug") or "").strip()
    if s:
        slug_counts[s] = slug_counts.get(s, 0) + 1


clean   = []
flagged = []

for item in items:
    reasons = []
    is_variable = item.get("sku") is None
    is_simple   = not is_variable

    # --- HTML entities ---
    reasons.extend(check_no_entities(item.get("name"), "name"))
    for ai, attr in enumerate(item.get("attributes") or []):
        reasons.extend(check_no_entities(attr.get("name"), f"attributes[{ai}].name"))
        for oi, opt in enumerate(attr.get("options") or []):
            reasons.extend(check_no_entities(opt.get("option") if isinstance(opt, dict) else opt, f"attributes[{ai}].options[{oi}].name"))
    for vi, v in enumerate(item.get("variations") or []):
        for ai, a in enumerate(v.get("attribute") or []):
            reasons.extend(check_no_entities(a.get("option"), f"variations[{vi}].attribute[{ai}].option"))

    # --- name / slug ---
    if not (item.get("name") or "").strip():
        reasons.append("name is null or empty")

    item_slug = (item.get("slug") or "").strip()
    if not item_slug:
        reasons.append("slug is null or empty")
    else:
        if not SLUG_RE.match(item_slug):
            reasons.append(f"slug invalid format: {item_slug!r}")
        if slug_counts.get(item_slug, 0) > 1:
            reasons.append(f"slug {item_slug!r} is duplicated in the catalogue")

    # --- content fields ---
    if not (item.get("description") or "").strip():
        reasons.append("description is null or empty")

    summary = item.get("summary")
    if not isinstance(summary, list) or not summary:
        reasons.append("summary must be non-empty array")
    else:
        for i, bullet in enumerate(summary):
            if not (bullet or "").strip():
                reasons.append(f"summary[{i}]: must be non-empty string")

    # --- fixed fields ---
    if item.get("featured") is not False:
        reasons.append(f"featured must be false, got {item.get('featured')!r}")
    if item.get("sale") is not False:
        reasons.append(f"sale must be false, got {item.get('sale')!r}")
    if item.get("salePriceCents") is not None:
        reasons.append(f"salePriceCents must be null, got {item.get('salePriceCents')!r}")
    # --- prices ---
    min_p = item.get("minPriceCents")
    max_p = item.get("maxPriceCents")
    if not is_int(min_p):
        reasons.append(f"minPriceCents must be int, got {min_p!r}")
    elif min_p <= 0:
        reasons.append(f"minPriceCents must be > 0, got {min_p}")
    if not is_int(max_p):
        reasons.append(f"maxPriceCents must be int, got {max_p!r}")
    elif max_p <= 0:
        reasons.append(f"maxPriceCents must be > 0, got {max_p}")
    if is_int(min_p) and is_int(max_p) and min_p > max_p:
        reasons.append(f"minPriceCents ({min_p}) > maxPriceCents ({max_p})")

    # --- categories ---
    reasons.extend(check_categories(item.get("categories", [])))

    # --- images ---
    prod_imgs = item.get("productImages") or []
    prod_srcs: set[str] = set()
    if not prod_imgs:
        reasons.append("productImages must be non-empty")
    else:
        for i, img in enumerate(prod_imgs):
            reasons.extend(check_image(img, f"productImages[{i}]"))
        reasons.extend(check_image_sort_unique(prod_imgs, "productImages"))
        prod_srcs = {img["src"] for img in prod_imgs if img.get("src")}
        if len(prod_srcs) < len(prod_imgs):
            reasons.append("productImages contains duplicate srcs")

    desc_imgs = item.get("descriptionImages") or []
    for i, img in enumerate(desc_imgs):
        reasons.extend(check_image(img, f"descriptionImages[{i}]"))
    if desc_imgs:
        reasons.extend(check_image_sort_unique(desc_imgs, "descriptionImages"))

    # --- simple-specific ---
    if is_simple:
        if not (item.get("sku") or "").strip():
            reasons.append("simple product sku is null or empty")
        if item.get("variations"):
            reasons.append("simple product has non-empty variations array")
        if item.get("totalSales") != 0:
            reasons.append(f"simple product totalSales must be 0, got {item.get('totalSales')!r}")

    # --- variable-specific ---
    if is_variable:
        if item.get("totalSales") is not None:
            reasons.append(f"variable product totalSales must be null, got {item['totalSales']!r}")

        attrs = item.get("attributes") or []
        attr_names: list[str] = []
        attr_options: dict[str, list] = {}

        if not attrs:
            reasons.append("variable product attributes must be non-empty")
        else:
            for j, a in enumerate(attrs):
                aname = (a.get("name") or "").strip()
                if not aname:
                    reasons.append(f"attributes[{j}]: name is null or empty")
                else:
                    attr_names.append(aname)
                options = a.get("options") or []
                if not options:
                    reasons.append(f"attributes[{j}] '{aname}': options must be non-empty")
                else:
                    for k, opt in enumerate(options):
                        oname = opt.get("option") if isinstance(opt, dict) else opt
                        if not (oname or "").strip():
                            reasons.append(f"attributes[{j}] '{aname}' options[{k}]: option must be non-empty string")
                        if isinstance(opt, dict):
                            for field in ("option", "slug"):
                                if not isinstance(opt.get(field), str):
                                    reasons.append(f"attributes[{j}] '{aname}' options[{k}].{field} must be str, got {type(opt.get(field)).__name__}")
                            if "value" in opt and not isinstance(opt["value"], str):
                                reasons.append(f"attributes[{j}] '{aname}' options[{k}].value must be str, got {type(opt['value']).__name__}")
                        if not isinstance(aname, str):
                            reasons.append(f"attributes[{j}].name must be str, got {type(aname).__name__}")
                    attr_options[aname] = options

        variations = item.get("variations") or []
        if len(variations) < 2:
            reasons.append(f"variable product has fewer than 2 variations ({len(variations)})")

        var_combos: set[tuple] = set()
        var_prices: list[int] = []

        for v in variations:
            v_sku = (v.get("sku") or "").strip()
            vlabel = f"variation {v_sku!r}" if v_sku else "variation (no sku)"

            if not v_sku:
                reasons.append(f"{vlabel}: sku is null or empty")
            reg_p = v.get("regularPriceCents")
            if not is_int(reg_p):
                reasons.append(f"{vlabel}: regularPriceCents must be int, got {reg_p!r}")
            elif reg_p <= 0:
                reasons.append(f"{vlabel}: regularPriceCents must be > 0, got {reg_p}")
            else:
                var_prices.append(reg_p)
            if v.get("salePriceCents") is not None:
                reasons.append(f"{vlabel}: salePriceCents must be null, got {v.get('salePriceCents')!r}")
            if v.get("totalSales") != 0:
                reasons.append(f"{vlabel}: totalSales must be 0, got {v.get('totalSales')!r}")
            if v.get("sale") is not False:
                reasons.append(f"{vlabel}: sale must be false, got {v.get('sale')!r}")

            vattrs = v.get("attribute") or []
            if not vattrs:
                reasons.append(f"{vlabel}: attribute must be non-empty")
            else:
                combo_parts = []
                for j, a in enumerate(vattrs):
                    aname = (a.get("name") or "").strip()
                    aopt  = (a.get("option") or "").strip()
                    if not isinstance(a.get("name"), str):
                        reasons.append(f"{vlabel} attribute[{j}].name must be str, got {type(a.get('name')).__name__}")
                    if not isinstance(a.get("option"), str):
                        reasons.append(f"{vlabel} attribute[{j}].option must be str, got {type(a.get('option')).__name__}")
                    if not isinstance(a.get("slug"), str):
                        reasons.append(f"{vlabel} attribute[{j}].slug must be str, got {type(a.get('slug')).__name__}")
                    if "value" in a and not isinstance(a["value"], str):
                        reasons.append(f"{vlabel} attribute[{j}].value must be str, got {type(a['value']).__name__}")
                    if not aname:
                        reasons.append(f"{vlabel} attribute[{j}]: name is null or empty")
                    if not aopt:
                        reasons.append(f"{vlabel} attribute[{j}]: option is null or empty")
                    if aname and aname not in attr_options:
                        reasons.append(f"{vlabel}: attribute name {aname!r} not declared in product attributes")
                    elif aname and aopt:
                        var_obj = {k: v for k, v in a.items() if k != "name"}
                        if var_obj not in attr_options.get(aname, []):
                            reasons.append(f"{vlabel}: option {aopt!r} not in product attributes['{aname}']")
                    combo_parts.append(f"{aname}={aopt}")

                combo = tuple(sorted(combo_parts))
                if combo in var_combos:
                    reasons.append(f"{vlabel}: duplicate attribute combination")
                var_combos.add(combo)

            for i, img in enumerate(v.get("variationImages") or []):
                reasons.extend(check_image(img, f"{vlabel} variationImages[{i}]"))
                if img.get("src") in prod_srcs:
                    reasons.append(f"{vlabel} variationImages[{i}]: src duplicates a productImage")

        # variation prices must agree with product-level min/max
        if var_prices and is_int(min_p) and is_int(max_p):
            if min(var_prices) != min_p:
                reasons.append(
                    f"minPriceCents {min_p} does not match min variation price {min(var_prices)}"
                )
            if max(var_prices) != max_p:
                reasons.append(
                    f"maxPriceCents {max_p} does not match max variation price {max(var_prices)}"
                )

    if reasons:
        flagged.append({"reasons": reasons, "item": item})
    else:
        clean.append(item)

(out_dir / "items.json").write_text(json.dumps(clean,   indent=2, ensure_ascii=False))
(out_dir / "flagged.json").write_text(json.dumps(flagged, indent=2, ensure_ascii=False))

print(f"Clean: {len(clean)}  Flagged: {len(flagged)}")
for f in flagged:
    print(f"  {f['item'].get('name')}: {f['reasons']}")
