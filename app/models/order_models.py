from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.shopping_models import Compras
    from models.user_models import Usuario

class OrdenBase(SQLModel):
    total_item: int = Field(default=None)
    total_precio: int = Field(default=None)
    id_usuario: int = Field(foreign_key="usuarios.id")

class Orden(OrdenBase, table=True):
    __tablename__ = "ordenes"

    id: int | None = Field(default=None, primary_key=True)
    usuario: "Usuario" = Relationship(back_populates="ordenes")
    compras_orden: List["Compras"] = Relationship(back_populates="orden")

class CrearActualizarOrden(OrdenBase):
    pass
