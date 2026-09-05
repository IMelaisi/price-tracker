import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.storage import (
    get_session_instance,
    get_or_create_retailer,
    get_or_create_product,
    add_price_entry,
)
from adapters.ebag import fetch_and_normalize_category as fetch_ebag_category
from adapters.mr_bricolage import fetch_and_normalize_category as fetch_mr_bricolage_category

EBAG_CATEGORY_IDS = [3, 1592, 490, 2, 419, 1533, 494, 1880, 1161, 6, 1095, 5, 5125, 7, 27, 28, 26, 29, 1614, 5745, 2305, 1093]

MAX_WORKERS = 5


def load_mr_bricolage_category_ids():
    ids = []
    with open("mr_bricolage_scrape_targets.txt", "r", encoding="utf-8") as f:
        for line in f:
            code, name = line.strip().split("\t")
            ids.append(code)
    return ids


MR_BRICOLAGE_CATEGORY_IDS = load_mr_bricolage_category_ids()


def fetch_all_categories_concurrently(retailer_name, category_ids, fetch_function):
    results = {}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_cat = {
            executor.submit(fetch_function, cat_id): cat_id
            for cat_id in category_ids
        }

        completed = 0
        total = len(category_ids)

        for future in as_completed(future_to_cat):
            cat_id = future_to_cat[future]
            completed += 1
            try:
                items = future.result()
                results[cat_id] = items
                print(f"[{retailer_name}] ({completed}/{total}) category {cat_id} done: {len(items)} items")
            except Exception as e:
                print(f"[{retailer_name}] ({completed}/{total}) category {cat_id} FAILED: {e}")
                results[cat_id] = []

    return results


BATCH_SIZE = 500


def insert_results(session, retailer_name, retailer_website, results):
    retailer = get_or_create_retailer(session, name=retailer_name, website=retailer_website)
    inserted = 0

    for cat_id, items in results.items():
        for item in items:
            product = get_or_create_product(
                session,
                retailer_id=retailer.id,
                source_id=item["source_id"],
                name=item["name"],
                brand=item["brand"],
                category_id=item["category_id"],
                unit_weight_text=item["unit_weight_text"],
            )

            add_price_entry(
                session,
                product_id=product.id,
                price=item["price"],
                currency=item["currency"],
                was_promo=item["was_promo"],
                discount_percent=item["discount_percent"],
                commit=False,
            )

            inserted += 1

            if inserted % BATCH_SIZE == 0:
                session.commit()
                print(f"[{retailer_name}] inserted {inserted} rows so far...")

    session.commit()
    return inserted


def run():
    start_time = time.time()
    session = get_session_instance()

    print(f"[ebag] Fetching {len(EBAG_CATEGORY_IDS)} categories concurrently ({MAX_WORKERS} at a time)...")
    ebag_results = fetch_all_categories_concurrently("ebag", EBAG_CATEGORY_IDS, fetch_ebag_category)
    ebag_count = insert_results(session, "ebag", "https://www.ebag.bg/en/", ebag_results)
    print(f"ebag: inserted {ebag_count} price entries.")

    print(f"[mr_bricolage] Fetching {len(MR_BRICOLAGE_CATEGORY_IDS)} categories concurrently ({MAX_WORKERS} at a time)...")
    mr_bricolage_results = fetch_all_categories_concurrently("mr_bricolage", MR_BRICOLAGE_CATEGORY_IDS, fetch_mr_bricolage_category)
    mr_bricolage_count = insert_results(session, "mr_bricolage", "https://mr-bricolage.bg/", mr_bricolage_results)
    print(f"mr_bricolage: inserted {mr_bricolage_count} price entries.")

    elapsed = time.time() - start_time
    print(f"Total inserted: {ebag_count + mr_bricolage_count} price entries.")
    print(f"Total runtime: {elapsed / 60:.1f} minutes")


if __name__ == "__main__":
    run()