from pathlib import Path
from dotenv import load_dotenv
import os

BASE = Path(__file__).parent.parent  # new-migration/
load_dotenv(dotenv_path=BASE.parent / ".env")

BRAND_CONFIG = {
    "prosport": {
        "slug": "prosport",
        "brand_name": "proSPORT Sunglasses",
        "base_url": "PROSPORT_BASE_URL",
        "consumer_key": "PROSPORT_CONSUMER_KEY",
        "consumer_secret": "PROSPORT_CONSUMER_SECRET",
    },
    "monster": {
        "slug": "monster",
        "brand_name": "Sunglass Monster",
        "base_url": "MONSTER_BASE_URL",
        "consumer_key": "MONSTER_CONSUMER_KEY",
        "consumer_secret": "MONSTER_CONSUMER_SECRET",
    },
}

def load_brand():
    key = os.getenv("BRAND")
    config = BRAND_CONFIG.get(key)
    if not config:
        raise SystemExit(f"Unknown BRAND={key!r}. Add it to BRAND_CONFIG.")
    return key, config
