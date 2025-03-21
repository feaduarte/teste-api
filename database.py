import os
from dotenv import load_dotenv
from motor.import_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI= os.getenv("MONGO_URI")

# conexao mongodb

client = AsyncIOMotorClient(MONGO_URI)
db = client["Teste_API"]

# colecoes do mongodb

items_colletion = db["itens"]
users_colletion = db["users"]

