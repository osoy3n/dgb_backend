from sqlmodel import SQLModel, Field

class PersonajeBase(SQLModel):
    afiliacion: str = Field(default=None)
    descripcion: str = Field(default=None)
    genero: str = Field(default=None)
    imagen: str = Field(default=None)
    ki: str = Field(default=None)
    maxKi: str = Field(default=None)
    nombre: str = Field(default=None)

class Personaje(PersonajeBase, table=True):
    __tablename__ = "personajes"

    id: int = Field(default=None, primary_key=True)


class ActualizarPersonaje(PersonajeBase):
    pass
