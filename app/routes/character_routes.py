from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from typing import List

from database.db_config import SessionDependency
from models.character_models import Personaje, ActualizarPersonaje
from libs.get_external_api import dragon_ball_api, generar_valores_random

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
            nombre = personaje_externo['name'],
            precio = generar_valores_random()
        )
        session.add(personaje)

    session.commit()
    return { "mensaje": "Personajes creados exitosamente" }

@router.post(
    "/personajes",
    response_model=Personaje,
    status_code=status.HTTP_201_CREATED
)
async def crear_personaje(data_personaje: Personaje, session: SessionDependency):
    dic_personaje = data_personaje.model_dump()
    personaje = Personaje.model_validate(dic_personaje)
    session.add(personaje)
    session.commit()
    session.refresh(personaje)
    return personaje

@router.get(
    "/personajes",
    response_model=List[Personaje],
    status_code=status.HTTP_200_OK
)
async def obtener_personajes(session: SessionDependency):
    return session.exec(select(Personaje)).all()

@router.get(
    "/personajes/{id_personaje}",
    response_model=Personaje,
    status_code=status.HTTP_200_OK
)
async def obtener_personaje(id_personaje: int, session: SessionDependency):
    personaje = session.get(Personaje, id_personaje)
    if not personaje:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personaje no encontrado")
    return personaje

@router.patch(
    "/personajes/{id_personaje}",
    response_model=Personaje,
    status_code=status.HTTP_201_CREATED
)
async def actualizar_personaje(id_personaje: int, data_personaje: ActualizarPersonaje, session: SessionDependency):
    personaje = await obtener_personaje(id_personaje, session)
    dic_personaje = data_personaje.model_dump(exclude_unset=True)
    personaje.sqlmodel_update(dic_personaje)
    session.add(personaje)
    session.commit()
    session.refresh(personaje)
    return personaje

@router.delete(
    "/personajes/{id_personaje}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def eliminar_personaje(id_personaje: int, session: SessionDependency):
    personaje = await obtener_personaje(id_personaje, session)
    session.delete(personaje)
    session.commit()
    return {"detail": "Personaje Eliminado"}
