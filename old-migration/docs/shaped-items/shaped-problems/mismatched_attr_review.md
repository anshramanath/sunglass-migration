# Mismatched Attributes Review
_Last updated: 2026-05-31_

**Source:** `migration/reshaped/mismatched_attr_items.json`

These products have one or more variations whose attribute slugs don't exist in the product's attribute terms. The variation references a color or power value that was never defined at the product level — added directly to the variation in WooCommerce without updating the product's attribute list, or the attribute term was later deleted from the product but the variation was left behind.

**Why it matters:** Every color button shown on the frontend is derived from `product.attributes`. If a variation uses a slug not in product attributes, clicking any button can never reach that variation — it's unreachable.

**Fix needed:** For each orphaned slug, owner either:
1. Confirms the display name → we add the term to product attributes and the variation becomes reachable
2. Confirms the variation should be dropped → remove it

**Note:** We only have the slug, not the display name — we can't auto-recover without owner input.

---

## Product List

| SKU | Name | Orphaned slug(s) | Affected variations |
|-----|------|-----------------|--------------------:|
| `BF4X37GV-0` | Geneva Oversized Women Bifocal | `tortoise-green-gradient-smoke`, `tortoise-white-gradient-smoke` | 8 |
| `PR29X57BB-0` | Bombay Multifocal Reader | `3.50` (power not in product terms) | 4 |
| `FM63X18VL-0` | BikerArmour Valor [MED – XLG] | `black-gray-mirror-silver`, `black-orange-mirror-green` | 2 |
| `CRE69X81EL-0` | Elite Clear Lens Reader | `black-blue-2` | 9 |
| `FM85X11MNM-0-YL` | Magnum – w/ Yellow Lens | `black-mirror-blue`, `blue-clear-to-gray`, `blue-yellow-to-brown` | 3 |
| `FM85X11MNM-0-SM` | BikerArmour Magnum [MED – LG] | `black-mirror-blue`, `blue-clear-to-gray`, `blue-yellow-to-brown` | 3 |
| `FM20X02CO-0-HD` | Cobra – HD | `black-polarized-smoke` | 1 |
| `FM20X02CO-0-YL` | Cobra – w/ Yellow Lens | `black-polarized-smoke` | 1 |
| `FM20X02CO-0-CL` | Cobra – Clear | `black-polarized-smoke` | 1 |
| `FM25X88MNRS-0-YL` | Angel Rhinestones for Ladies – w/ Yellow Lens | `red-clear`, `red-smoke`, `red-yellow` | 3 |
| `FM25X88MNRS-0-CL` | Angel Rhinestones for Ladies – Clear | `red-clear`, `red-smoke`, `red-yellow` | 3 |
| `FM25X88MNRS-0-SM` | BikerArmour Angel with Rhinestone [MED – LG] | `red-clear`, `red-smoke`, `red-yellow` | 3 |
| `FM85X11MNA-0-YL` | Angel for Ladies – Yellow Lens | `red-clear-to-gray`, `red-yellow-to-brown` | 2 |
| `FM85X11MNA-0-HD` | Angel for Ladies – HD | `red-clear-to-gray`, `red-yellow-to-brown` | 2 |
| `FM85X11MNA-0-CL` | Angel for Ladies – Clear | `red-clear-to-gray`, `red-yellow-to-brown` | 2 |
| `FM85X11MNA-0-SM` | BikerArmour Angel [MED – LG] | `red-yellow-to-brown` | 1 |
| `FM0X76AB-0-XT` | BikerArmour Air Boss for Eclipse XT [MED – LG] | `clear-to-green-w-anti-reflective-coat`, `clear-to-green` | 2 |
| `LO91055-0` | Locs Cruiser 91055 | `glossy-black-smoke` | 1 |
| `SP60X29US-0` | US Route 40 | `tortoise-yellow` | 1 |
| `SP02X15EG-0` | Eagle Eye | `tortoise-hd` | 1 |
| `CA250X06CQ-0` | Conquest | `gold-mirror-gold` | 1 |
| `BF4X19HW-SM-0` | Hawkeye Bifocal [Fits MEDIUM – XLARGE Heads] | `black-yellow-smoke` | 4 |

---

## Patterns

**Same slug across a product family (most fixable):**
- Cobra family (`FM20X02CO-*`): all share `black-polarized-smoke` — likely one color added to variations but not the product list
- Angel Rhinestones family (`FM25X88MNRS-*`): all share `red-clear`, `red-smoke`, `red-yellow`
- Angel for Ladies family (`FM85X11MNA-*`): all share `red-clear-to-gray`, `red-yellow-to-brown`
- Magnum family (`FM85X11MNM-*`): all share `black-mirror-blue`, `blue-clear-to-gray`, `blue-yellow-to-brown`

**Power value out of range:**
- `PR29X57BB-0`: product defines powers up to `3.00` but variation uses `3.50` — product's power list needs extending

**Slug typo/duplicate:**
- `CRE69X81EL-0`: uses `black-blue-2` while product has `black-blue` — likely a WooCommerce duplicate created by accident
- `SP72X90RL-0`, `SP88X75SP-0`: similar `-2` suffix pattern

---

## Blocker

Owner needs to confirm for each orphaned slug:
- The correct display name (so we can add it to product attributes), OR
- That the variation should be dropped
