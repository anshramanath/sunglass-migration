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
# Maps WooCommerce path slug → (name, new_slug)
# Key is the WooCommerce leaf slug, value is (display name, slug for new site)

CATEGORY_MAP = {
    # accessories
    "accessories":                              ("Accessories",                   "accessories"),
    "cases":                                    ("Cases",                         "cases"),
    "extra-lenses":                             ("Extra Lenses",                  "extra-lenses"),
    "return-labels":                            ("Return Labels",                 "return-labels"),
    "strings":                                  ("Strings",                       "strings"),
    "tools":                                    ("Tools",                         "tools"),
    # bifocals
    "bifocal-motorcycle-glasses":               ("Bifocals",                      "bifocals"),
    "bifocals-motorcycle-sport":                ("Sport Bifocals",                "sport-bifocals"),
    "full-lens-reader-bifocal-type":            ("Full Lens Reader",              "full-lens-reader"),
    "lined-bifocals-bifocal-type":              ("Lined Bifocals",                "lined-bifocals"),
    "multifocal-reader":                        ("Multifocal Reader",             "multifocal-reader"),
    "polarized-bifocals":                       ("Polarized Bifocals",            "polarized-bifocals"),
    # sunglasses
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
    "long-eyelashes":                           ("Low Nose Bridge / Long Lashes", "low-nose-bridge-long-lashes"),
    "medium-large":                             ("Medium - Large",                "medium-large"),
    "one-size-fits-all":                        ("One Size Fits All",             "one-size-fits-all"),
    "small-medium":                             ("Small - Medium",                "small-medium"),
    "xsmall-small":                             ("XSmall - Small",                "xsmall-small"),
    # prescription
    "prescription-motorcycle-glasses":          ("Prescription",                  "prescription"),
    "high-power-rx":                            ("High Power Rx",                 "high-power-rx"),
    "rx-brands":                                ("Rx Brands",                     "rx-brands"),
    "7eye-rx-prescription-motorcycle-sunglasses-frames": ("7Eye Rx Frames",       "7eye-rx-frames"),
    "bikerarmour-rx-frames":                    ("BikerArmour Rx Frames",         "bikerarmour-rx-frames"),
    "wileyx-rx-frames":                         ("WileyX Rx Frames",              "wileyx-rx-frames"),
    "ziena-dry-eye-glasses":                    ("Ziena Dry Eye",                 "ziena-dry-eye"),
    # other roots
    "sales":                                    ("Sale",                          "sale"),
    "see-all-combo-sets":                       ("Combo Sets",                    "combo-sets"),
    "try-before-you-buy":                       ("Try Before You Buy",            "try-before-you-buy"),
    # transitions
    "transitions-motorcycle-sunglasses":        ("Transitions",                   "transitions"),
    "eclipse-photochromics-motorcycle-sunglasses": ("Eclipse Photochromics",      "eclipse-photochromics"),
    "bikerarmour-eclipse-photochromic-sunglasses": ("BikerArmour Eclipse",        "bikerarmour-eclipse"),
    "transition-motorcycle-sunglasses-eclipse-xt": ("Eclipse XT",                "eclipse-xt"),
    "bikerarmour-eclipse-xt":                   ("BikerArmour Eclipse XT",        "bikerarmour-eclipse-xt"),
    "eclipse_xt_transition_motorcycle_sunglasses_7eye": ("7eye Eclipse XT",       "7eye-eclipse-xt"),
    "eclipse_xt_transition_motorcycle_sunglasses_wileyx": ("WileyX Eclipse XT",   "wileyx-eclipse-xt"),
}

# ── Recategorization rules ────────────────────────────────────────────────────

BASE_URL = "https://bikershades.com/product-category"

DROP_SLUGS = {
    "see-all-brands", "see-all-rx-frames", "see-all-eclipse-xt-frames",
    "see-all-try-before-you-buy", "all-products", "got-frames",
}

