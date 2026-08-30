import os
from dotenv import load_dotenv
from core.models import get_engine, init_db, get_session, Retailer, Product, PriceEntry

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

_engine = get_engine(DATABASE_URL)
init_db(_engine)


def get_or_create_retailer(session, name, website):
    retailer = session.query(Retailer).filter_by(name=name).first()
    if retailer is None:
        retailer = Retailer(name=name, website=website)
        session.add(retailer)
        session.commit()
    return retailer


def get_or_create_product(session, retailer_id, source_id, name, brand, category_id, unit_weight_text):
    product = session.query(Product).filter_by(
        retailer_id=retailer_id, source_id=source_id
    ).first()
    if product is None:
        product = Product(
            retailer_id=retailer_id,
            source_id=source_id,
            name=name,
            brand=brand,
            category_id=category_id,
            unit_weight_text=unit_weight_text,
        )
        session.add(product)
        session.commit()
    return product


def add_price_entry(session, product_id, price, currency, was_promo, discount_percent):
    entry = PriceEntry(
        product_id=product_id,
        price=price,
        currency=currency,
        was_promo=was_promo,
        discount_percent=discount_percent,
    )
    session.add(entry)
    session.commit()
    return entry


def get_session_instance():
    return get_session(_engine)