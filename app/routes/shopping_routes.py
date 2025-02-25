from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from typing import List

from database.db_config import SessionDependency
from models.shopping_models import Compras, CrearActualizarCompra

router = APIRouter()

@router.post(
    "/compras",
    response_model=Compras,
    status_code=status.HTTP_201_CREATED
)
async def crear_compra(data_compra: CrearActualizarCompra, session: SessionDependency):
    dic_compra = data_compra.model_dump()
    compra = Compras.model_validate(dic_compra)
    session.add(compra)
    session.commit()
    session.refresh(compra)
    return compra

@router.get(
    "/compras",
    response_model=List[Compras],
    status_code=status.HTTP_200_OK
)
async def obtener_compras(session: SessionDependency):
    return session.exec(select(Compras)).all()

@router.get(
    "/compras/{id_compra}",
    response_model=Compras,
    status_code=status.HTTP_200_OK
)
async def obtener_compra(id_compra: int, session: SessionDependency):
    compra = session.get(Compras, id_compra)
    if not compra:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compra no encontrada")
    return compra

@router.patch(
    "/compras/{id_compra}",
    response_model=Compras,
    status_code=status.HTTP_201_CREATED
)
async def actualizar_compra(id_compra: int, data_compra: CrearActualizarCompra, session: SessionDependency):
    compra = await obtener_compra(id_compra, session)
    dic_compra = data_compra.model_dump(exclude_unset=True)
    compra.sqlmodel_update(dic_compra)
    session.add(compra)
    session.commit()
    session.refresh(compra)
    return compra

@router.delete(
    "/compras/{id_compra}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def eliminar_compra(id_compra: int, session: SessionDependency):
    compra = await obtener_compra(id_compra, session)
    session.delete(compra)
    session.commit()
    return {"detail": "Compra Eliminada"}
