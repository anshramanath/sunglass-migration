import json
import sys
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(line_buffering=True)

BASE = Path(__file__).parent.parent  # migration/
(BASE / "recategorized").mkdir(exist_ok=True)

with open(BASE / "reshaped/shaped_items.json", encoding="utf-8") as f:
    items = json.load(f)

# ── Category name map ─────────────────────────────────────────────────────────
# WooCommerce leaf slug → (display name, new slug)

CATEGORY_MAP = {
    "accessories":                              ("Accessories",                   "accessories"),
    "cases":                                    ("Cases",                         "cases"),
    "extra-lenses":                             ("Extra Lenses",                  "extra-lenses"),
    "return-labels":                            ("Return Labels",                 "return-labels"),
    "strings":                                  ("Strings",                       "strings"),
    "tools":                                    ("Tools",                         "tools"),
    "bifocal-motorcycle-glasses":               ("Bifocals",                      "bifocals"),
    "bifocals-motorcycle-sport":                ("Sport Bifocals",                "sport-bifocals"),
    "full-lens-reader-bifocal-type":            ("Full Lens Reader",              "full-lens-reader"),
    "lined-bifocals-bifocal-type":              ("Lined Bifocals",                "lined-bifocals"),
    "multifocal-reader":                        ("Multifocal Reader",             "multifocal-reader"),
    "polarized-bifocals":                       ("Polarized Bifocals",            "polarized-bifocals"),
    "motorcycle-sunglasses":                    ("Sunglasses",                    "sunglasses"),
    "brands":                                   ("Brands",                        "brands"),
    "7eye":                                     ("7eye",                          "7eye"),
    "bikerarmour-motorcycle-riding-glasses":    ("BikerArmour",                   "bikerarmour"),
    "locs":                                     ("Locs",                          "locs"),
    "prosport-sunglasses":                      ("ProSport",                      "prosport"),
    "wiley-x-sunglasses":                       ("Wiley X",                       "wiley-x"),
    "xloop":                                    ("X-Loop",                        "x-loop"),
    "cover-overs":                              ("Cover Overs",                   "cover-overs"),
    "ladies-motorcycle-sunglasses":             ("Ladies",                        "ladies"),
    "lens-type":                                ("Lens Type",                     "lens-type"),
    "brown-lens-type":                          ("Brown",                         "brown"),
    "clear":                                    ("Clear",                         "clear"),
    "computer-blue-block-lenses":               ("Computer Blue Block",           "computer-blue-block"),
    "hd-copper":                                ("HD Copper",                     "hd-copper"),
    "mirror":                                   ("Mirror",                        "mirror"),
    "polarized":                                ("Polarized",                     "polarized"),
    "smoke-grey":                               ("Smoke Grey",                    "smoke-grey"),
    "yellow":                                   ("Yellow",                        "yellow"),
    "z87-safety":                               ("Z87 Safety",                    "z87-safety"),
    "motorcycle-goggles":                       ("Goggles",                       "goggles"),
    "shop-by-head-size":                        ("Head Size",                     "head-size"),
    "large-xlarge":                             ("Large - XLarge",                "large-xlarge"),
    "long-eyelashes":                           ("Low Nose Bridge Long Lashes",   "low-nose-bridge-long-lashes"),
    "medium-large":                             ("Medium - Large",                "medium-large"),
    "one-size-fits-all":                        ("One Size Fits All",             "one-size-fits-all"),
    "small-medium":                             ("Small - Medium",                "small-medium"),
    "xsmall-small":                             ("XSmall - Small",                "xsmall-small"),
    "prescription-motorcycle-glasses":          ("Prescription",                  "prescription"),
    "high-power-rx":                            ("High Power Rx",                 "high-power-rx"),
    "rx-brands":                                ("Rx Brands",                     "rx-brands"),
    "7eye-rx-prescription-motorcycle-sunglasses-frames": ("7Eye Rx Frames",       "7eye-rx-frames"),
    "bikerarmour-rx-frames":                    ("BikerArmour Rx Frames",         "bikerarmour-rx-frames"),
    "wileyx-rx-frames":                         ("WileyX Rx Frames",              "wileyx-rx-frames"),
    "ziena-dry-eye-glasses":                    ("Ziena Dry Eye",                 "ziena-dry-eye"),
    "sales":                                    ("Sale",                          "sale"),
    "see-all-combo-sets":                       ("Combo Sets",                    "combo-sets"),
    "try-before-you-buy":                       ("Try Before You Buy",            "try-before-you-buy"),
    "transitions-motorcycle-sunglasses":        ("Transitions",                   "transitions"),
    "eclipse-photochromics-motorcycle-sunglasses": ("Eclipse Photochromics",      "eclipse-photochromics"),
    "bikerarmour-eclipse-photochromic-sunglasses": ("BikerArmour Eclipse",        "bikerarmour-eclipse"),
    "transition-motorcycle-sunglasses-eclipse-xt": ("Eclipse XT",                "eclipse-xt"),
    "bikerarmour-eclipse-xt":                   ("BikerArmour Eclipse XT",        "bikerarmour-eclipse-xt"),
    "eclipse_xt_transition_motorcycle_sunglasses_7eye": ("7eye Eclipse XT",       "7eye-eclipse-xt"),
    "eclipse_xt_transition_motorcycle_sunglasses_wileyx": ("WileyX Eclipse XT",   "wileyx-eclipse-xt"),
}

