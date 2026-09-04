import requests

url = "https://www.ebag.bg/en/categories/1/products/json"
headers = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}

response = requests.get(url, headers=headers, params={"page": 500}, timeout=10)
print(f"Status code for page 500: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"count: {data['count']}")
    print(f"next: {data['next']}")
    print(f"results on this page: {len(data['results'])}")