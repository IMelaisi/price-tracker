import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}
BASE_URL = "https://api.mr-bricolage.bg/occ/v2/bricolage-spa/categories/{code}"

TOP_LEVEL_CODES = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011"]


def extract_leaves(category_node, leaves):
    children = category_node.get("categories", [])
    if not children:
        product_count = category_node.get("productsCount", 0)
        if product_count > 0:
            leaves.append((category_node["code"], category_node.get("name", ""), product_count))
    else:
        for child in children:
            extract_leaves(child, leaves)


def fetch_all_leaf_categories():
    all_leaves = []
    for code in TOP_LEVEL_CODES:
        url = BASE_URL.format(code=code)
        response = requests.get(url, headers=HEADERS, params={"lang": "bg", "curr": "EUR"}, timeout=15)
        response.raise_for_status()
        data = response.json()
        extract_leaves(data, all_leaves)
        print(f"Processed department {code}: {len(all_leaves)} leaf categories so far")
    return all_leaves


if __name__ == "__main__":
    leaves = fetch_all_leaf_categories()
    print()
    print(f"Total leaf categories found: {len(leaves)}")
    total_products = sum(count for _, _, count in leaves)
    print(f"Sum of productsCount across all leaves: {total_products}")

    with open("../mr_bricolage_category_ids.txt", "w", encoding="utf-8") as f:
        for code, name, count in leaves:
            f.write(f"{code}\t{name}\t{count}\n")

    print("Saved to mr_bricolage_category_ids.txt")