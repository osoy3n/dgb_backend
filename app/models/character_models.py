from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.shopping_models import Compras

class PersonajeBase(SQLModel):
    afiliacion: str = Field(default=None)
    descripcion: str = Field(default=None)
    genero: str = Field(default=None)
    imagen: str = Field(default=None)
    ki: str = Field(default=None)
    maxKi: str = Field(default=None)
    nombre: str = Field(default=None)
    precio: int = Field(default=None)

class Personaje(PersonajeBase, table=True):
    __tablename__ = "personajes"

    id: int = Field(default=None, primary_key=True)
    compras_personaje: List["Compras"] = Relationship(back_populates="personaje")


class ActualizarPersonaje(PersonajeBase):
    pass
