from fastapi import FastAPI

from database.db_config import init_db
from routes import character_routes

app = FastAPI(lifespan=init_db, title="G-Padilla API")

@app.get("/")
async def root():
    return {"mensaje": "Hola, bienvenido a G-Padilla API"}

app.include_router(character_routes.router, tags=["Personajes"])
