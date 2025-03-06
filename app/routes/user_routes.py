from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from typing import List

from database.db_config import SessionDependency
from models.order_models import Orden
from models.user_models import Usuario, CrearActualizarUsuario

router = APIRouter()

@router.post(
    "/usuarios",
    response_model=Usuario,
    status_code=status.HTTP_201_CREATED
)
async def crear_usuario(data_usuario: CrearActualizarUsuario, session: SessionDependency):
    dic_usuario = data_usuario.model_dump()
    usuario = Usuario.model_validate(dic_usuario)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@router.get(
    "/usuarios",
    response_model=List[Usuario],
    status_code=status.HTTP_200_OK
)
async def obtener_usuarios(session: SessionDependency):
    return session.exec(select(Usuario)).all()

@router.get(
    "/usuarios/{id_usuario}",
    response_model=Usuario,
    status_code=status.HTTP_200_OK
)
async def obtener_usuario(id_usuario: int, session: SessionDependency):
    usuario = session.get(Usuario, id_usuario)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario

@router.patch(
    "/usuarios/{id_usuario}",
    response_model=Usuario,
    status_code=status.HTTP_201_CREATED
)
async def actualizar_usuario(id_usuario: int, data_usuario: CrearActualizarUsuario, session: SessionDependency):
    usuario = await obtener_usuario(id_usuario, session)
    dic_usuario = data_usuario.model_dump(exclude_unset=True)
    usuario.sqlmodel_update(dic_usuario)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@router.delete(
    "/usuarios/{id_usuario}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def eliminar_usuario(id_usuario: int, session: SessionDependency):
    orden = session.exec(select(Orden).where(Orden.id_usuario == id_usuario)).first()
    if orden:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar un usuario con ordenes asociadas")
    usuario = await obtener_usuario(id_usuario, session)
    session.delete(usuario)
    session.commit()
    return {"detail": "Usuario Eliminado"}
