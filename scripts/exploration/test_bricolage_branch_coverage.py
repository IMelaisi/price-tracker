import requests

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


branch_id = "004001"  # "Настолни лампи" branch
leaf_a = "004001002"  # 571 products
leaf_b = "004001003"  # 19 products

branch_count = get_product_count(branch_id)
leaf_a_count = get_product_count(leaf_a)
leaf_b_count = get_product_count(leaf_b)

print(f"Branch {branch_id}: {branch_count} products")
print(f"Leaf {leaf_a}: {leaf_a_count} products")
print(f"Leaf {leaf_b}: {leaf_b_count} products")
print(f"Sum of leaves: {leaf_a_count + leaf_b_count}")