import json
import urllib.request
from pathlib import Path
from mcp.server.fastmcp import FastMCP, Image

BASE = Path(__file__).parent

mcp = FastMCP("bikershades-migration")

BRAND_CONTEXT = {
    "prosport": {
        "name": "proSPORT Sunglasses",
        "about": "An affordable sport and outdoor eyewear brand. Products include wrap sunglasses, polarized sunglasses, readers, bifocals, night vision glasses, and hard cases.",
        "customer": "active adults, outdoor enthusiasts, and drivers",
        "tone": "Practical and feature-focused. Conversational but informative. Highlight the specific lens technology and what it does for the wearer.",
        "description_style": "2–3 sentences. Name the product, describe its look and key feature, then mention its best use case. Do not include measurements.",
        "summary_style": "4–6 short bullet strings. Each covers one distinct feature: UV protection, lens type, frame material, comfort feature, or included accessories. Capitalize the first word, no period.",
        "key_concepts": [
            "100% UV400 protection",
            "Polarized lenses reduce glare",
            "HD copper lenses enhance contrast in bright conditions",
            "Yellow/night vision lenses improve visibility in low light or overcast",
            "Bifocal readers have magnification power options",
            "Polycarbonate lenses are shatter-resistant",
            "Spring hinges for a flexible, comfortable fit",
            "Includes microfiber drawstring case",
        ],
        "examples": [
            {
                "name": "proSPORT Road Gator Sport Sunglasses",
                "description": "The Road Gator is ANSI Z87.1 rated with a superior wrap frame that protects your eyes from all angles. Ideal for motorcycle riding, night driving, and working in hazardous conditions.",
                "summary": ["Ultra wrap ANSI Z87.1 rated frames and lenses", "100% UV protection", "Choose from Yellow or Clear lenses", "Durable polycarbonate frames", "Lightweight and comfortable", "Fits small to large heads"],
            },
            {
                "name": "proSPORT Mercury Polarized Mirror Sunglasses",
                "description": "The Mercury features retro square mirrored lenses that seem to float in the frame — a bold, military-inspired look with serious polarized protection. Perfect for bright outdoor days when glare is a real issue.",
                "summary": ["100% UV protection", "Polarized polycarbonate lenses", "Floating nosepieces for enhanced comfort", "Flexible spring hinge temples", "Durable nickel silver frames", "Includes free microfiber drawstring case"],
            },
        ],
    },
    "monster": {
        "name": "Sunglass Monster",
        "about": "A fashion-forward lifestyle eyewear retailer. Products include fashion sunglasses, polarized styles, readers, bifocals, retro frames, and kids eyewear. Also carries Locs and X-Loop.",
        "customer": "style-conscious shoppers looking for trendy, affordable eyewear",
        "tone": "Stylish and accessible. Lead with the product's personality and look, then back it up with practical specs. Warmer tone than proSPORT.",
        "description_style": "2–3 sentences. Introduce the product by name, describe its style and standout visual feature, then mention its practical benefit or who it suits best.",
        "summary_style": "4–6 short bullet strings covering style, lens type, UV protection, frame feature, and accessories. Capitalize the first word, no period.",
        "key_concepts": [
            "100% UV protection",
            "Polarized lenses reduce glare",
            "Retro and vintage-inspired styles",
            "Bold or oversized frames for fashion impact",
            "Lightweight frames for all-day wear",
            "Reader and bifocal magnification powers available",
            "Includes microfiber cleaning case",
        ],
        "examples": [
            {
                "name": "Locs Camino 91185",
                "description": "The Camino brings authentic Locs streetwear attitude in a wrap-around frame built for medium to XLarge heads. Super dark lenses keep eyes concealed while the bold silhouette demands attention.",
                "summary": ["Authentic Locs sunglasses with bold streetwear style", "Super dark lenses for maximum eye concealment", "Full wraparound frame for maximum sun and wind protection", "100% UV protection", "Includes a microfiber cleaning case"],
            },
        ],
    },
    "bikershades": {
        "name": "BikerShades",
        "about": "A specialty motorcycle eyewear store. Products include foam-sealed goggles, cover-overs (fit over prescription glasses), bifocal riding glasses, photochromic styles, and clear/yellow/HD lens options. Carries BikerArmour house brand plus Wiley X and 7Eye.",
        "customer": "motorcyclists and bikers who need reliable, protective eye coverage while riding",
        "tone": "Practical and safety-focused, written for riders. Lead with protection and fit, then lens options. Mention riding conditions where relevant (night, fog, bright sun, all-day).",
        "description_style": "2–3 sentences. State the product name and fit range, describe the protection it offers (foam seal, wrap, cover-over), then mention lens options and riding conditions it suits. Do not include measurements.",
        "summary_style": "4–6 short bullet strings covering: foam seal or frame type, lens options and their purpose, UV/safety rating, head size fit range, and included case. Capitalize the first word, no period.",
        "key_concepts": [
            "Foam seal blocks wind, debris, dust, and pollen — critical for open-face riding",
            "Cover-over styles fit over prescription glasses",
            "Clear lenses: ideal for night riding or overcast conditions",
            "Yellow lenses: enhance contrast in fog, rain, or low light",
            "HD copper lenses: boost contrast and depth in bright sunlight",
            "Polarized lenses: cut glare on water and wet roads",
            "Photochromic (Eclipse) lenses auto-darken outdoors and clear indoors",
            "Bifocal power options for riders who need reading assistance",
            "Size ranges like [SM-MED], [MED-LG], [LG-XLG] refer to head circumference fit, not frame size",
            "Z87.1 means ANSI-rated impact resistance",
            "Includes BikerShades hard case and microfiber cleaning case",
        ],
        "examples": [
            {
                "name": "BikerArmour Enduro [MED - LG]",
                "description": "The BikerArmour Enduro is a foam-sealed motorcycle goggle built for medium to large heads. The foam cushion blocks wind, dust, and debris, making it a solid choice for long rides in all conditions. Available in clear and yellow lens options to suit night riding or overcast days.",
                "summary": ["Foam seal blocks wind, dust, and debris", "Available in Clear and Yellow lens options", "100% UV protection", "Fits medium to large heads", "Includes BikerShades hard case and microfiber cleaning case"],
            },
            {
                "name": "Wiley X Hudson for Eclipse XT [MED - LG]",
                "description": "The Wiley X Hudson with Eclipse XT features genuine Transitions XtrActive photochromic lenses that darken automatically outdoors and return to clear inside — no swapping lenses mid-ride. Built to ANSI Z87.1 safety standards and sized for medium to large heads.",
                "summary": ["Genuine Transitions XtrActive photochromic lenses", "Shatter-resistant polycarbonate lenses", "100% UVA/UVB protection", "Meets ANSI Z87.1 safety standards", "Fits medium to large heads", "Includes Wiley X hard case and microfiber cleaning case"],
            },
        ],
    },
}


