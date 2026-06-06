from pathlib import Path
from dotenv import load_dotenv
import os

BASE = Path(__file__).parent.parent  # final-migration/
load_dotenv(dotenv_path=BASE.parent / ".env")

VEEQO_KEY = os.getenv("VEEQO_KEY")

BRAND_CONFIG = {
    "prosport": {
        "slug": "prosport",
        "brand_name": "proSPORT Sunglasses",
        "base_url": "https://prosportsunglasses.com",
        "consumer_key": "PROSPORT_CONSUMER_KEY",
        "consumer_secret": "PROSPORT_CONSUMER_SECRET",
    },
    "monster": {
        "slug": "monster",
        "brand_name": "Sunglass Monster",
        "base_url": "https://www.sunglassmonster.com",
        "consumer_key": "MONSTER_CONSUMER_KEY",
        "consumer_secret": "MONSTER_CONSUMER_SECRET",
    },
    "bikershades": {
        "slug": "bikershades",
        "brand_name": "BikerShades",
        "base_url": "https://bikershades.com",
        "consumer_key": "BIKERSHADES_CONSUMER_KEY",
        "consumer_secret": "BIKERSHADES_CONSUMER_SECRET",
    },
}

def load_brand():
    key = os.getenv("BRAND")
    config = BRAND_CONFIG.get(key)
    if not config:
        raise SystemExit(f"Unknown BRAND={key!r}. Add it to BRAND_CONFIG.")
    return key, config
