from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# --- LÓGICA DE CONEXIÓN DINÁMICA ---
# Extraemos variables o usamos valores por defecto (asegúrate que coincidan con tu .env)
# DB_HOST = os.getenv("DB_HOST", "db")
user = os.getenv('POSTGRES_USER', 'rugby_admin')
password = os.getenv('POSTGRES_PASSWORD', 'Vir-24')
database = os.getenv('POSTGRES_DB', 'rugby_db')

# Si detecta DB_HOST=localhost (desde el script de aduana), lo usa. 
# Si no hay variable, por defecto usa 'db' para Docker.
host = os.getenv('DB_HOST', 'db') 

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
