import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
if brand_key != "prosport":
    raise SystemExit(f"This script is for prosport only (got BRAND={brand_key})")
slug = config["slug"]

in_path = BASE / "data" / slug / "clean-content" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run clean_content.py first. Not found: {in_path}")

# TREE: slug -> (name, sortOrder) for leaf nodes
#             -> (name, sortOrder, {children}) for non-leaf nodes
TREE = {
    "sunglasses": ("Sunglasses", 1, {
        "sport":      ("Sport",      1),
        "polarized":  ("Polarized",  2),
        "hd-lens":    ("HD Lens",    3),
        "night":      ("Night",      4),
        "mirror":     ("Mirror",     5),
        "aviator":    ("Aviator",    6),
        "fashion":    ("Fashion",    7),
    }),
    "bifocals": ("Bifocals", 2, {
        "standard":   ("Standard",   1),
        "polarized":  ("Polarized",  2),
        "foam":       ("Foam",       3),
    }),
    "readers": ("Readers", 3, {
        "sunglass":   ("Sunglass",   1),
        "clear":      ("Clear",      2),
        "computer":   ("Computer",   3),
        "multifocal": ("Multifocal", 4),
    }),
    "cases-accessories": ("Cases & Accessories", 4),
}

PRODUCT_PATHS = {
    # Sunglasses > Sport only
    "prosport-apollo-safety-wrap-sunglasses":            [("sunglasses", "sport")],
    "prosport-aruba-sport-sunglasses":                   [("sunglasses", "sport")],
    "prosport-boulder-sport-sunglasses":                 [("sunglasses", "sport")],
    "prosport-bravado-sunglasses":                       [("sunglasses", "sport")],
    "prosport-cliff-sport-sunglasses":                   [("sunglasses", "sport")],
    "prosport-conquest-wide-sunglasses":                 [("sunglasses", "sport")],
    "prosport-el-capitan-big-tall-sunglasses":           [("sunglasses", "sport")],
    "prosport-fareway":                                  [("sunglasses", "sport")],
    "prosport-finish-sunglasses":                        [("sunglasses", "sport")],
    "prosport-fuel-sport-sunglasses":                    [("sunglasses", "sport")],
    "prosport-road-gator-sport-sunglasses":              [("sunglasses", "sport")],
    "prosport-sly":                                      [("sunglasses", "sport")],
    "prosport-sonic-sport-sunglasses":                   [("sunglasses", "sport")],
    "prosport-speedracer-clear-sunglasses":              [("sunglasses", "sport")],
    "prosport-trans-am":                                 [("sunglasses", "sport")],
    # Sport + Polarized
    "prosport-axle-polarized-wrap-sunglasses":           [("sunglasses", "sport"), ("sunglasses", "polarized")],
    "prosport-bombora-polarized-float-sunglasses":       [("sunglasses", "sport"), ("sunglasses", "polarized")],
    "prosport-sharktail-polarized-float-sunglasses":     [("sunglasses", "sport"), ("sunglasses", "polarized")],
    # Sport + Mirror
    "prosport-x-ray-mirror-sport-sunglasses":            [("sunglasses", "sport"), ("sunglasses", "mirror")],
    # Sport + Readers > Sunglass
    "prosport-rocket-high-wrap-reader-sunglasses":       [("sunglasses", "sport"), ("readers", "sunglass")],
    # Sport + Bifocals > Standard
    "prosport-dolphin-wrap-bifocal-sunglasses":          [("sunglasses", "sport"), ("bifocals", "standard")],
    # Sunglasses > Polarized only
    "prosport-altitude-polarized-leather-shield-sunglasses": [("sunglasses", "polarized")],
    "prosport-apex-day-vision-polarized-sunglasses":     [("sunglasses", "polarized")],
    "prosport-aruba-polarized-sunglasses":               [("sunglasses", "polarized")],
    "prosport-boxer-polarized-sunglasses":               [("sunglasses", "polarized")],
    "prosport-breaker-polarized":                        [("sunglasses", "polarized")],
    "prosport-clipper-polarized-sunglasses":             [("sunglasses", "polarized")],
    "prosport-gazelle-polarized-sunglasses":             [("sunglasses", "polarized")],
    "prosport-goby-half-rim-polarized-sunglasses":       [("sunglasses", "polarized")],
    "prosport-hammer-head-polarized-sunglasses":         [("sunglasses", "polarized")],
    "prosport-outrigger-polarized-sunglasses":           [("sunglasses", "polarized")],
    "prosport-pike-polarized-square-sunglasses":         [("sunglasses", "polarized")],
    "prosport-piranha-polarized-sunglasses":             [("sunglasses", "polarized")],
    "prosport-striper-polarized-sunglasses":             [("sunglasses", "polarized")],
    "prosport-surf-polarized":                           [("sunglasses", "polarized")],
    "prosport-turismo-polarized-sunglasses":             [("sunglasses", "polarized")],
    "prosport-turk-half-rim-polarized-sunglasses":       [("sunglasses", "polarized")],
    # Polarized + HD Lens
    "prosport-formula1-hd-copper-polarized-sunglasses":  [("sunglasses", "polarized"), ("sunglasses", "hd-lens")],
    "prosport-serengeti-hd-polarized-sunglasses":        [("sunglasses", "polarized"), ("sunglasses", "hd-lens")],
    # Polarized + Night
    "prosport-eliminator-polarized-night-vision-sunglasses": [("sunglasses", "polarized"), ("sunglasses", "night")],
    "prosport-equinox-yellow-polarized-sunglasses":      [("sunglasses", "polarized"), ("sunglasses", "night")],
    "prosport-panama-yellow-polarized-sunglasses":       [("sunglasses", "polarized"), ("sunglasses", "night")],
    "prosport-sahara-yellow-polarized-sunglasses":       [("sunglasses", "polarized"), ("sunglasses", "night")],
    # Polarized + Mirror
    "prosport-aero-mirror-polarized-sunglasses":         [("sunglasses", "polarized"), ("sunglasses", "mirror")],
    "prosport-atoll-mirror-polarized-sunglasses":        [("sunglasses", "polarized"), ("sunglasses", "mirror")],
    "prosport-barbados-mirror-polarized-sunglasses":     [("sunglasses", "polarized"), ("sunglasses", "mirror")],
    "prosport-dozer-polarized-mirror-sunglasses":        [("sunglasses", "polarized"), ("sunglasses", "mirror")],
    "prosport-gremlin-mirror-polarized-sunglasses":      [("sunglasses", "polarized"), ("sunglasses", "mirror")],
    "prosport-mercury-polarized-mirror-sunglasses":      [("sunglasses", "polarized"), ("sunglasses", "mirror")],
    # Polarized + Aviator
    "prosport-atoll-polarized-square-aviator-sunglasses": [("sunglasses", "polarized"), ("sunglasses", "aviator")],
    "prosport-morocco-polarized-aviator-sunglasses":     [("sunglasses", "polarized"), ("sunglasses", "aviator")],
    "prosport-surge-polarized-aviator-sunglasses":       [("sunglasses", "polarized"), ("sunglasses", "aviator")],
    # Polarized + Mirror + Aviator
    "prosport-morocco-polarized-mirror-sunglasses":      [("sunglasses", "polarized"), ("sunglasses", "mirror"), ("sunglasses", "aviator")],
    # Sunglasses > HD Lens only
    "prosport-air-parcel-rimless-hd-copper-sunglasses":  [("sunglasses", "hd-lens")],
    "prosport-cartel-hd-copper-sunglasses":              [("sunglasses", "hd-lens")],
    "prosport-draft-rimless-hd-copper-sunglasses":       [("sunglasses", "hd-lens")],
    "prosport-eagle-eye-hd-copper-sunglasses":           [("sunglasses", "hd-lens")],
    "prosport-falcon-hd-copper-sunglasses":              [("sunglasses", "hd-lens")],
    "prosport-gear-box-hd-copper-sunglasses":            [("sunglasses", "hd-lens")],
    "prosport-navigator-rimless-hd-copper-sunglasses":   [("sunglasses", "hd-lens")],
    "prosport-speedracer-hd-copper-sunglasses":          [("sunglasses", "hd-lens")],
    "prosport-spinner-rimless-hd-copper-sunglasses":     [("sunglasses", "hd-lens")],
    # Sunglasses > Night only
    "prosport-baffle-night-vision-sunglasses":           [("sunglasses", "night")],
    "prosport-eliminator-night-vision-sunglasses":       [("sunglasses", "night")],
    "prosport-flite-hd-vision-sunglasses":               [("sunglasses", "night")],
    "prosport-freeway-yellow-sunglasses":                [("sunglasses", "night")],
    "prosport-metric-night-vision-sunglasses":           [("sunglasses", "night")],
    "prosport-nitrous-hd-vision-sunglasses":             [("sunglasses", "night")],
    "prosport-phoenix-yellow-sunglasses":                [("sunglasses", "night")],
    "prosport-trooper-night-driving-sunglasses":         [("sunglasses", "night")],
    "prosport-turismo-night-driving-sunglasses":         [("sunglasses", "night")],
    "prosport-vortex-night-vision-sunglasses":           [("sunglasses", "night")],
    # Night + Bifocals > Standard
    "prosport-eliminator-night-vision-bifocal":          [("sunglasses", "night"), ("bifocals", "standard")],
    # Sunglasses > Mirror only
    "prosport-ace-mirror-sunglasses":                    [("sunglasses", "mirror")],
    "prosport-hotrod-mirror-sunglasses":                 [("sunglasses", "mirror")],
    "prosport-mako-metal-mirror-sunglasses":             [("sunglasses", "mirror")],
    "prosport-neptune-mirror-sunglasses":                [("sunglasses", "mirror")],
    "prosport-turismo-mirror-sunglasses":                [("sunglasses", "mirror")],
    "prosport-wobbegong-mirror-sunglasses":              [("sunglasses", "mirror")],
    # Mirror + Bifocals > Standard
    "prosport-cabriolet-mirror-bifocal":                 [("sunglasses", "mirror"), ("bifocals", "standard")],
    # Mirror + Aviator
    "prosport-yogi-mirror-aviator-sunglasses":           [("sunglasses", "mirror"), ("sunglasses", "aviator")],
    # Sunglasses > Aviator only
    "prosport-barrel-aviator-sunglasses":                [("sunglasses", "aviator")],
    "prosport-monza-aviator-inspired-sunglasses":        [("sunglasses", "aviator")],
    "prosport-morocco-sunglasses":                       [("sunglasses", "aviator")],
    # Aviator + Readers > Sunglass
    "prosport-runway-aviator-sunglass-readers":          [("sunglasses", "aviator"), ("readers", "sunglass")],
    # Sunglasses > Fashion
    "brandy":                                            [("sunglasses", "fashion")],
    "carmen-fashion-sunglasses":                         [("sunglasses", "fashion")],
    "miami-square-fashion-sunglasses":                   [("sunglasses", "fashion")],
    "popcat":                                            [("sunglasses", "fashion")],
    "prosport-kuna":                                     [("sunglasses", "fashion")],
    "sputnik-sunglasses":                                [("sunglasses", "fashion")],
    "zulu-metal-fashion-sunglasses":                     [("sunglasses", "fashion")],
    # Bifocals > Standard only
    "prosport-blade-bifocal":                            [("bifocals", "standard")],
    "prosport-cleo-bifocal-sunglasses":                  [("bifocals", "standard")],
    "prosport-eliminator-day-vision-bifocal":            [("bifocals", "standard")],
    "prosport-first-lady-bifocal":                       [("bifocals", "standard")],
    "prosport-garnet-gradient-bifocal":                  [("bifocals", "standard")],
    "prosport-glider-bifocal":                           [("bifocals", "standard")],
    "prosport-hawkeye-bifocal":                          [("bifocals", "standard")],
    "prosport-hawkeye-hd-bifocal":                       [("bifocals", "standard")],
    "prosport-liverpool-hd-bifocal":                     [("bifocals", "standard")],
    "prosport-liverpool-smoke-bifocal":                  [("bifocals", "standard")],
    "prosport-marigold-bifocal-sunglasses":              [("bifocals", "standard")],
    "prosport-methane-bifocal":                          [("bifocals", "standard")],
    "prosport-pheaton-bifocal":                          [("bifocals", "standard")],
    "prosport-puma-bifocal":                             [("bifocals", "standard")],
    "prosport-spike-bifocal":                            [("bifocals", "standard")],
    "prosport-starlet-bifocal":                          [("bifocals", "standard")],
    "prosport-tailpipe-bifocal":                         [("bifocals", "standard")],
    "prosport-venice-womens-bifocal-sunglasses":         [("bifocals", "standard")],
    "prosport-wallstreet-bifocal":                       [("bifocals", "standard")],
    # Bifocals > Polarized
    "prosport-cobalt-polarized-bifocal":                 [("bifocals", "polarized")],
    "prosport-commando-polarized-bifocal":               [("bifocals", "polarized")],
    "prosport-karma-polarized-bifocal":                  [("bifocals", "polarized")],
    "prosport-kumatage-polarized-bifocal":               [("bifocals", "polarized")],
    "prosport-orchid-lady-polarized-bifocal":            [("bifocals", "polarized")],
    "prosport-overdrive-polarized-bifocal":              [("bifocals", "polarized")],
    "prosport-pheaton-polarized-bifocal":                [("bifocals", "polarized")],
    "prosport-sharkbait-polarized-bifocal":              [("bifocals", "polarized")],
    "prosport-talon-polarized-bifocal":                  [("bifocals", "polarized")],
    "prosport-taxi-polarized-bifocal":                   [("bifocals", "polarized")],
    # Bifocals > Foam
    "prosport-airfoil-foam-bifocal":                     [("bifocals", "foam")],
    "prosport-horsepower-foam-bifocal":                  [("bifocals", "foam")],
    "prosport-quake-foam-bifocal":                       [("bifocals", "foam")],
    "prosport-xcalibre-foam-bifocal":                    [("bifocals", "foam")],
    "prosport-zorst-foam-bifocal":                       [("bifocals", "foam")],
    # Readers > Sunglass only
    "prosport-jersey-sunglass-readers":                  [("readers", "sunglass")],
    "prosport-monaco-sunglass-readers":                  [("readers", "sunglass")],
    "prosport-regal-reader":                             [("readers", "sunglass")],
    # Readers > Clear
    "prosport-carraway-reader":                          [("readers", "clear")],
    "prosport-clutch-reader":                            [("readers", "clear")],
    "prosport-garnet-gradient-reader":                   [("readers", "clear")],
    "prosport-gypsy-reader":                             [("readers", "clear")],
    "prosport-kitty-reader":                             [("readers", "clear")],
    "prosport-liverpool-reader":                         [("readers", "clear")],
    "prosport-newport-reader":                           [("readers", "clear")],
    "prosport-sonoma-reader":                            [("readers", "clear")],
    "prosport-studebaker-reader":                        [("readers", "clear")],
    # Readers > Computer
    "prosport-kennedy-computer-reader":                  [("readers", "computer")],
    "prosport-magellan-computer-reader":                 [("readers", "computer")],
    # Readers > Multifocal
    "prosport-georgetown-multifocal-reader":             [("readers", "multifocal")],
    "prosport-harvard-multifocal-reader":                [("readers", "multifocal")],
    "prosport-kennedy-multifocal-reader":                [("readers", "multifocal")],
    "prosport-professor-multifocal-reader":              [("readers", "multifocal")],
    "prosport-studio-multifocal-reader":                 [("readers", "multifocal")],
    # Cases & Accessories
    "agate-lady-black-extra-large-leather-case":         [("cases-accessories",)],
    "ametrine-medium-leather-hard-case":                 [("cases-accessories",)],
    "citrine-woody-hard-case":                           [("cases-accessories",)],
    "garnet-deep-zipper-case-with-clipper":              [("cases-accessories",)],
    "hematite-small-shiny-leather-case":                 [("cases-accessories",)],
    "jade-deep-fabric-case":                             [("cases-accessories",)],
    "leopard-print-hard-case":                           [("cases-accessories",)],
}


