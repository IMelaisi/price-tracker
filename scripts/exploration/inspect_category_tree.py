import json
import requests

url = "https://www.ebag.bg/en/categories/json"
headers = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}

response = requests.get(url, headers=headers, timeout=15)
data = response.json()

print(f"Type of top-level data: {type(data)}")

if isinstance(data, list):
    print(f"Number of top-level items: {len(data)}")
    print("First item, pretty-printed:")
    print(json.dumps(data[0], indent=2, ensure_ascii=False))
elif isinstance(data, dict):
    print(f"Top-level keys: {list(data.keys())}")
    print("Pretty-printed sample (first 2000 chars):")
    print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])