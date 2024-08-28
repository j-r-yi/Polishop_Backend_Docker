from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base

class Product(Base):
    __tablename__ = 'products'

    productId = Column(Integer, primary_key=True, index=True)
    img = Column(String(255))
    name = Column(String(255))
    price = Column(Float) 
    color = Column(String(255))
    discount = Column(Float)
    description = Column(String(255))
    rating = Column(Float)
    quantity = Column(Integer)
    stockQuantity = Column(Integer)
    reviews = Column(Integer)
    date_created = Column(DateTime)
    product_details = Column(String)
    gallery_1 = Column(String)
    gallery_2 = Column(String)
    category = Column(String)


class Banner(Base):
    __tablename__ = 'product_banner_images'

    product_id = Column(Integer, primary_key=True, index=True)
    image_source = Column(String(255))

class User(Base):
    __tablename__ = 'users'

    userId = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))
    password = Column(String(255))
    email = Column(String(255))
    address = Column(String(255))
    cart = Column(String(255))
