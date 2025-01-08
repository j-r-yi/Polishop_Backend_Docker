from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserSchema(BaseModel):
    username: str
    password: str
    email: str

class UpdatePasswordRequest(BaseModel):
    new_password: str


class UserPackage(BaseModel):
    email: str
    password: str

class UpdateCartRequest(BaseModel):
    new_cart: str

class ProductSchema(BaseModel):
    img: Optional[str]
    name: str
    price: float
    # color: Optional[str]
    discount: Optional[float]
    description: Optional[str]
    # rating: Optional[float]
    quantity: Optional[int]
    # stockQuantity: Optional[int]
    # reviews: Optional[int]
    # date_created: Optional[datetime]
    product_details: Optional[str]
    gallery_1: Optional[str]
    gallery_2: Optional[str]
    category: str
    subcategory: str