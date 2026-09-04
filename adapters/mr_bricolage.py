
import time
import requests

BASE_URL = "https://api.mr-bricolage.bg/occ/v2/bricolage-spa/categories/{cat_id}/products/all"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}
RATE_LIMIT_SECONDS = 0.5


def fetch_category(cat_id):
    all_results = []
    current_page = 0
    total_pages = 1
    max_retries = 3

    while current_page < total_pages:
        params = {
            "fields": "FULL",
            "pageSize": 30,
            "sort": "relevance",
            "query": "",
            "lang": "bg",
            "curr": "EUR",
            "currentPage": current_page,
        }
        url = BASE_URL.format(cat_id=cat_id)

        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(url, headers=HEADERS, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                break
            except requests.exceptions.RequestException as e:
                print(f"  [mr_bricolage] category {cat_id} - page {current_page} - attempt {attempt} failed: {e}")
                if attempt == max_retries:
                    print(f"  [mr_bricolage] category {cat_id} - page {current_page} - giving up after {max_retries} attempts")
                    raise
                time.sleep(2 * attempt)

        all_results.extend(data["products"])
        print(f"  [mr_bricolage] category {cat_id} - page {current_page + 1} - {len(all_results)} items so far")

        total_pages = data["pagination"]["totalPages"]
        current_page += 1

        if current_page < total_pages:
            time.sleep(RATE_LIMIT_SECONDS)

    return all_results


def normalize(raw_item):
    strike_price = raw_item.get("strikePrice")
    return {
        "source_id": str(raw_item["code"]),
        "name": raw_item["name"],
        "brand": None,
        "category_id": None,
        "unit_weight_text": raw_item.get("unit"),
        "price": float(raw_item["price"]["value"]),
        "currency": raw_item["price"]["currencyIso"],
        "was_promo": strike_price is not None,
        "discount_percent": None,
    }


def fetch_and_normalize_category(cat_id):
    raw_items = fetch_category(cat_id)
    return [normalize(item) for item in raw_items]