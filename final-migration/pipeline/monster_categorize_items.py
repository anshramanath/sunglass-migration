import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
if brand_key != "monster":
    raise SystemExit(f"This script is for monster only (got BRAND={brand_key})")
slug = config["slug"]

in_path = BASE / "data" / slug / "clean-content" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run clean_content.py first. Not found: {in_path}")

# TREE: slug -> (name, sortOrder) for leaf nodes
#             -> (name, sortOrder, {children}) for non-leaf nodes
TREE = {
    "fashion": ("Fashion", 1),
    "sunglasses": ("Sunglasses", 2, {
        "sport":      ("Sport",      1),
        "polarized":  ("Polarized",  2),
        "hd-lens":    ("HD Lens",    3),
        "night":      ("Night",      4),
        "mirror":     ("Mirror",     5),
        "aviator":    ("Aviator",    6),
        "wide-fit":   ("Wide Fit",   7),
    }),
    "bifocals": ("Bifocals", 3, {
        "standard":   ("Standard",   1),
        "polarized":  ("Polarized",  2),
        "foam":       ("Foam",       3),
    }),
    "readers": ("Readers", 4, {
        "sunglass":   ("Sunglass",   1),
        "clear":      ("Clear",      2),
        "computer":   ("Computer",   3),
        "multifocal": ("Multifocal", 4),
    }),
    "cases-accessories": ("Cases & Accessories", 5),
}

