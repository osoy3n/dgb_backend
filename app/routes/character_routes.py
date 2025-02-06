from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select

from database.db_config import SessionDependency
from models.character_models import Personaje
from libs.get_external_api import dragon_ball_api

router = APIRouter()

@router.post(
    "/personajes_externos",
    status_code=status.HTTP_201_CREATED
)
async def crear_personajes(session: SessionDependency):
    data = dragon_ball_api()
    personajes_externos = data['items']

    for personaje_externo in personajes_externos:
        personaje = Personaje(
            id = personaje_externo['id'],
            afiliacion = personaje_externo['affiliation'],
            descripcion = personaje_externo['description'],
            genero = personaje_externo['gender'],
            imagen = personaje_externo['image'],
            ki = personaje_externo['ki'],
            maxKi = personaje_externo['maxKi'],
            nombre = personaje_externo['name']
        )
        session.add(personaje)

    session.commit()
    return { "mensaje":  "Personajes creados exitosamente" }

@router.post(
    "/personajes",
    response_model=Personaje,
    status_code=status.HTTP_201_CREATED
)
async def crear_personaje(data: Personaje, session: SessionDependency):
    pass