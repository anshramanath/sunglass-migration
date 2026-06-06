import re

def check_sku(sku: str) -> bool:
    chunk = sku.split("-")[0]
    return bool(re.search(r'\d+[Xx]\d+', chunk))