def resolve_path(path_tuple):
    nodes = []
    current = TREE
    last_entry = None
    for i, node_slug in enumerate(path_tuple):
        if node_slug not in current:
            raise ValueError(f"Slug '{node_slug}' not found at level {i + 1} of path {path_tuple}")
        entry = current[node_slug]
        nodes.append({"level": i + 1, "name": entry[0], "slug": node_slug, "sortOrder": entry[1]})
        last_entry = entry
        if i < len(path_tuple) - 1:
            if len(entry) < 3:
                raise ValueError(f"'{node_slug}' is a leaf but path {path_tuple} continues past it")
            current = entry[2]
    if len(last_entry) > 2:
        raise ValueError(f"Path {path_tuple} ends at a non-leaf node (has children)")
    return nodes


items = json.loads(in_path.read_text())
item_slugs = {item["slug"] for item in items}

errors = []
for product_slug in PRODUCT_PATHS:
    if product_slug not in item_slugs:
        errors.append(f"PRODUCT_PATHS has '{product_slug}' but it is not in items")
for item in items:
    if item["slug"] not in PRODUCT_PATHS:
        errors.append(f"No category assigned for '{item['slug']}'")
if errors:
    for e in errors:
        print(f"ERROR: {e}")
    raise SystemExit(f"{len(errors)} coverage error(s) — fix PRODUCT_PATHS before proceeding")

category_counts = {}
for item in items:
    paths = PRODUCT_PATHS[item["slug"]]
    resolved = []
    leaf_slugs = []
    for path_tuple in paths:
        nodes = resolve_path(path_tuple)
        resolved.append(nodes)
        leaf = path_tuple[-1]
        if leaf in leaf_slugs:
            errors.append(f"'{item['slug']}': duplicate leaf '{leaf}'")
        leaf_slugs.append(leaf)
        category_counts[path_tuple] = category_counts.get(path_tuple, 0) + 1
    item["categories"] = resolved

if errors:
    for e in errors:
        print(f"ERROR: {e}")
    raise SystemExit(f"{len(errors)} error(s) — fix before proceeding")

out_dir = BASE / "data" / slug / "categorize-items"
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "items.json").write_text(json.dumps(items, indent=2, ensure_ascii=False))

print(f"Categorized {len(items)} items")
for path_tuple, count in sorted(category_counts.items()):
    print(f"  {' > '.join(path_tuple)}: {count}")
total_assignments = sum(category_counts.values())
print(f"Total path assignments: {total_assignments} ({total_assignments - len(items):+d} vs unique)")
