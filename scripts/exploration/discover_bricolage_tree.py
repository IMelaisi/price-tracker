import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceTrackerBot/0.1)"}
BASE_URL = "https://api.mr-bricolage.bg/occ/v2/bricolage-spa/categories/{code}"


def probe_top_level_codes():
    valid_codes = []
    for i in range(1, 31):
        code = f"{i:03d}"
        url = BASE_URL.format(code=code)
        response = requests.get(url, headers=HEADERS, params={"lang": "bg", "curr": "EUR"}, timeout=8)
        if response.status_code == 200:
            data = response.json()
            valid_codes.append((code, data.get("name", "")))
            print(f"FOUND\t{code}\t{data.get('name', '')}")
        else:
            print(f"skip\t{code}\t{response.status_code}")
    return valid_codes


if __name__ == "__main__":
    codes = probe_top_level_codes()
    print()
    print(f"Total top-level departments found: {len(codes)}")