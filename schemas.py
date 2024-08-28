from pydantic import BaseModel

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