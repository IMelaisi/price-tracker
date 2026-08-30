from core.storage import (
    get_session_instance,
    get_or_create_retailer,
    get_or_create_product,
    add_price_entry,
)
from adapters.ebag import fetch_and_normalize_category as fetch_ebag_category
from adapters.mr_bricolage import fetch_and_normalize_category as fetch_mr_bricolage_category

EBAG_CATEGORY_IDS = [1748]
MR_BRICOLAGE_CATEGORY_IDS = ["003001001"]


def run_retailer(session, retailer_name, retailer_website, category_ids, fetch_function):
    retailer = get_or_create_retailer(session, name=retailer_name, website=retailer_website)
    inserted = 0

    for cat_id in category_ids:
        items = fetch_function(cat_id)

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
            )

            inserted += 1

    return inserted


def run():
    session = get_session_instance()

    ebag_count = run_retailer(
        session,
        retailer_name="ebag",
        retailer_website="https://www.ebag.bg/en/",
        category_ids=EBAG_CATEGORY_IDS,
        fetch_function=fetch_ebag_category,
    )
    print(f"ebag: inserted {ebag_count} price entries.")

    mr_bricolage_count = run_retailer(
        session,
        retailer_name="mr_bricolage",
        retailer_website="https://mr-bricolage.bg/",
        category_ids=MR_BRICOLAGE_CATEGORY_IDS,
        fetch_function=fetch_mr_bricolage_category,
    )
    print(f"mr_bricolage: inserted {mr_bricolage_count} price entries.")

    print(f"Total inserted: {ebag_count + mr_bricolage_count} price entries.")


if __name__ == "__main__":
    run()