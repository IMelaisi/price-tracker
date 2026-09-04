import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}

CANDIDATE_URLS = [
    "https://www.ebag.bg/en/categories/json",
    "https://www.ebag.bg/en/categories/tree/json",
    "https://www.ebag.bg/en/categories/all/json",
    "https://www.ebag.bg/en/category-tree/json",
    "https://www.ebag.bg/en/menu/json",
    "https://www.ebag.bg/en/nav/json",
    "https://www.ebag.bg/en/categories/1/json",
    "https://www.ebag.bg/en/categories/1/children/json",
    "https://www.ebag.bg/en/categories/1/subcategories/json",
]

for url in CANDIDATE_URLS:
    try:
        response = requests.get(url, headers=HEADERS, timeout=8)
        print(f"{response.status_code}\t{url}\t{len(response.content)} bytes")
    except requests.RequestException as e:
        print(f"ERROR\t{url}\t{e}")