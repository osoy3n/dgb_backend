from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.character_models import Personaje
    from models.order_models import Orden

class ComprasBase(SQLModel):
    id_personaje: int = Field(foreign_key="personajes.id")
    id_orden: int = Field(foreign_key="ordenes.id")

class Compras(ComprasBase, table=True):
    __tablename__ = "compras"

    id: int | None = Field(default=None, primary_key=True)
    orden: "Orden" = Relationship(back_populates="compras_orden")
    personaje: "Personaje" = Relationship(back_populates="compras_personaje")

class CrearActualizarOrden(ComprasBase):
    pass
