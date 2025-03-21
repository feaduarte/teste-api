from pydantic import BaseModel

# modelo do item

class Item(BaseModel):
    name: str
    price: float

# modelo user

class User(BaseModel):
    username: str
    password: str