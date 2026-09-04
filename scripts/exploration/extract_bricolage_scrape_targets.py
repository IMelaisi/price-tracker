import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}
BASE_URL = "https://api.mr-bricolage.bg/occ/v2/bricolage-spa/categories/{code}"
TOP_LEVEL_CODES = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011"]


def pick_scrape_targets(node, targets):
    children = node.get("categories", [])

    if not children:
        targets.append((node["code"], node.get("name", "")))
        return

    all_children_are_leaves = all(not child.get("categories", []) for child in children)

    if all_children_are_leaves:
        targets.append((node["code"], node.get("name", "")))
    else:
        for child in children:
            pick_scrape_targets(child, targets)


def fetch_all_targets():
    all_targets = []
    for code in TOP_LEVEL_CODES:
        url = BASE_URL.format(code=code)
        response = requests.get(url, headers=HEADERS, params={"lang": "bg", "curr": "EUR"}, timeout=15)
        response.raise_for_status()
        data = response.json()
        pick_scrape_targets(data, all_targets)
        print(f"Processed department {code}: {len(all_targets)} scrape targets so far")
    return all_targets


if __name__ == "__main__":
    targets = fetch_all_targets()
    print()
    print(f"Total scrape targets: {len(targets)}")

    with open("../mr_bricolage_scrape_targets.txt", "w", encoding="utf-8") as f:
        for code, name in targets:
            f.write(f"{code}\t{name}\n")

    print("Saved to mr_bricolage_scrape_targets.txt")