def data_path(brand: str) -> Path:
    return BASE / "data" / brand / "generate-content" / "items.json"


def load_items(brand: str) -> list:
    path = data_path(brand)
    if not path.exists():
        raise FileNotFoundError(f"Run init_generate_content.py for {brand} first.")
    return json.loads(path.read_text())


def save_items(brand: str, items: list) -> None:
    data_path(brand).write_text(json.dumps(items, indent=2, ensure_ascii=False))


def find_next(items: list) -> dict | None:
    for item in items:
        if item.get("description") is None or not item.get("summary"):
            return item
    return None


def fetch_image(url: str) -> Image | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            mime = resp.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
            fmt  = mime.split("/")[-1]  # "image/jpeg" -> "jpeg"
            return Image(data=data, format=fmt)
    except Exception:
        return None


@mcp.tool()
def get_progress(brand: str) -> str:
    """Returns how many items still need content generated for a brand (prosport, monster, bikershades)."""
    items     = load_items(brand)
    remaining = sum(1 for i in items if i.get("description") is None or not i.get("summary"))
    total     = sum(1 for i in items if i["wasMissingDescription"] or i["wasMissingSummary"])
    done      = total - remaining
    return json.dumps({"brand": brand, "remaining": remaining, "done": done, "total": total})


@mcp.tool()
def save_content(brand: str, slug: str, description: str = "", summary: list[str] = []) -> str:
    """
    Saves generated description and/or summary for a product.
    Only pass fields that were generated — do not pass fields the product already had.
    """
    items = load_items(brand)
    for i, item in enumerate(items):
        if item["slug"] == slug:
            if description:
                items[i]["description"] = description
            if summary:
                items[i]["summary"] = summary
            save_items(brand, items)
            remaining = sum(1 for x in items if x.get("description") is None or not x.get("summary"))
            return f"Saved '{item['name']}'. {remaining} items remaining for {brand}."
    return f"ERROR: slug '{slug}' not found in {brand}."


