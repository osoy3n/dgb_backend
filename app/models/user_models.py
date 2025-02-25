from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.order_models import Orden

class UsuarioBase(SQLModel):
    usuario: str = Field(default=None)
    contrasena: str = Field(default=None)

class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios"

    id: int | None = Field(default=None, primary_key=True)
    ordenes: List["Orden"] = Relationship(back_populates="usuario")


class CrearActualizarUsuario(UsuarioBase):
    pass
