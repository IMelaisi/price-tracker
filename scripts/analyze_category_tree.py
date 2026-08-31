import requests

url = "https://www.ebag.bg/en/categories/json"
headers = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}

response = requests.get(url, headers=headers, timeout=15)
data = response.json()

categories = data["categories"]

by_id = {cat["id"]: cat for cat in categories}

top_level = [cat for cat in categories if cat["parent_id"] == 1]

print(f"Total categories: {len(categories)}")
print(f"Top-level categories (direct children of 'All', id=1): {len(top_level)}")
print()

for cat in sorted(top_level, key=lambda c: c["index"]):
    child_count = sum(1 for c in categories if c["parent_id"] == cat["id"])
    print(f"id={cat['id']}\tname={cat['name_en']}\tdirect_children={child_count}")