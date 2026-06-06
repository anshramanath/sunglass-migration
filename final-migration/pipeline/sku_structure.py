import re

def check_sku(sku: str) -> bool:
    chunk = sku.split("-")[0]
    return bool(re.search(r'\d+[Xx]\d+', chunk))

def get_structure(sku: str) -> str | None:
    chunk = sku.split("-")[0]
    m = re.search(r'\d+[Xx]\d+', chunk)
    return m.group(0).upper() if m else None
