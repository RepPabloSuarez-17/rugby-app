from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
import os
import random

# --- MEDIDA OWASP: RATE LIMITING ---
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Importamos tus archivos locales
import models, database, schemas

# 1. Configuramos el limitador por dirección IP
limiter = Limiter(key_func=get_remote_address)

# --- CONFIGURACIÓN DE SEGURIDAD ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("JWT_SECRET", "clave-secreta-pro")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Sincroniza las tablas
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Rugby App - Seguridad Blindada")

# 2. Unimos el limitador a la aplicación y manejamos el error de exceso
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- MEDIDA OWASP: CORS RESTRINGIDO ---
# Cambiamos "*" por tu IP específica para evitar que otros sitios usen tu API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://10.50.58.13"], 
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# --- EL GUARDIÁN ---
def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token sin identidad")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

# --- LÓGICA DE USUARIOS ---

@app.post("/register")
def register(username: str, password: str, db: Session = Depends(database.get_db)):
    existe = db.query(models.User).filter(models.User.username == username).first()
    if existe:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    nuevo_pin = str(random.randint(1000, 9999))
    hashed_pw = pwd_context.hash(password)
    nuevo_usuario = models.User(username=username, hashed_password=hashed_pw, pin=nuevo_pin)

    db.add(nuevo_usuario)
    db.commit()

    return {
        "message": "Usuario creado correctamente",
        "tu_pin_de_seguridad": nuevo_pin
    }

@app.post("/token")
@limiter.limit("5/minute")  # --- PROTECCIÓN CONTRA FUERZA BRUTA ---
async def login(
    request: Request,  # Requerido para el limitador
    security_token: str, 
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    # Validamos: Usuario + Password + PIN
    if not user or not pwd_context.verify(form_data.password, user.hashed_password) or security_token != user.pin:
        raise HTTPException(status_code=401, detail="Credenciales o PIN incorrectos")

    # Generación del Token JWT
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": user.username, "exp": expire}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}

# --- LÓGICA DE JUGADORES ---

@app.get("/jugadores/", response_model=list[schemas.Jugador])
def listar(db: Session = Depends(database.get_db), usuario: str = Depends(obtener_usuario_actual)):
    return db.query(models.Jugador).all()

@app.post("/jugadores/", response_model=schemas.Jugador)
def crear(jugador: schemas.JugadorCreate, db: Session = Depends(database.get_db), usuario: str = Depends(obtener_usuario_actual)):
    nuevo = models.Jugador(**jugador.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