BASE_URL = "https://bikershades.com/product-category"

DROP_SLUGS = {
    "see-all-brands", "see-all-rx-frames", "see-all-eclipse-xt-frames",
    "see-all-try-before-you-buy", "all-products", "got-frames",
}

MERGE_SLUGS = {
    "mirrored":                           "mirror",
    "small-medium-shop-by-head-size":     "small-medium",
    "low-nose-bridge-long-lashes-shades": "long-eyelashes",
    "bifocal-type":                       None,  # promote to parent
}


def parse_segments(link):
    path = link.rstrip("/").replace(BASE_URL, "").strip("/")
    return path.split("/") if path else []


def apply_drops_merges(link):
    segments = parse_segments(link)
    if not segments:
        return None
    leaf = segments[-1]
    if leaf in DROP_SLUGS:
        return None
    if leaf in MERGE_SLUGS:
        target = MERGE_SLUGS[leaf]
        if target is None:
            return (BASE_URL + "/" + "/".join(segments[:-1])) if len(segments) > 1 else None
        segments[-1] = target
    return BASE_URL + "/" + "/".join(segments)


def build_path(link):
    segments = parse_segments(link)
    path = []
    for i, seg in enumerate(segments):
        meta = CATEGORY_MAP.get(seg)
        if not meta:
            print(f"  WARNING: no map entry for slug '{seg}'")
            return None
        path.append({"level": i + 1, "name": meta[0], "slug": meta[1]})
    return path


def get_leaves(all_links):
    return {l for l in all_links if not any(
        other.startswith(l + "/") for other in all_links
    )}


# ── Pass 1: apply drops and merges ───────────────────────────────────────────

item_links = []
for item in items:
    surviving = set()
    for link in item.get("categories", []):
        result = apply_drops_merges(link.rstrip("/"))
        if result:
            surviving.add(result)
    item_links.append(surviving)

# ── Pass 2: iteratively remove single-item leaves ────────────────────────────

active = list(range(len(items)))  # indices of items still in play
single_leaf_indices = set()

changed = True
while changed:
    changed = False
    all_links = {link for i in active for link in item_links[i]}
    leaves = get_leaves(all_links)
    leaf_counts = Counter(link for i in active for link in item_links[i] if link in leaves)

    single_leaves = {l for l, c in leaf_counts.items() if c == 1}
    if not single_leaves:
        break

    new_active = []
    for i in active:
        if item_links[i] & single_leaves:
            single_leaf_indices.add(i)
            print(f"  SINGLE-LEAF: [{items[i]['sku']}] {items[i]['name']} — {[parse_segments(l) for l in item_links[i] & single_leaves]}")
            changed = True
        else:
            new_active.append(i)
    active = new_active

# ── Pass 3: strip non-leaf paths from remaining items ────────────────────────

all_links = {link for i in active for link in item_links[i]}
leaves = get_leaves(all_links)

stripped_count = 0
for i in active:
    before = len(item_links[i])
    item_links[i] = {l for l in item_links[i] if l in leaves}
    stripped_count += before - len(item_links[i])

if stripped_count:
    print(f"  STRIPPED: {stripped_count} non-leaf paths removed")

# ── Pass 4: build output ──────────────────────────────────────────────────────

categorized_out = []
no_category_out = []
single_leaf_out = [items[i] for i in single_leaf_indices]

for i in active:
    item = items[i]
    if not item_links[i]:
        no_category_out.append(item)
        continue
    paths = [build_path(l) for l in sorted(item_links[i])]
    paths = [p for p in paths if p]
    item["categories"] = paths
    categorized_out.append(item)

# ── Write output ──────────────────────────────────────────────────────────────

with open(BASE / "recategorized/categorized_items.json", "w", encoding="utf-8") as f:
    json.dump(categorized_out, f, indent=2, ensure_ascii=False)

with open(BASE / "recategorized/no_category_items.json", "w", encoding="utf-8") as f:
    json.dump(no_category_out, f, indent=2, ensure_ascii=False)

with open(BASE / "recategorized/single_leaf_items.json", "w", encoding="utf-8") as f:
    json.dump(single_leaf_out, f, indent=2, ensure_ascii=False)

print(f"\nDone.")
print(f"  Categorized items:   {len(categorized_out)}")
print(f"  No-category items:   {len(no_category_out)} → no_category_items.json")
print(f"  Single-leaf items:   {len(single_leaf_out)} → single_leaf_items.json")
print()
print("  → Run QA: python migration/qa/audit_categorized_items.py")
print("  → Run QA: python migration/qa/verify_categorized_items.py")
