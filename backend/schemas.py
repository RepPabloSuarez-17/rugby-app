from pydantic import BaseModel

class JugadorBase(BaseModel):
    nombre: str
    posicion: str
    equipo: str

class JugadorCreate(JugadorBase):
    pass

class Jugador(JugadorBase):
    id: int
    class Config:
        from_attributes = True