@mcp.tool()
def get_next_product(brand: str) -> list:
    """
    Returns the next product needing description or summary, with full context and instructions.
    Call this, analyze the product image, generate content, then call save_content.
    """
    items   = load_items(brand)
    product = find_next(items)
    ctx     = BRAND_CONTEXT[brand]

    if product is None:
        return f"All done! No more items need content for {brand}."

    need_desc = product.get("description") is None
    need_sum  = not product.get("summary")
    image_url = (product.get("productImages") or [{}])[0].get("src", "")

    attrs = product.get("attributes", [])
    attr_text = "\n".join(
        f"  {a['name'].capitalize()}: {', '.join(a['options'])}"
        for a in attrs if a.get("options")
    ) or "  (none)"

    price = f"${(product.get('minPriceCents') or 0) / 100:.2f}"
    if product.get("maxPriceCents") and product["maxPriceCents"] != product.get("minPriceCents"):
        price += f" – ${product['maxPriceCents'] / 100:.2f}"

    examples_text = "\n\n".join(
        f"Name: {e['name']}\nDescription: {e['description']}\nSummary: {json.dumps(e['summary'])}"
        for e in ctx["examples"]
    )

    fields_needed = []
    if need_desc:
        fields_needed.append(f"description ({ctx['description_style']})")
    if need_sum:
        fields_needed.append(f"summary ({ctx['summary_style']})")

    text = f"""=== PRODUCT CONTENT GENERATION TASK ===

STORE: {ctx['name']}
ABOUT: {ctx['about']}
CUSTOMER: {ctx['customer']}
TONE: {ctx['tone']}

--- PRODUCT ---
Name:  {product['name']}
Slug:  {product['slug']}
Price: {price}
Attributes:
{attr_text}
{"Existing description: " + product['description'] if product.get('description') else ""}
{"Existing summary: " + json.dumps(product['summary']) if product.get('summary') else ""}

--- PRODUCT IMAGE ---
{"The product image is attached above. Use what you see — frame shape, lens color, foam seal, style — to inform the content." if image_url else "(no image available — infer from name and attributes)"}

--- GENERATE ---
You need to write: {" AND ".join(fields_needed)}

Key concepts for this brand:
{chr(10).join("• " + k for k in ctx['key_concepts'])}

--- EXAMPLES FROM THIS BRAND ---
{examples_text}

--- INSTRUCTIONS ---
1. Study the product image carefully.
2. Write content that matches the tone and style of the examples above.
3. Do not invent specs not visible in the image or implied by the name/attributes.
4. Plain text only — no markdown, no HTML.
5. Call save_content with:
   - brand="{brand}"
   - slug="{product['slug']}"
   {"- description: your generated description" if need_desc else ""}
   {"- summary: your generated summary array" if need_sum else ""}
"""

    result = [text]
    if image_url:
        img = fetch_image(image_url)
        if img:
            result.append(img)

    return result


if __name__ == "__main__":
    mcp.run()
