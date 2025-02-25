from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from typing import List

from database.db_config import SessionDependency
from models.order_models import Orden, CrearActualizarOrden
from models.shopping_models import Compras

router = APIRouter()

@router.post(
    "/ordenes",
    response_model=Orden,
    status_code=status.HTTP_201_CREATED
)
async def crear_orden(data_orden: CrearActualizarOrden, session: SessionDependency):
    dic_orden = data_orden.model_dump()
    orden = Orden.model_validate(dic_orden)
    session.add(orden)
    session.commit()
    session.refresh(orden)
    return orden

@router.get(
    "/ordenes",
    response_model=List[Orden],
    status_code=status.HTTP_200_OK
)
async def obtener_ordenes(session: SessionDependency):
    return session.exec(select(Orden)).all()

@router.get(
    "/ordenes/{id_orden}",
    response_model=Orden,
    status_code=status.HTTP_200_OK
)
async def obtener_orden(id_orden: int, session: SessionDependency):
    orden = session.get(Orden, id_orden)
    if not orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return orden

@router.patch(
    "/ordenes/{id_orden}",
    response_model=Orden,
    status_code=status.HTTP_201_CREATED
)
async def actualizar_orden(id_orden: int, data_orden: CrearActualizarOrden, session: SessionDependency):
    orden = await obtener_orden(id_orden, session)
    dic_orden = data_orden.model_dump(exclude_unset=True)
    orden.sqlmodel_update(dic_orden)
    session.add(orden)
    session.commit()
    session.refresh(orden)
    return orden

@router.delete(
    "/ordenes/{id_orden}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def eliminar_orden(id_orden: int, session: SessionDependency):
    compra = session.exec(select(Compras).where(Compras.id_orden == id_orden)).first()
    if compra:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar una orden con compras asociadas")
    orden = await obtener_orden(id_orden, session)
    session.delete(orden)
    session.commit()
    return {"detail": "Orden Eliminada"}
