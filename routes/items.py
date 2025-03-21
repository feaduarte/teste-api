from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import items_collection
from models import Item

router = APIRouter()

@router.get("/{item_id}")
async def read_item(item_id: str):
    item = await items_collection.find_one({"_id": ObjectId(item_id)})
    if item:
        item["_id"] = str(item["_id"]) 
        return item
    raise HTTPException(status_code=404, detail="Item não encontrado")

@router.post("/")
async def create_item(item: Item):
    item_dict = item.dict()
    result = await items_collection.insert_one(item_dict)
    return {"id": str(result.inserted_id), "name": item.name, "price": item.price}

@router.put("/{item_id}")
async def update_item(item_id: str, item: Item):
    updated_item = {"$set": item.dict()}
    result = await items_collection.update_one({"_id": ObjectId(item_id)}, updated_item)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"message": "Item atualizado com sucesso!"}

@router.delete("/{item_id}")
async def delete_item(item_id: str):
    result = await items_collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"message": f"Item {item_id} deletado com sucesso"}

@router.get("/")
async def get_items(skip: int = 0, limit: int = 10):
    items_cursor = items_collection.find().skip(skip).limit(limit)
    items = await items_cursor.to_list(length=limit)
    for item in items:
        item["_id"] = str(item["_id"])  
    return {"items": items}
