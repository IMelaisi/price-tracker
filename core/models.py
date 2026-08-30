from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Boolean, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Retailer(Base):
    __tablename__ = "retailers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    website = Column(String, nullable=False)

    products = relationship("Product", back_populates="retailer")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    retailer_id = Column(Integer, ForeignKey("retailers.id"), nullable=False)
    source_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    category_id = Column(String, nullable=True)
    unit_weight_text = Column(String, nullable=True)

    retailer = relationship("Retailer", back_populates="products")
    price_entries = relationship("PriceEntry", back_populates="product")


class PriceEntry(Base):
    __tablename__ = "price_entries"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    was_promo = Column(Boolean, default=False)
    discount_percent = Column(Float, nullable=True)
    observed_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="price_entries")


def get_engine(db_url):
    return create_engine(db_url)


def init_db(engine):
    Base.metadata.create_all(engine)


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()