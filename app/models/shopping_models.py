from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

from models.character_models import PersonajeBase
from models.order_models import OrdenBase

if TYPE_CHECKING:
    from models.character_models import Personaje, PersonajeBase
    from models.order_models import Orden, OrdenBase

class ComprasBase(SQLModel):
    id_personaje: int = Field(foreign_key="personajes.id")
    id_orden: int = Field(foreign_key="ordenes.id")

class Compras(ComprasBase, table=True):
    __tablename__ = "compras"

    id: int | None = Field(default=None, primary_key=True)
    orden: "Orden" = Relationship(back_populates="compras_orden")
    personaje: "Personaje" = Relationship(back_populates="compras_personaje")

class CrearActualizarCompra(ComprasBase):
    pass

class ComprasHechas(SQLModel):
    id_compra: int
    id_personaje: int
    id_orden: int
    orden: OrdenBase
    personaje: PersonajeBase
