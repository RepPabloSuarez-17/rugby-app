from sqlalchemy import Column, Integer, String
from database import Base

class Jugador(Base):
    __tablename__ = "jugadores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    posicion = Column(String)
    equipo = Column(String)

# TOKEN DINAMICO
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    pin = Column(String)
