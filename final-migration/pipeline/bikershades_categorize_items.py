import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
if brand_key != "bikershades":
    raise SystemExit(f"This script is for bikershades only (got BRAND={brand_key})")
slug = config["slug"]

in_path = BASE / "data" / slug / "clean-content" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run clean_content.py first. Not found: {in_path}")

TREE = {
    "brands": ("Brands", 1, {
        "bikerarmour": ("BikerArmour", 1, {
            "foam-goggles":  ("Foam Goggles",  1),
            "cover-overs":   ("Cover Overs",   2),
            "photochromic":  ("Photochromic",  3),
            "combos":        ("Combos",        4),
        }),
        "wiley-x": ("Wiley X",  2),
        "7eye":    ("7Eye",     3),
    }),
    "sunglasses": ("Sunglasses", 2, {
        "sport":      ("Sport",      1),
        "polarized":  ("Polarized",  2),
        "hd-lens":    ("HD Lens",    3),
        "night":      ("Night",      4),
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

FG  = ("brands", "bikerarmour", "foam-goggles")
CO  = ("brands", "bikerarmour", "cover-overs")
PC  = ("brands", "bikerarmour", "photochromic")
CMB = ("brands", "bikerarmour", "combos")
WX  = ("brands", "wiley-x")
SE  = ("brands", "7eye")
SPT = ("sunglasses", "sport")
POL = ("sunglasses", "polarized")
HD  = ("sunglasses", "hd-lens")
NGT = ("sunglasses", "night")
BST = ("bifocals", "standard")
BPL = ("bifocals", "polarized")
BFM = ("bifocals", "foam")
RSG = ("readers", "sunglass")
RCL = ("readers", "clear")
RCP = ("readers", "computer")
RMF = ("readers", "multifocal")
CAS = ("cases-accessories",)

PRODUCT_PATHS = {
    # Brands > BikerArmour > Foam Goggles only
    "alfer-clear":                                       [FG],
    "alfer-go-pink":                                     [FG],
    "alfer-hd":                                          [FG],
    "angel-for-ladies-clear-fits-med-lg-heads":          [FG],
    "angel-for-ladies-hd-fits-med-lg-heads":             [FG],
    "barricade-clear-lens-fits-med-xlg-heads":           [FG],
    "bikerarmour-air-boss-lg-xlg":                       [FG],
    "bikerarmour-alfer-fits-xs-sm":                      [FG],
    "bikerarmour-anaconda-med-lg":                       [FG],
    "bikerarmour-angel-chrome-with-rhinestones-med-lg":  [FG],
    "bikerarmour-angel-med-lg":                          [FG],
    "bikerarmour-barricade-med-xlg":                     [FG],
    "bikerarmour-blower-goggles-med-xxlg":               [FG],
    "bikerarmour-bumblebee-goggles-sm-lg":               [FG],
    "bikerarmour-camber-lg-xl":                          [FG],
    "bikerarmour-camshaft-sm-med":                       [FG],
    "bikerarmour-cayman-xsm-sm":                         [FG],
    "bikerarmour-cobra-sm-med":                          [FG],
    "bikerarmour-cyclone-med-lg":                        [FG],
    "bikerarmour-detonate-med-lg":                       [FG],
    "bikerarmour-downforce-med-xl":                      [FG],
    "bikerarmour-dragster-med-xl":                       [FG],
    "bikerarmour-dynamo-lg-xl":                          [FG],
    "bikerarmour-enduro-med-lg":                         [FG],
    "bikerarmour-evolution-med-xlg":                     [FG],
    "bikerarmour-horsepower-ii-med-xlg":                 [FG],
    "bikerarmour-lugnut-med-lg":                         [FG],
    "bikerarmour-magnum-chrome-med-lg":                  [FG],
    "bikerarmour-magnum-med-lg":                         [FG],
    "bikerarmour-marauder-lg-xl":                        [FG],
    "bikerarmour-mini-tank-sm-med":                      [FG],
    "bikerarmour-monster-lg-xl":                         [FG],
    "bikerarmour-night-hawk-med-xl":                     [FG],
    "bikerarmour-octane-lg-xlg":                         [FG],
    "bikerarmour-pinkie-sm-med":                         [FG],
    "bikerarmour-pola-bora-sm-med":                      [FG],
    "bikerarmour-renegade-sm-med":                       [FG],
    "bikerarmour-robin-mini-goggle-xxxs-sm":             [FG],
    "bikerarmour-slider-ii-med-lg":                      [FG],
    "bikerarmour-slider-med-xlg":                        [FG],
    "bikerarmour-spoiler-lg-xlg":                        [FG],
    "bikerarmour-spyder-sm-med":                         [FG],
    "bikerarmour-tank-goggles-med-xxlg":                 [FG],
    "bikerarmour-throttle-med-lg":                       [FG],
    "bikerarmour-thunder-goggle-sm-xl":                  [FG],
    "bikerarmour-tiger-goggle-sm-xl":                    [FG],
    "bikerarmour-transporter-lg-xl":                     [FG],
    "bikerarmour-valor-med-xlg":                         [FG],
    "bikerarmour-vanguard-sm-med":                       [FG],
    "bikerarmour-viper-med-lg":                          [FG],
    "blower-clear":                                      [FG],
    "bumblebee-clear":                                   [FG],
    "camber-clear":                                      [FG],
    "camshaft-clear":                                    [FG],
    "cayman-clear":                                      [FG],
    "cobra-clear":                                       [FG],
    "cobra-hd":                                          [FG],
    "detonate-clear":                                    [FG],
    "downforce-fits-med-xl-heads-clear":                 [FG],
    "downforce-fits-med-xl-heads-hd":                   [FG],
    "dragster-fits-med-xl-heads-clear":                  [FG],
    "dragster-fits-med-xl-heads-hd":                     [FG],
    "dynamo-fits-lg-xl-heads-clear":                     [FG],
    "enduro-clear-fits-med-lg-heads":                    [FG],
    "grid-foam-motorcycle-sunglasses-fits-lg-xlarge-heads": [FG],
    "horsepower-ii-fits-lg-xlg-heads-clear":             [FG],
    "lugnut-fits-med-lg-heads-clear":                    [FG],
    "magnum-chrome-clear":                               [FG],
    "magnum-clear":                                      [FG],
    "magnum-hd":                                         [FG],
    "marauder-clear":                                    [FG],
    "marauder-hd":                                       [FG],
    "mini-tank-fits-sm-med-heads-clear":                 [FG],
    "night-hawk-fits-medium-xlarge-heads-clear":         [FG],
    "night-hawk-fits-medium-xlarge-heads-hd":            [FG],
    "octane-fits-lg-xlg-heads-clear":                    [FG],
    "pola-bora-fits-sm-med-heads-clear":                 [FG],
    "pola-bora-fits-sm-med-heads-hd":                    [FG],
    "renegade-fits-sm-med-most-large-heads-clear":       [FG],
    "renegade-fits-sm-med-most-large-heads-hd":          [FG],
    "spoiler-fits-lg-xlg-heads-clear":                   [FG],
    "spyder-clear":                                      [FG],
    "tank-clear":                                        [FG],
    "throttle-fits-med-lg-heads-clear":                  [FG],
    "throttle-fits-med-lg-heads-hd":                     [FG],
    "transporter-fits-lg-xlarge-heads-clear":            [FG],
    # Foam Goggles + Night (yellow lens)
    "alfer-w-yellow-lens":                               [FG, NGT],
    "angel-for-ladies-yellow-lens-fits-med-lg-heads":    [FG, NGT],
    "blower-w-yellow-lens":                              [FG, NGT],
    "bumblebee-w-yellow-lens":                           [FG, NGT],
    "camber-w-yellow-lens":                              [FG, NGT],
    "camshaft-w-yellow-lens":                            [FG, NGT],
    "cayman-w-yellow-lens":                              [FG, NGT],
    "cobra-w-yellow-lens":                               [FG, NGT],
    "cronus-wrap-foam-motorcycle-sunglasses-for-night-riding": [FG, NGT],
    "detonate-w-yellow-lens":                            [FG, NGT],
    "downforce-fits-med-xl-heads-w-yellow-lens":         [FG, NGT],
    "dragster-fits-med-xl-heads-w-yellow-lens":          [FG, NGT],
    "dynamo-fits-lg-xl-heads-w-yellow-lens":             [FG, NGT],
    "enduro-w-yellow-lens-fits-med-lg-heads":            [FG, NGT],
    "horsepower-ii-fits-lg-xlg-heads-w-yellow-lens":     [FG, NGT],
    "lugnut-fits-med-lg-heads-w-yellow-lens":            [FG, NGT],
    "magnum-chrome-w-yellow-lens":                       [FG, NGT],
    "magnum-w-yellow-lens":                              [FG, NGT],
    "marauder-w-yellow-lens":                            [FG, NGT],
    "mini-tank-fits-sm-med-heads-w-yellow-lens":         [FG, NGT],
    "night-hawk-fits-medium-x-large-heads-w-yellow-lens": [FG, NGT],
    "octane-fits-lg-xlg-heads-w-yellow-lens":            [FG, NGT],
    "pola-bora-fits-sm-med-heads-w-yellow-lens":         [FG, NGT],
    "renegade-fits-sm-med-most-large-heads-w-yellow-lens": [FG, NGT],
    "spoiler-fits-lg-xlg-heads-w-yellow-lens":           [FG, NGT],
    "spyder-w-yellow-lens":                              [FG, NGT],
    "tank-w-yellow-lens":                                [FG, NGT],
    "throttle-fits-med-lg-heads-w-yellow-lens":          [FG, NGT],
    "transporter-fits-lg-xlarge-heads-yellow-lens":      [FG, NGT],
    # Foam Goggles + Polarized
    "alpine-polarized-glacier-leather-shield-sunglasses": [FG, POL],
    "altitude-polarized-glacier-leather-shield-sunglasses": [FG, POL],
    "socket-goggles-polarized":                          [FG, POL],
    # Brands > BikerArmour > Cover Overs only
    "bandit-clear":                                      [CO],
    "bandit-hd":                                         [CO],
    "bikerarmour-bandit-cover-over-with-strap-fits-over-sm-med-frames": [CO],
    "bikerarmour-bomber-cover-over-fits-over-sm-lg-frames": [CO],
    "bikerarmour-thunder-cover-over-fits-over-sm-med-frames": [CO],
    "bomber-cover-over-for-small-to-large-glasses-clear": [CO],
    "tiger-cover-over-fits-over-sm-med-glasses-clear":   [CO],
    # Cover Overs + Night
    "bandit-w-yellow-lens":                              [CO, NGT],
    "bomber-cover-over-for-small-to-large-glasses-w-yellow-lens": [CO, NGT],
    "tiger-cover-over-fits-over-sm-med-glasses-yellow-lens": [CO, NGT],
    # Cover Overs + Polarized
    "bandit-cover-over-w-strap-polarized-fits-over-sm-med-glasses": [CO, POL],
    "bomber-cover-over-for-small-to-large-glasses-polarized": [CO, POL],
    # Brands > BikerArmour > Photochromic
    "bikerarmour-air-boss-for-eclipse-xt-med-lg":                    [PC],
    "bikerarmour-alfer-eclipse-photochromic-xsm-sm":                 [PC],
    "bikerarmour-anaconda-eclipse-photochromic-med-lg":              [PC],
    "bikerarmour-anaconda-for-eclipse-xt-med-lg":                    [PC],
    "bikerarmour-angel-chrome-with-rhinestone-eclipse-photochromic-med-lg": [PC],
    "bikerarmour-angel-chrome-with-rhinestone-for-eclipse-xt-med-lg": [PC],
    "bikerarmour-angel-with-rhinestones-eclipse-photochromic-med-lg": [PC],
    "bikerarmour-angel-with-rhinstones-for-eclipse-xt-med-lg":       [PC],
    "bikerarmour-bandit-for-eclipse-xt-sm-med":                      [PC],
    "bikerarmour-blower-for-eclipse-xt-med-xx-lg":                   [PC],
    "bikerarmour-bumblebee-for-eclipse-xt-sm-med":                   [PC],
    "bikerarmour-detonate-for-eclipse-xt-med-lg":                    [PC],
    "bikerarmour-downforce-for-eclipse-xt-med-xl":                   [PC],
    "bikerarmour-dynamo-for-eclipse-xt-med-lg":                      [PC],
    "bikerarmour-enduro-for-eclipse-xt-med-lg":                      [PC],
    "bikerarmour-evolution-eclipse-photochromic-med-lg":             [PC],
    "bikerarmour-evolution-for-eclipse-xt-med-xlg":                  [PC],
    "bikerarmour-lugnut-for-eclipse-xt-med-lg":                      [PC],
    "bikerarmour-magnum-chrome-eclipse-photochromic-med-lg":         [PC],
    "bikerarmour-magnum-chrome-for-eclipse-xt-med-lg":               [PC],
    "bikerarmour-magnum-eclipse-photochromic-med-lg":                [PC],
    "bikerarmour-magnum-for-eclipse-xt-med-lg":                      [PC],
    "bikerarmour-marauder-for-eclipse-xt-lg-xlg":                    [PC],
    "bikerarmour-mini-tank-for-eclipse-xt-sm-med":                   [PC],
    "bikerarmour-monster-for-eclipse-xt-fits-lg-xl":                 [PC],
    "bikerarmour-night-hawk-eclipse-photochromic-med-xlg":           [PC],
    "bikerarmour-octane-for-eclipse-xt-lg-xl":                       [PC],
    "bikerarmour-pola-bora-for-eclipse-xt-sm-med":                   [PC],
    "bikerarmour-renegade-eclipse-photochromic-sm-med":              [PC],
    "bikerarmour-robin-for-eclipse-xt-xxsm-sm":                      [PC],
    "bikerarmour-socket-for-eclipse-xt-med-xxl":                     [PC],
    "bikerarmour-socket-goggle-eclipse-photochromic-one-size-fits-all": [PC],
    "bikerarmour-spoiler-eclipse-photochromic-lg-xlg":               [PC],
    "bikerarmour-spoiler-for-eclipse-xt-lg-xlg":                     [PC],
    "bikerarmour-spyder-for-eclipse-xt-sm-med":                      [PC],
    "bikerarmour-t-rex-eclipse-photochromic-med-lg":                 [PC],
    "bikerarmour-t-rex-for-eclipse-xt-med-xlg":                      [PC],
    "bikerarmour-tank-for-eclipse-xt-med-xlg":                       [PC],
    "bikerarmour-transporter-eclipse-photochromic-lg-xl":            [PC],
    "bikerarmour-transporter-for-eclipse-xt-lg-xlg":                 [PC],
    # Brands > BikerArmour > Combos
    "alfer-combos-fits-xs-sm-heads":                     [CMB],
    "anaconda-combo-fits-med-lg-heads":                  [CMB],
    "bikerarmour-angel-chrome-rhinestones-for-ladies-combos-fits-med-lg-heads": [CMB],
    "bikerarmour-magnum-chrome-combos-med-lg":           [CMB],
    "blower-combo-goggles-one-size-fits-all":            [CMB],
    "bomber-combo-cover-over-fits-small-to-large-glasses": [CMB],
    "bumblebee-combos-fits-sm-lg-heads":                 [CMB],
    "cobra-combos-fits-sm-med-heads":                    [CMB],
    "dragster-2-pair-combos-fits-med-xl-heads":          [CMB],
    "dynamo-combos-fits-lg-xl-heads":                    [CMB],
    "evolution-2-pair-combos-fits-med-xlg-heads":        [CMB],
    "horsepower-ii-2-pair-combofits-med-xlg-heads":      [CMB],
    "magnum-combos-fits-med-xlg-heads":                  [CMB],
    # Brands > Wiley X
    "wiley-x-airrage-for-eclipse-xt-sm-med":             [WX],
    "wiley-x-airrage-sm-med":                            [WX],
    "wiley-x-boss-for-eclipse-xt-med-lg":                [WX],
    "wiley-x-boss-med-xlg":                              [WX],
    "wiley-x-breach-for-eclipse-xt-med-lg":              [WX],
    "wiley-x-breach-med-lg":                             [WX],
    "wiley-x-brick-for-eclipse-xt-med-lg":               [WX],
    "wiley-x-brick-med-lg":                              [WX],
    "wiley-x-censor-for-eclipse-xt-sm-med":              [WX],
    "wiley-x-enzo-for-eclipse-xt-med-lg":                [WX],
    "wiley-x-enzo-med-lg":                               [WX],
    "wiley-x-gravity-for-eclipse-xt-med-lg":             [WX],
    "wiley-x-gravity-med-lg":                            [WX],
    "wiley-x-grid-for-eclipse-xt-lg-xxl":                [WX],
    "wiley-x-hudson-for-eclipse-xt-med-lg":              [WX],
    "wiley-x-ignite-for-eclipse-xt-sm-med":              [WX],
    "wiley-x-kingpin-for-eclipse-xt-sm-med":             [WX],
    "wiley-x-kingpin-sm-med":                            [WX],
    "wiley-x-nash-for-eclipse-xt-med-lg":                [WX],
    "wiley-x-omega-for-eclipse-xt-med-lg":               [WX],
    "wiley-x-omega-med-lg":                              [WX],
    "wiley-x-ovation-for-eclipse-xt-sm-lg":              [WX],
    "wiley-x-ozone-for-eclipse-xt-med-xl":               [WX],
    "wiley-x-p-17-sm-med":                               [WX],
    "wiley-x-p17-for-eclipse-xt-sm-med":                 [WX],
    "wiley-x-peak-for-eclipse-xt-med-lg":                [WX],
    "wiley-x-peak-med-lg":                               [WX],
    "wiley-x-rebel-alternate-fit-fits-med-lg-heads":     [WX],
    "wiley-x-rebel-for-eclipse-xt-alternative-fit-med-lg": [WX],
    "wiley-x-rebel-for-eclipse-xt-med-lg":               [WX],
    "wiley-x-romer3-for-eclipse-xt-med-lg":              [WX],
    "wiley-x-saint-for-eclipse-xt-sm-lg":                [WX],
    "wiley-x-slay-for-eclipse-xt-lg-xl":                 [WX],
    "wiley-x-slay-lg-xlg":                               [WX],
    "wiley-x-sleek-for-eclipse-xt-xs-sm":                [WX],
    "wiley-x-sleek-xs-sm":                               [WX],
    "wiley-x-tide-for-eclipse-xt-med-lg":                [WX],
    "wiley-x-tide-med-lg":                               [WX],
    "wiley-x-twisted-for-eclipse-xt-med-lg":             [WX],
    "wiley-x-twisted-med-lg":                            [WX],
    "wiley-x-valor-for-eclipse-xt-med-lg":               [WX],
    "wiley-x-xl-1-advanced-for-eclipse-xt-sm-med":       [WX],
    # Brands > 7Eye
    "7eye-aspen-for-eclipse-xt-sm-med":                  [SE],
    "7eye-aspen-sm-med":                                 [SE],
    "7eye-bali-for-eclipse-xt-sm-med":                   [SE],
    "7eye-bali-sm-med":                                  [SE],
    "7eye-bora-for-eclipse-xt-med-lg":                   [SE],
    "7eye-bora-med-lg":                                  [SE],
    "7eye-briza-for-eclipse-xt-sm-med":                  [SE],
    "7eye-briza-sm-med":                                 [SE],
    "7eye-cape-for-eclipse-xt-med-lg":                   [SE],
    "7eye-cape-med-lg":                                  [SE],
    "7eye-chubasco-for-eclipse-xt-sm-med":               [SE],
    "7eye-chubasco-sm-med":                              [SE],
    "7eye-churada-for-eclipse-xt-sm-med":                [SE],
    "7eye-churada-sm-med":                               [SE],
    "7eye-cyclone-med-lg":                               [SE],
    "7eye-derby-for-eclipse-xt-med-lg":                  [SE],
    "7eye-derby-med-lg":                                 [SE],
    "7eye-diablo-for-eclipse-xt-sm-med":                 [SE],
    "7eye-diablo-sm-med":                                [SE],
    "7eye-notus-for-eclipse-xt-lg-xlg":                  [SE],
    "7eye-oasis-med-lg":                                 [SE],
    "7eye-panhead-for-eclipse-xt-med-xl":                [SE],
    "7eye-panhead-med-xl":                               [SE],
    "7eye-raptor-for-eclipse-xt-med-lg":                 [SE],
    "7eye-raptor-med-lg":                                [SE],
    "7eye-sedona-for-eclipse-xt-xs-med":                 [SE],
    "7eye-sedona-sm-med":                                [SE],
    "7eye-sierra-for-eclipse-xt-sm-med":                 [SE],
    "7eye-sierra-xsm-sm":                                [SE],
    "7eye-taku-plus-for-eclipse-xt-lg-xl":               [SE],
    "7eye-taku-plus-lg-xlg":                             [SE],
    "7eye-ventus-for-eclipse-xt-sm-lg":                  [SE],
    "7eye-ventus-sm-med":                                [SE],
    "7eye-viento-for-eclipse-xt-xs-med":                 [SE],
    "7eye-viento-xs-sm":                                 [SE],
    "7eye-warrior-for-eclipse-xt-med-lg":                [SE],
    "7eye-whirlwind-for-eclipse-xt-med-lg":              [SE],
    "7eye-whirlwind-med-lg":                             [SE],
    # Sunglasses > Sport
    "airspeed":                                          [SPT],
    "aruba":                                             [SPT],
    "atlas":                                             [SPT],
    "backspin-sport-sunglasses":                         [SPT],
    "bullseye":                                          [SPT],
    "chopper-901-fits-sm-lg":                            [SPT],
    "conquest":                                          [SPT],
    "convair-fits-lg-xlg":                               [SPT],
    "coupe-sm-med":                                      [SPT],
    "daisy":                                             [SPT],
    "eliminator":                                        [SPT],
    "equator":                                           [SPT],
    "everest":                                           [SPT],
    "fareway":                                           [SPT],
    "hairpin-sm-med":                                    [SPT],
    "hangar":                                            [SPT],
    "hemi":                                              [SPT],
    "hollywood":                                         [SPT],
    "horizon":                                           [SPT],
    "jupiter":                                           [SPT],
    "locs-amigo-9003":                                   [SPT],
    "locs-bario-9083":                                   [SPT],
    "locs-bel-air-91149":                                [SPT],
    "locs-camino-91185":                                 [SPT],
    "locs-cruiser-91055":                                [SPT],
    "locs-del-ray-91102":                                [SPT],
    "locs-deville-91026":                                [SPT],
    "locs-fleetwood-91182":                              [SPT],
    "locs-hombre-9035":                                  [SPT],
    "locs-mark-v-91180":                                 [SPT],
    "locs-monte-carlo-9058":                             [SPT],
    "locs-san-diego-91111":                              [SPT],
    "locs-showtime-91148":                               [SPT],
    "locs-tuner-91045":                                  [SPT],
    "locs-voodoo-91160":                                 [SPT],
    "madeline":                                          [SPT],
    "nitrous":                                           [SPT],
    "omega":                                             [SPT],
    "panther":                                           [SPT],
    "pegasus":                                           [SPT],
    "phantom-med-lg":                                    [SPT],
    "redline-med-lg":                                    [SPT],
    "reflex":                                            [SPT],
    "road-gator":                                        [SPT],
    "rusty-big-tall-sunglasses":                         [SPT],
    "samurai-sport-mirror-sunglasses":                   [SPT],
    "savannah-med-lg":                                   [SPT],
    "sly":                                               [SPT],
    "sonic":                                             [SPT],
    "spear-lg-xlg":                                      [SPT],
    "spinner":                                           [SPT],
    "storm":                                             [SPT],
    "targa":                                             [SPT],
    "topspin-sport-sunglasses":                          [SPT],
    "torpedo":                                           [SPT],
    "traffic":                                           [SPT],
    "trans-am":                                          [SPT],
    "us-route-40":                                       [SPT],
    "vato":                                              [SPT],
    "x-loop-3303-bogey":                                 [SPT],
    "x-loop-3304-fender":                                [SPT],
    "x-loop-3319-club":                                  [SPT],
    "x-loop-3320-sprint":                                [SPT],
    "x-loop-3322-infield":                               [SPT],
    # Sunglasses > Polarized only
    "aero-polarized-wrap-sport-sunglasses":              [POL],
    "apex-polarized":                                    [POL],
    "apex-polarized-rose":                               [POL],
    "ares-polarized-wrap-sport-sunglasses":              [POL],
    "bombora-polarized-float-sunglasses":                [POL],
    "brooklyn-polarized-one-size-fits-all":              [POL],
    "carina-polarized":                                  [POL],
    "coral-ii-polarized-sunglasses":                     [POL],
    "equinox-polarized-sunglasses":                      [POL],
    "everest-polarized-sunglasses":                      [POL],
    "gazelle-polarized-fits-all-heads":                  [POL],
    "gremlin-polarized-sunglasses":                      [POL],
    "jupiter-polarized":                                 [POL],
    "maverick-polarized":                                [POL],
    "panama-polarized-sunglasses":                       [POL],
    "pike-polarized-sunglasses":                         [POL],
    "sahara-dark-polarized":                             [POL],
    "sahara-polarized":                                  [POL],
    "serengeti-polarized-fits-med-large-heads":          [POL],
    "skyline-polarized":                                 [POL],
    "stinger-polarized":                                 [POL],
    "turk-polarized":                                    [POL],
    # Polarized + HD Lens
    "formula1-hd-copper-polarized-sunglasses":           [POL, HD],
    # Sunglasses > HD Lens only
    "cartel":                                            [HD],
    "eagle-eye":                                         [HD],
    "falcon":                                            [HD],
    "navigator":                                         [HD],
    # HD Lens + Bifocals > Standard
    "eliminator-copper-hd-bifocal-fits-medium-large-heads": [HD, BST],
    # Sunglasses > Night only
    "flite":                                             [NGT],
    "freeway":                                           [NGT],
    "metric":                                            [NGT],
    "phoenix-w-yellow-lens-wrap-sunglasses":             [NGT],
    "spitzer":                                           [NGT],
    "trooper":                                           [NGT],
    "vortex":                                            [NGT],
    # Night + Bifocals > Standard
    "eliminator-night-vision-bifocal-fits-medium-large-heads": [NGT, BST],
    # Bifocals > Standard only
    "blade-bifocal-fits-medium-xlarge-heads":            [BST],
    "cabana-bifocal-one-size-fits-all":                  [BST],
    "cabriolet-mirror-bifocal-one-size-fits-all":        [BST],
    "cadet-bifocal-sunglasses-fits-medium-large-heads":  [BST],
    "cleo-ladies-bifocal-sunglasses-one-size-fits-all":  [BST],
    "cognac-bifocal-sunglasses-one-size-fits-all":       [BST],
    "cooper-bifocal-fits-medium-xlarge-heads":           [BST],
    "dolphin-wrap-bifocal-sunglasses-fits-up-to-large-heads": [BST],
    "first-lady-bifocal-fits-medium-large-heads":        [BST],
    "garnet-gradient-bifocal-fits-medium-large-heads":   [BST],
    "geneva-oversized-women-bifocal":                    [BST],
    "glider-bifocal-aviator-sunglasses-fits-medium-xlarge-heads": [BST],
    "glider-bifocal-fits-small-medium-heads":            [BST],
    "gullwing-bifocal-fits-medium-large-heads":          [BST],
    "hawkeye-bifocal-fits-medium-xlarge-heads":          [BST],
    "hawkeye-hd-bifocal-fits-medium-xlarge-heads":       [BST],
    "katy-women-bifocal":                                [BST],
    "liverpool-smoke-fits-small-large-heads":            [BST],
    "marigold-bifocal-sunglasses-one-size-fits-all":     [BST],
    "methane-bifocal-fits-small-medium-heads":           [BST],
    "metre-bifocal-fits-medium-xlarge-heads":            [BST],
    "pacific-mirror-bifocal":                            [BST],
    "pheaton-bifocal-fits-small-medium-heads":           [BST],
    "puma-bifocal-fits-small-medium-heads":              [BST],
    "renegade-bifocal-fits-medium-xlarge-heads":         [BST],
    "spike-bifocal-fits-small-medium-heads":             [BST],
    "tailpipe-bifocal-fits-medium-xlarge-heads":         [BST],
    "venice-womens-bifocal-sunglasses":                  [BST],
    "wallstreet-bifocal-sunglasses-fits-medium-xlarge-heads": [BST],
    # Bifocals > Polarized
    "artemis-sport-polarized-bifocal":                   [BPL],
    "cobalt-polarized-bifocal-fits-medium-xlarge-heads": [BPL],
    "colorado-polarized-bifocal-fits-medium-xlarge-heads": [BPL],
    "commando-polarized-bifocal-fits-medium-xlarge-heads": [BPL],
    "cooper-polarized-bifocal-fits-med-xlarge-heads":    [BPL],
    "eliminator-polarized-bifocal-fits-medium-large-heads": [BPL],
    "karma-polarized-bifocal-fits-medium-largeheads":    [BPL],
    "kumatage-polarized-bifocal-fits-medium-xlarge-heads": [BPL],
    "orchid-lady-polarized-bifocal-one-size-fits-all":   [BPL],
    "overdrive-polarized-bifocal-fits-medium-xlarge-heads": [BPL],
    "pheaton-polarized-bifocal-fits-medium-xlarge-heads": [BPL],
    "sharkbait-polarized-bifocal-fits-medium-xlarge-heads": [BPL],
    "sturgeon-sport-polarized-bifocal":                  [BPL],
    "talon-polarized-bifocal-fits-medium-xlarge-heads":  [BPL],
    # Bifocals > Foam
    "airfoil-bifocal-with-foam-cushionfits-large-xlarge-heads": [BFM],
    "airstrike-bifocal-goggles-fits-up-to-large-heads":  [BFM],
    "apollo-safety-wrap-bifocal-sunglasses-fits-medium-large-heads": [BFM],
    "new-horsepower-bifocal-with-foam-cushion-fits-medium-xlarge-heads": [BFM],
    "quake-bifocal-with-foam-cushion-fits-small-medium-heads": [BFM],
    "xcalibre-z87-safety-bifocal-w-foam-cushion-fits-med-lg-heads": [BFM],
    "zorst-bifocal-with-non-slip-rubber-seal-fits-large-xlarge-heads": [BFM],
    # Readers > Sunglass
    "cole-sunglass-reader":                              [RSG],
    "jersey-sunglass-reader":                            [RSG],
    "monaco-reader-med-xlg":                             [RSG],
    "regal-full-lens-sunglass-reader-2-pairs":           [RSG],
    "rocket-wrap-reading-sunglasses":                    [RSG],
    "runway-aviator-sunglass-reader":                    [RSG],
    "verbena-sunglass-reader":                           [RSG],
    "voyager-reading-sunglasses":                        [RSG],
    "wave-mirror-reader":                                [RSG],
    # Readers > Clear
    "carraway-reader-one-size-fits-all":                 [RCL],
    "clutch-reader-med-xlg":                             [RCL],
    "dorothy-reader":                                    [RCL],
    "elite-clear-lens-reader":                           [RCL],
    "garnet-gradient-reader-fits-sm-lg-heads":           [RCL],
    "gypsy-reader":                                      [RCL],
    "holiday-reader":                                    [RCL],
    "kitty-reader":                                      [RCL],
    "liverpool-reader-one-size-fits-all":                [RCL],
    "loft-reader":                                       [RCL],
    "methane-full-lens-readers-fits-small-med-heads":    [RCL],
    "newport-reader-one-size-fits-all":                  [RCL],
    "onyx-reader":                                       [RCL],
    "sonoma-reader":                                     [RCL],
    "studebaker-full-lens-reader":                       [RCL],
    "trek-goggle-full-lens-reader":                      [RCL],
    # Readers > Computer
    "cabot-photochromic-computer-reader":                [RCP],
    "edison-photochromic-computer-reader":               [RCP],
    "goose-aviator-computer-reader":                     [RCP],
    "gunner-wrap-yellow-computer-glasses":               [RCP],
    "kennedy-computer-reader":                           [RCP],
    "magellan-computer-reader":                          [RCP],
    "orion-computer-reader":                             [RCP],
    "sapphire-computer-reading-glasses":                 [RCP],
    "vasari-computer-reading-glasses":                   [RCP],
    "vespa-computer-reader":                             [RCP],
    "zane-computer-reading-glasses":                     [RCP],
    # Readers > Multifocal
    "bombay-multifocal-reader":                          [RMF],
    "georgetown-multifocal-reader":                      [RMF],
    "hailey-multifocal-reader":                          [RMF],
    "kennedy-multifocal-reader":                         [RMF],
    "pixel-multifocal-reader":                           [RMF],
    "professor-multifocal-reader":                       [RMF],
    "spy-multifocal-reader":                             [RMF],
    "studio-multifocal-reader":                          [RMF],
    # Cases & Accessories
    "2-pack-bandannas-you-get-2-pieces-of-color-you-choose-black-hot-pink-red-navy-blue-royal-blue-w-yellow-lens-in-stock": [CAS],
    "agate-lady-black-extra-large-leather-case":         [CAS],
    "ametrine-medium-leather-hard-case":                 [CAS],
    "biker-armour-microfiber-cleaning-case":             [CAS],
    "citrine-woody-hard-case":                           [CAS],
    "garnet-deep-zipper-case-with-clipper":              [CAS],
    "hematite-small-shiny-leather-case":                 [CAS],
    "jade-deep-fabric-case":                             [CAS],
    "leopard-print-hard-case":                           [CAS],
    "pm-25-medical-face-masks-pack-of-three":            [CAS],
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
