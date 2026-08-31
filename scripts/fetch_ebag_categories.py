import re
import requests

SITEMAP_URL = "https://www.ebag.bg/en/sitemap_categories_en.xml"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}

PATTERN = re.compile(
    r"<loc>https://www\.ebag\.bg/en/categories/([a-z0-9-]+)/(\d+)</loc>"
)


def fetch_category_ids():
    response = requests.get(SITEMAP_URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
    xml_text = response.text

    matches = PATTERN.findall(xml_text)

    seen_ids = set()
    unique_categories = []
    for slug, cat_id in matches:
        if cat_id not in seen_ids:
            seen_ids.add(cat_id)
            unique_categories.append((slug, cat_id))

    return unique_categories


if __name__ == "__main__":
    categories = fetch_category_ids()
    print(f"Found {len(categories)} unique category IDs.")

    with open("ebag_category_ids.txt", "w", encoding="utf-8") as f:
        for slug, cat_id in categories:
            f.write(f"{cat_id}\t{slug}\n")

    print("Saved to ebag_category_ids.txt")
    print("First 10 entries:")
    for slug, cat_id in categories[:10]:
        print(f"{cat_id}\t{slug}")