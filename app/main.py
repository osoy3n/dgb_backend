from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db_config import init_db
from routes import character_routes

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
