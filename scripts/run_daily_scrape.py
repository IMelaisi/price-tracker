from core.storage import (
    get_session_instance,
    get_or_create_retailer,
    get_or_create_product,
    add_price_entry,
)
from adapters.ebag import fetch_and_normalize_category

EBAG_CATEGORY_IDS = [1748]


def run():
    session = get_session_instance()

    retailer = get_or_create_retailer(
        session, name="ebag", website="https://www.ebag.bg/en/"
    )

    total_inserted = 0

    for cat_id in EBAG_CATEGORY_IDS:
        items = fetch_and_normalize_category(cat_id)

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

            total_inserted += 1

    print(f"Inserted {total_inserted} price entries.")


if __name__ == "__main__":
    run()