# --- ETAPA 1: Compilación (Builder) ---
FROM python:3.11-slim as builder

WORKDIR /app

# Instalamos dependencias de compilación si fueran necesarias
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

COPY requirements.txt .
# Instalamos las librerías en una carpeta local para luego copiarla
RUN pip install --user --no-cache-dir -r requirements.txt

# --- ETAPA 2: Ejecución (Final) ---
FROM python:3.11-slim

WORKDIR /app

# Creamos un usuario del sistema sin privilegios llamado 'rugbyuser'
RUN groupadd -r rugbygroup && useradd -r -g rugbygroup rugbyuser

# Copiamos solo las librerías instaladas desde la etapa anterior
COPY --from=builder /root/.local /home/rugbyuser/.local
# Copiamos el código de la aplicación
COPY . .

# Aseguramos que el usuario tenga permisos sobre su propia carpeta
RUN chown -R rugbyuser:rugbygroup /app

# Ajustamos las variables de entorno para que Python encuentre las librerías
ENV PATH=/home/rugbyuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# --- MEDIDA DE SEGURIDAD CLAVE: Cambiar a usuario no-root ---
USER rugbyuser

# Exponemos el puerto interno
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