PRODUCT_PATHS = {
    # Fashion
    "abba-retro-sunglasses":                             [("fashion",)],
    "airspeed":                                          [("fashion",)],
    "aloha-polarized":                                   [("fashion",)],
    "bacardi":                                           [("fashion",)],
    "belini-fashion-gradient-sunglasses":                [("fashion",)],
    "boho-retro-sunglasses":                             [("fashion",)],
    "brandy":                                            [("fashion",)],
    "bravado-mirror-polarized":                          [("fashion",)],
    "bravado-polarized-sunglasses":                      [("fashion",)],
    "bullseye":                                          [("fashion",)],
    "bungalow-polarized":                                [("fashion",)],
    "cappuchino":                                        [("fashion",)],
    "carina-polarized":                                  [("fashion",)],
    "carmen-fashion-sunglasses":                         [("fashion",)],
    "childrens-boys-girls-flip-up-shield":               [("fashion",)],
    "chloe-polarized-lady-sunglasses":                   [("fashion",)],
    "convair":                                           [("fashion",)],
    "coral-ii-polarized-sunglasses":                     [("fashion",)],
    "coupe":                                             [("fashion",)],
    "gazelle-polarized":                                 [("fashion",)],
    "gemini":                                            [("fashion",)],
    "gemini-mirror-round-metal-sunglasses":              [("fashion",)],
    "giselle":                                           [("fashion",)],
    "hairpin":                                           [("fashion",)],
    "horizon":                                           [("fashion",)],
    "jupiter":                                           [("fashion",)],
    "jupiter-polarized":                                 [("fashion",)],
    "kiki-retro-fashion-sunglasses":                     [("fashion",)],
    "lennon-sunglasses":                                 [("fashion",)],
    "lexi-cat-eye-sunglasses":                           [("fashion",)],
    "locs-amigo-9003":                                   [("fashion",)],
    "locs-bario-9083":                                   [("fashion",)],
    "locs-bel-air-91149":                                [("fashion",)],
    "locs-camino-91185":                                 [("fashion",)],
    "locs-cruiser-91055":                                [("fashion",)],
    "locs-del-ray-91102":                                [("fashion",)],
    "locs-deville-91026":                                [("fashion",)],
    "locs-fleetwood-91182":                              [("fashion",)],
    "locs-hombre-9035":                                  [("fashion",)],
    "locs-impala-91025":                                 [("fashion",)],
    "locs-mark-v-91180":                                 [("fashion",)],
    "locs-monte-carlo-9058":                             [("fashion",)],
    "locs-san-diego-91111":                              [("fashion",)],
    "locs-showtime-91148":                               [("fashion",)],
    "locs-tuner-91045":                                  [("fashion",)],
    "locs-voodoo-91160":                                 [("fashion",)],
    "madeline":                                          [("fashion",)],
    "mahi-polarized-sunglasses":                         [("fashion",)],
    "maverick-polarized":                                [("fashion",)],
    "miami-square-fashion-sunglasses":                   [("fashion",)],
    "mondial-polarized-sunglasses":                      [("fashion",)],
    "ohana":                                             [("fashion",)],
    "opal":                                              [("fashion",)],
    "phantom":                                           [("fashion",)],
    "playa-cat-eye-retro-sunglasses":                    [("fashion",)],
    "popcat":                                            [("fashion",)],
    "redline":                                           [("fashion",)],
    "reflex":                                            [("fashion",)],
    "reggae":                                            [("fashion",)],
    "savannah":                                          [("fashion",)],
    "shaka-retro-sunglasses":                            [("fashion",)],
    "simi-sunglasses":                                   [("fashion",)],
    "spear":                                             [("fashion",)],
    "spunk-sunglasses":                                  [("fashion",)],
    "sputnik-sunglasses":                                [("fashion",)],
    "stinger-polarized":                                 [("fashion",)],
    "storm":                                             [("fashion",)],
    "tahiti-polarized":                                  [("fashion",)],
    "tango-round-metal-style":                           [("fashion",)],
    "torpedo":                                           [("fashion",)],
    "traffic":                                           [("fashion",)],
    "vato":                                              [("fashion",)],
    "x-loop-3304":                                       [("fashion",)],
    "x-loop-3322":                                       [("fashion",)],
    "zulu-metal-fashion-sunglasses":                     [("fashion",)],
    # Sunglasses > Sport only
    "prosport-apollo-safety-wrap-sunglasses":            [("sunglasses", "sport")],
    "prosport-aruba-sport-sunglasses":                   [("sunglasses", "sport")],
    "prosport-boulder-sport-sunglasses":                 [("sunglasses", "sport")],
    "prosport-bravado-sunglasses":                       [("sunglasses", "sport")],
    "prosport-cliff-sport-sunglasses":                   [("sunglasses", "sport")],
    "prosport-fareway":                                  [("sunglasses", "sport")],
    "prosport-finish-sunglasses":                        [("sunglasses", "sport")],
    "prosport-fuel-sport-sunglasses":                    [("sunglasses", "sport")],
    "prosport-kuna":                                     [("sunglasses", "sport")],
    "prosport-lava-fury-wood-sunglasses":                [("sunglasses", "sport")],
    "prosport-road-gator-sport-sunglasses":              [("sunglasses", "sport")],
    "prosport-sly":                                      [("sunglasses", "sport")],
    "prosport-sonic-sport-sunglasses":                   [("sunglasses", "sport")],
    "prosport-speedracer-clear-sunglasses":              [("sunglasses", "sport")],
    "prosport-trans-am":                                 [("sunglasses", "sport")],
    "prosport-tsunami-rectangular-sunglasses":           [("sunglasses", "sport")],
    # Sport + Polarized
    "prosport-altitude-polarized-leather-shield-sunglasses": [("sunglasses", "sport"), ("sunglasses", "polarized")],
    "prosport-axle-polarized-wrap-sunglasses":           [("sunglasses", "sport"), ("sunglasses", "polarized")],
    "prosport-bombora-polarized-float-sunglasses":       [("sunglasses", "sport"), ("sunglasses", "polarized")],
    "prosport-seaway-polarized-float-sunglasses":        [("sunglasses", "sport"), ("sunglasses", "polarized")],
    "prosport-sharktail-polarized-float-sunglasses":     [("sunglasses", "sport"), ("sunglasses", "polarized")],
    # Sport + Mirror
    "prosport-x-ray-mirror-sport-sunglasses":            [("sunglasses", "sport"), ("sunglasses", "mirror")],
    # Sport + Bifocals > Standard
    "prosport-dolphin-wrap-bifocal-sunglasses":          [("sunglasses", "sport"), ("bifocals", "standard")],
    # Sunglasses > Polarized only
    "prosport-apex-day-vision-polarized-sunglasses":     [("sunglasses", "polarized")],
    "prosport-aruba-polarized-sunglasses":               [("sunglasses", "polarized")],
    "prosport-boxer-polarized-sunglasses":               [("sunglasses", "polarized")],
    "prosport-breaker-polarized":                        [("sunglasses", "polarized")],
    "prosport-clipper-polarized-sunglasses":             [("sunglasses", "polarized")],
    "prosport-gazelle-polarized-sunglasses":             [("sunglasses", "polarized")],
    "prosport-goby-half-rim-polarized-sunglasses":       [("sunglasses", "polarized")],
    "prosport-hammer-head-polarized-sunglasses":         [("sunglasses", "polarized")],
    "prosport-marlin-polarized":                         [("sunglasses", "polarized")],
    "prosport-monza-polarized-sunglasses":               [("sunglasses", "polarized")],
    "prosport-outrigger-polarized-sunglasses":           [("sunglasses", "polarized")],
    "prosport-pike-polarized-square-sunglasses":         [("sunglasses", "polarized")],
    "prosport-piranha-polarized-sunglasses":             [("sunglasses", "polarized")],
    "prosport-striper-polarized-sunglasses":             [("sunglasses", "polarized")],
    "prosport-surf-polarized":                           [("sunglasses", "polarized")],
    "prosport-turismo-polarized-sunglasses":             [("sunglasses", "polarized")],
    "prosport-turk-half-rim-polarized-sunglasses":       [("sunglasses", "polarized")],
    "prosport-wahoo-polarized":                          [("sunglasses", "polarized")],
    "prosport-waikiki-polarized-sunglasses":             [("sunglasses", "polarized")],
    # Polarized + HD Lens
    "prosport-formula1-hd-copper-polarized-sunglasses":  [("sunglasses", "polarized"), ("sunglasses", "hd-lens")],
    "prosport-serengeti-hd-polarized-sunglasses":        [("sunglasses", "polarized"), ("sunglasses", "hd-lens")],
    # Polarized + HD Lens + Aviator
    "prosport-skyline-aviator-hd-polarized-sunglasses":  [("sunglasses", "polarized"), ("sunglasses", "hd-lens"), ("sunglasses", "aviator")],
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
    "prosport-spitzer-night-vision-sunglasses":          [("sunglasses", "night")],
    "prosport-trooper-night-driving-sunglasses":         [("sunglasses", "night")],
    "prosport-turismo-night-driving-sunglasses":         [("sunglasses", "night")],
    "prosport-vortex-night-vision-sunglasses":           [("sunglasses", "night")],
    # Night + Bifocals > Standard
    "prosport-eliminator-night-vision-bifocal":          [("sunglasses", "night"), ("bifocals", "standard")],
    # Sunglasses > Mirror only
    "prosport-ace-mirror-sunglasses":                    [("sunglasses", "mirror")],
    "prosport-bravado-mirrored-sunglasses":              [("sunglasses", "mirror")],
    "prosport-hotrod-mirror-sunglasses":                 [("sunglasses", "mirror")],
    "prosport-mako-metal-mirror-sunglasses":             [("sunglasses", "mirror")],
    "prosport-neptune-mirror-sunglasses":                [("sunglasses", "mirror")],
    "prosport-nokona-mirror-sunglasses":                 [("sunglasses", "mirror")],
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
    "prosport-runway-aviator-sun-reader":                [("sunglasses", "aviator"), ("readers", "sunglass")],
    # Sunglasses > Wide Fit
    "prosport-conquest-wide-sunglasses":                 [("sunglasses", "wide-fit")],
    "prosport-el-capitan-big-tall-sunglasses":           [("sunglasses", "wide-fit")],
    "prosport-equator-wide-sunglasses":                  [("sunglasses", "wide-fit")],
    "prosport-everest-wide-sunglasses":                  [("sunglasses", "wide-fit")],
    # Bifocals > Standard only
    "cabana-bifocal":                                    [("bifocals", "standard")],
    "cadet-bifocal-sunglasses":                          [("bifocals", "standard")],
    "cognac-bifocal-sunglasses":                         [("bifocals", "standard")],
    "gullwing-bifocal":                                  [("bifocals", "standard")],
    "iris-bifocal":                                      [("bifocals", "standard")],
    "metre-bifocal":                                     [("bifocals", "standard")],
    "pacific-mirror-bifocal":                            [("bifocals", "standard")],
    "prosport-blade-bifocal":                            [("bifocals", "standard")],
    "prosport-bypass-bifocal":                           [("bifocals", "standard")],
    "prosport-cleo-bifocal-sunglasses":                  [("bifocals", "standard")],
    "prosport-cooper-bifocal":                           [("bifocals", "standard")],
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
    "colorado-polarized-bifocal":                        [("bifocals", "polarized")],
    "eliminator-polarized-bifocal":                      [("bifocals", "polarized")],
    "prosport-cobalt-polarized-bifocal":                 [("bifocals", "polarized")],
    "prosport-commando-polarized-bifocal":               [("bifocals", "polarized")],
    "prosport-cooper-polarized-bifocal":                 [("bifocals", "polarized")],
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
    "cole-sun-reader":                                   [("readers", "sunglass")],
    "monaco-sun-reader":                                 [("readers", "sunglass")],
    "prosport-jersey-sun-reader":                        [("readers", "sunglass")],
    "prosport-regal-reader":                             [("readers", "sunglass")],
    "verbena-sun-reader":                                [("readers", "sunglass")],
    "voyager-reading-sunglasses":                        [("readers", "sunglass")],
    # Readers > Clear
    "dorothy-reader":                                    [("readers", "clear")],
    "holiday-reader":                                    [("readers", "clear")],
    "loft-reader":                                       [("readers", "clear")],
    "newport-reader-one-size-fits-all":                  [("readers", "clear")],
    "onyx-reader":                                       [("readers", "clear")],
    "prosport-carraway-reader":                          [("readers", "clear")],
    "prosport-clutch-reader":                            [("readers", "clear")],
    "prosport-garnet-gradient-reader":                   [("readers", "clear")],
    "prosport-gypsy-reader":                             [("readers", "clear")],
    "prosport-kitty-reader":                             [("readers", "clear")],
    "prosport-liverpool-reader":                         [("readers", "clear")],
    "prosport-sonoma-reader":                            [("readers", "clear")],
    "prosport-studebaker-reader":                        [("readers", "clear")],
    "trek-cover-over-full-lens-reader":                  [("readers", "clear")],
    # Readers > Computer
    "prosport-kennedy-computer-reader":                  [("readers", "computer")],
    "prosport-magellan-computer-reader":                 [("readers", "computer")],
    # Readers > Multifocal
    "bombay-multifocal-reader":                          [("readers", "multifocal")],
    "hailey-multifocal-reader":                          [("readers", "multifocal")],
    "pixel-multifocal-reader":                           [("readers", "multifocal")],
    "prosport-georgetown-multifocal-reader":             [("readers", "multifocal")],
    "prosport-kennedy-multifocal-reader":                [("readers", "multifocal")],
    "prosport-professor-multifocal-reader":              [("readers", "multifocal")],
    "prosport-studio-multifocal-reader":                 [("readers", "multifocal")],
    "spy-multifocal-reader":                             [("readers", "multifocal")],
    # Cases & Accessories
    "agate-lady-black-extra-large-leather-case":         [("cases-accessories",)],
    "ametrine-medium-leather-hard-case":                 [("cases-accessories",)],
    "black-reusable-stretch-face-mask":                  [("cases-accessories",)],
    "citrine-woody-hard-case":                           [("cases-accessories",)],
    "garnet-deep-zipper-case-with-clipper":              [("cases-accessories",)],
    "hematite-small-shiny-leather-case":                 [("cases-accessories",)],
    "jade-deep-fabric-case":                             [("cases-accessories",)],
    "vshield-vibrant-100-cotton-2-pack-bandannas-you-get-2-pieces-of-color-you-choose-black-red-navy-blue-royal-bluehot-pink-in-stock": [("cases-accessories",)],
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
