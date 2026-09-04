import requests
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}


def get_product_count(cat_id):
    url = f"https://api.mr-bricolage.bg/occ/v2/bricolage-spa/categories/{cat_id}/products/all"
    params = {
        "fields": "BASIC",
        "pageSize": 1,
        "sort": "relevance",
        "query": "",
        "lang": "bg",
        "curr": "EUR",
    }
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()["pagination"]["totalResults"]


targets = []
with open("../mr_bricolage_scrape_targets.txt", "r", encoding="utf-8") as f:
    for line in f:
        code, name = line.strip().split("\t")
        targets.append(code)

total = 0
for i, code in enumerate(targets, start=1):
    count = get_product_count(code)
    total += count
    if i % 20 == 0:
        print(f"Checked {i}/{len(targets)} - running total: {total}")
    time.sleep(0.2)

print(f"Final total products across all {len(targets)} targets: {total}")