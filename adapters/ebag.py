import time
import requests

BASE_URL = "https://www.ebag.bg/en/categories/{cat_id}/products/json"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}
RATE_LIMIT_SECONDS = 0.5


def fetch_category(cat_id):
    url = BASE_URL.format(cat_id=cat_id)
    all_results = []
    page_number = 1
    max_retries = 3

    while url:
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(url, headers=HEADERS, timeout=10)
                response.raise_for_status()
                data = response.json()
                break
            except requests.exceptions.RequestException as e:
                print(f"  [ebag] category {cat_id} - page {page_number} - attempt {attempt} failed: {e}")
                if attempt == max_retries:
                    print(f"  [ebag] category {cat_id} - page {page_number} - giving up after {max_retries} attempts")
                    raise
                time.sleep(2 * attempt)

        all_results.extend(data["results"])
        print(f"  [ebag] category {cat_id} - page {page_number} - {len(all_results)} items so far")

        url = data["next"]
        page_number += 1

        if url:
            time.sleep(RATE_LIMIT_SECONDS)

    return all_results


def normalize(raw_item):
    prices = raw_item.get("prices_data_per_currency", {})
    preferred_currency = "EUR" if "EUR" in prices else next(iter(prices), "EUR")

    if preferred_currency == "EUR":
        price_value = float(raw_item["current_price_eur"])
    else:
        price_value = float(raw_item["current_price"])

    return {
        "source_id": str(raw_item["id"]),
        "name": raw_item["name_en"] or raw_item["name"],
        "brand": raw_item["brand"]["name_en"] if raw_item["brand"] else None,
        "category_id": str(raw_item["main_category_id"]),
        "unit_weight_text": raw_item["unit_weight_text"],
        "price": price_value,
        "currency": preferred_currency,
        "was_promo": raw_item["price_promo"] is not None,
        "discount_percent": raw_item["discount_percent"],
    }


def fetch_and_normalize_category(cat_id):
    raw_items = fetch_category(cat_id)
    return [normalize(item) for item in raw_items]