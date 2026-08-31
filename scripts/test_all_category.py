import requests

url = "https://www.ebag.bg/en/categories/1/products/json"
headers = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()
data = response.json()

print(f"count: {data['count']}")
print(f"next: {data['next']}")
print(f"number of results on this page: {len(data['results'])}")