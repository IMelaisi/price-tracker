import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}


def get_count(cat_id):
    url = f"https://www.ebag.bg/en/categories/{cat_id}/products/json"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()["count"]


parent_id = 3  # Fruits and vegetables
child_id_a = 600  # Fruit
child_id_b = 601  # Vegetables (from earlier sitemap sample)

parent_count = get_count(parent_id)
child_a_count = get_count(child_id_a)
child_b_count = get_count(child_id_b)

print(f"Parent (Fruits and vegetables, id={parent_id}): {parent_count} products")
print(f"Child (Fruit, id={child_id_a}): {child_a_count} products")
print(f"Child (Vegetables, id={child_id_b}): {child_b_count} products")
print(f"Sum of these two children: {child_a_count + child_b_count}")