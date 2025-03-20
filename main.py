from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from bson import ObjectId

app = FastAPI()

# Carregar variaveis do .env
load_dotenv()

# Pegar URI do MongoDB
MONGO_URI = os.getenv("MONGO_URI")

# Conectar ao MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client["Teste_API"]
collection = db["itens"]

# Modelo de dados
class Item(BaseModel):
    name: str
    price: float

# Rota p obter informações de um item pelo ID
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    item = await collection.find_one({"_id": ObjectId(item_id)})
    if item:
        item["_id"] = str(item["_id"]) 
        return item
    raise HTTPException(status_code=404, detail="Item não encontrado")

# Rota p criar um item
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    result = await collection.insert_one(item_dict)
    return {"id": str(result.inserted_id), "name": item.name, "price": item.price}

# Rota p atualizar um item
@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    updated_item = {"$set": item.dict()}
    result = await collection.update_one({"_id": ObjectId(item_id)}, updated_item)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"message": "Item atualizado com sucesso!"}

# Rota p atualizar parcialmente um item
@app.patch("/items/{item_id}")
async def patch_item(item_id: str, item: Item):
    updated_item = {"$set": item.dict()}
    result = await collection.update_one({"_id": ObjectId(item_id)}, updated_item)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"message": "Item atualizado parcialmente!"}

# Rota p deletar um item
@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = await collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"message": f"Item {item_id} deletado com sucesso"}

# Rota p obter multiplos itens com paginacao (listar itens de uma pagina por ex)
@app.get("/items/")
async def get_items(skip: int = 0, limit: int = 10):
    items_cursor = collection.find().skip(skip).limit(limit)
    items = await items_cursor.to_list(length=limit)
    for item in items:
        item["_id"] = str(item["_id"])  
    return {"items": items}
