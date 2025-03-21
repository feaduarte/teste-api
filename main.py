from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from bson import ObjectId
from passlib.context import CryptContext


app = FastAPI()

# CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

# uri mongo
MONGO_URI = os.getenv("MONGO_URI")

# conectar MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client["Teste_API"]

items_collection = db["itens"]
users_collection = db["users"]

# modelo de Item
class Item(BaseModel):
    name: str
    price: float

# rota para obter informações de um item pelo ID
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    item = await items_collection.find_one({"_id": ObjectId(item_id)})
    if item:
        item["_id"] = str(item["_id"]) 
        return item
    raise HTTPException(status_code=404, detail="Item não encontrado")

# rota p criar um item
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    result = await items_collection.insert_one(item_dict)
    return {"id": str(result.inserted_id), "name": item.name, "price": item.price}

# rota p atualizar um item
@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    updated_item = {"$set": item.dict()}
    result = await items_collection.update_one({"_id": ObjectId(item_id)}, updated_item)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"message": "Item atualizado com sucesso!"}

# rota p deletar um item
@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = await items_collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"message": f"Item {item_id} deletado com sucesso"}

# rota p obter múltiplos itens com paginação
@app.get("/items/")
async def get_items(skip: int = 0, limit: int = 10):
    items_cursor = items_collection.find().skip(skip).limit(limit)
    items = await items_cursor.to_list(length=limit)
    for item in items:
        item["_id"] = str(item["_id"])  
    return {"items": items}

# hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Gera um hash seguro para a senha."""
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return pwd_context.verify(password, hashed_password)

# modelo de user
class User(BaseModel):
    username: str
    password: str  

# rota p criar um user
@app.post("/users/")
async def create_user(user: User):
    hashed_password = hash_password(user.password)  
    user_data = {"username": user.username, "hashed_password": hashed_password}
    result = await users_collection.insert_one(user_data)
    
    return {"id": str(result.inserted_id), "username": user.username}
