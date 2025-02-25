from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db_config import init_db
from routes import character_routes
from routes import order_routes
from routes import shopping_routes
from routes import user_routes

app = FastAPI(lifespan=init_db, title="G-Padilla API")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"mensaje": "Hola, bienvenido a G-Padilla API"}

app.include_router(character_routes.router, tags=["Personajes"])
app.include_router(order_routes.router, tags=["Ordenes"])
app.include_router(shopping_routes.router, tags=["Compras"])
app.include_router(user_routes.router, tags=["Usuarios"])
