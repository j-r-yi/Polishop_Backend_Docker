from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from database import SessionLocal, engine
from models import Product, User, Banner
from schemas import UserSchema, UpdatePasswordRequest, UserPackage

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/products", response_model=List[dict])
def read_all_products(db: Session = Depends(get_db)):
    all_products = db.query(Product).all()
    if not all_products:
        raise HTTPException(status_code=404, detail="No products found")
    return [
        {
            "productId": product.productId,
            "img": product.img,
            "productname": product.name,
            "price": product.price,
            "color": product.color,
            "discount": product.discount,
            "description": product.description,
            "rating": product.rating,
            "quantity": product.quantity,
            "stockQuantity": product.stockQuantity,
            "reviews": product.reviews,
        }
        for product in all_products
    ]

@app.get("/products/{productId}", response_model=dict)
def read_item(productId: int, db: Session = Depends(get_db)):
    db_item = db.query(Product).filter(Product.productId == productId).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "productid": db_item.productId,
        "img": db_item.img,
        "productname": db_item.name,
        "price": db_item.price,
        "color": db_item.color,
        "discount": db_item.discount,
        "description": db_item.description,
        "rating": db_item.rating,
        "quantity": db_item.quantity,
        "stockQuantity": db_item.stockQuantity,
        "reviews": db_item.reviews,
    }

@app.get("/banners", response_model=List[dict])
def read_banners(db: Session = Depends(get_db)):
    all_banners = db.query(Banner).all()
    if not all_banners:
        raise HTTPException(status_code=404, detail="Banners not found")
    return[
        {
            "bannerId": banner.product_id,
            "image_source": banner.image_source
        }
        for banner in all_banners
    ]

@app.get("/users", response_model=List[dict])
def read_all_users(db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    if not all_users:
        raise HTTPException(status_code=404, detail="Users not found")
    return[
        {
            "userId": user.userId,
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "address": user.address
        }
        for user in all_users
    ]

@app.get("/user_info", response_model=dict)
def read_user(user: UserPackage, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return{
        "userId": user.userId,
        "username": user.username,
        "password": user.password,
        "email": user.email,
        "address": user.address,
        "cart": user.cart,
    }


@app.post("/users_post")
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    user_already_exists = db.query(User).filter((User.username==user.username) | (User.email==user.email)).first()
    if user_already_exists is not None:
        if user_already_exists.username == user.username:
            error_message = "Username already exists"
        else:
            error_message = "Email already used"
        return {"Error": error_message}
    else:
        db_user = User(username=user.username, email=user.email, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

@app.delete("/users_delete/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Username not found")
    db.delete(db_user)
    db.commit()
    return {"message": f"User {username} deleted successfully"}

@app.put("/password_update/{username}")
def update_password(username: str, update_password_request: UpdatePasswordRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Username not found")
    new_password = update_password_request.new_password
    db_user.password= new_password
    db.commit()
    return {"message": f"Password updated successfully for user {username}"}


@app.post("/login")
def user_login(user_data: UserPackage, db: Session = Depends(get_db)):
    email = user_data.email
    password = user_data.password

    db_user = db.query(User).filter(User.email == email).first()
    if db_user is None:
        return {"Error": "Email not found"}
    else:
        if db_user.password != password:
            return{"Error": "Password is incorrect"}
        return {"username": db_user.username, "email": db_user.email, "cart": db_user.cart}

    
