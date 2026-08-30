import time
import requests

BASE_URL = "https://www.ebag.bg/en/categories/{cat_id}/products/json"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}
RATE_LIMIT_SECONDS = 1


def fetch_category(cat_id):
    url = BASE_URL.format(cat_id=cat_id)
    all_results = []

    while url:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        all_results.extend(data["results"])
        url = data["next"]

        if url:
            time.sleep(RATE_LIMIT_SECONDS)

    return all_results


def normalize(raw_item):
    return {
        "source_id": str(raw_item["id"]),
        "name": raw_item["name_en"] or raw_item["name"],
        "brand": raw_item["brand"]["name_en"] if raw_item["brand"] else None,
        "category_id": str(raw_item["main_category_id"]),
        "unit_weight_text": raw_item["unit_weight_text"],
        "price": float(raw_item["current_price"]),
        "currency": "BGN",
        "was_promo": raw_item["price_promo"] is not None,
        "discount_percent": raw_item["discount_percent"],
    }


def fetch_and_normalize_category(cat_id):
    raw_items = fetch_category(cat_id)
    return [normalize(item) for item in raw_items]