MERGE_SLUGS = {
    "mirrored":                              "mirror",
    "small-medium-shop-by-head-size":        "small-medium",
    "low-nose-bridge-long-lashes-shades":    "long-eyelashes",
    "bifocal-type":                          None,  # promote to parent
}


def parse_path_segments(link):
    """Extract slug segments from a WooCommerce category link."""
    path = link.rstrip("/").replace(BASE_URL, "").strip("/")
    return path.split("/") if path else []


def apply_drops_merges(link):
    """
    Returns the normalised link after applying drops and merges,
    or None if the link should be removed entirely.
    """
    segments = parse_path_segments(link)
    if not segments:
        return None

    leaf = segments[-1]

    if leaf in DROP_SLUGS:
        return None

    target = MERGE_SLUGS.get(leaf)
    if target is None and leaf in MERGE_SLUGS:
        # bifocal-type: promote to parent
        if len(segments) > 1:
            return BASE_URL + "/" + "/".join(segments[:-1])
        return None
    if target:
        segments[-1] = target
        return BASE_URL + "/" + "/".join(segments)

    return link


def build_path(link):
    """Build [{level, name, slug}, ...] for a surviving link."""
    segments = parse_path_segments(link)
    path = []
    for i, seg in enumerate(segments):
        meta = CATEGORY_MAP.get(seg)
        if not meta:
            print(f"  WARNING: no category map entry for slug '{seg}' in {link}")
            return None
        path.append({"level": i + 1, "name": meta[0], "slug": meta[1]})
    return path


# ── Pass 1: apply drops and merges, count per surviving link ──────────────────

# Map item index → set of surviving links
item_links = []
for item in items:
    surviving = set()
    for link in item.get("categories", []):
        result = apply_drops_merges(link.rstrip("/"))
        if result:
            surviving.add(result)
    item_links.append(surviving)

# ── Pass 2: iterative collapse of single-item leaves ─────────────────────────

def get_leaves(all_links_flat):
    paths_set = set(all_links_flat)
    return {p for p in paths_set if not any(
        other.startswith(p + "/") for other in paths_set
    )}

changed = True
while changed:
    changed = False
    link_counts = Counter(link for links in item_links for link in links)
    all_links_flat = set(link_counts.keys())
    leaves = get_leaves(all_links_flat)
    single_leaves = {l for l in leaves if link_counts[l] == 1}

    if not single_leaves:
        break

    for i, links in enumerate(item_links):
        new_links = set()
        for link in links:
            if link in single_leaves:
                segments = parse_path_segments(link)
                if len(segments) > 1:
                    parent = BASE_URL + "/" + "/".join(segments[:-1])
                    new_links.add(parent)
                    changed = True
                    print(f"  COLLAPSE: {link.replace(BASE_URL,'')} → {parent.replace(BASE_URL,'')}")
                else:
                    # root-level single leaf — keep it, can't collapse further
                    new_links.add(link)
            else:
                new_links.add(link)
        item_links[i] = new_links

# ── Pass 3: build final category paths and split output ──────────────────────

clean_out = []
no_category_out = []

for item, links in zip(items, item_links):
    if not links:
        no_category_out.append(item)
        continue

    category_paths = []
    for link in sorted(links):  # sorted for deterministic output
        path = build_path(link)
        if path:
            category_paths.append(path)

    item["categories"] = category_paths
    clean_out.append(item)

# ── Write output ──────────────────────────────────────────────────────────────

with open(BASE / "recategorized/categorized_items.json", "w", encoding="utf-8") as f:
    json.dump(clean_out, f, indent=2, ensure_ascii=False)

with open(BASE / "recategorized/no_category_items.json", "w", encoding="utf-8") as f:
    json.dump(no_category_out, f, indent=2, ensure_ascii=False)

print(f"\nDone.")
print(f"  Clean items:       {len(clean_out)}")
print(f"  No category items: {len(no_category_out)} → no_category_items.json")
