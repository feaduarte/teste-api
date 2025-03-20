from fastapi import FastAPI 
from pydantic import BaseModel 
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

app = FastAPI()

# Carregar variaveis do .env 

load_dotenv()

# Pegar URI do MongoDB

MONGO_URI = os.getenv("MONGO_URI")

# Conectar ao MongoDB

client = AsyncIOMotorClient(MONGO_URI)
db = client["Teste_API"]
collection = db["itens"]

# Atribuindo informação sobre a classe Item.
class Item(BaseModel):
    name: str
    price: float

# Rota p obter infos.
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

# Rota p criar.
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()  # Convertendo para dicionário
    result = await collection.insert_one(item_dict)  # Inserindo no MongoDB
    return {"name": item.name, "price": item.price, "id": str(result.inserted_id)}

# Rota p atualizar.
@app.put("/items/{item_id}")
async def update_item(item_id: int , item: Item):
    updated_item = {"name": item.name, "price": item.price}
    result = await collection.update_one({"_id": item_id}, {"$set": updated_item})
    return {"item_id": item_id, "name": item.name, "price": item.price, "message": "Item atualizado com sucesso!"}

# Rota para atualizar parcialmente.
@app.patch("/items/{item_id}")
async def patch_item(item_id: int, item: Item):
    updated_item = {"name": item.name, "price": item.price}
    result = await collection.update_one({"_id": item_id}, {"$set": updated_item})
    return {"item_id": item_id, "name": item.name, "price": item.price, "message": "Item atualizado parcialmente!"}

# Rota p deletar.
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    result = await collection.delete_one({"_id": item_id})
    if result.deleted_count:
        return {"message": f"Item {item_id} deletado com sucesso"}
    return {"message": f"Item {item_id} não encontrado"}

# Rota com parametro de consulta (Exemplo retornar produtos numa página)
@app.get("/items/")
async def get_items(skip: int = 0, limit: int = 10):
    items = collection.find().skip(skip).limit(limit)
    items_list = await items.to_list(length=limit)
    return {"items": items_list}
