from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import items, users

app = FastAPI()

# configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# registrar as rotas
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(users.router, prefix="/users", tags=["users"])
