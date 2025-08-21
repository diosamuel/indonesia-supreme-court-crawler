import re, hashlib
import datetime
def make_hash_id(text):
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
    return hashlib.sha256(cleaned.encode('utf-8')).hexdigest()

from datetime import datetime
mapperDate = {
    "januari": "january",
    "februari": "february",
    "maret": "march",
    "april": "april",
    "mei": "may",
    "juni": "june",
    "juli": "july",
    "agustus": "august",
    "september": "september",
    "oktober": "october",
    "nopember": "november",
    "desember": "december"
}

def convert_to_ymd(date_str):
    parts = date_str.strip().lower().split()
    if len(parts) != 3:
        return None
    day, month_id, year = parts
    month_en = mapperDate.get(month_id)
    if not month_en:
        return None
    date_en = f"{day} {month_en} {year}"
    dt = datetime.strptime(date_en, "%d %B %Y")
    return dt.strftime("%Y-%m-%d")

def safe_date(date_str):
    DEFAULT_DATE = datetime.date(1970, 1, 1)
    if not date_str:
        return DEFAULT_DATE
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return DEFAULT_DATE

def safe_str(val):
    return val if (val is not None and isinstance(val, str)) else ''