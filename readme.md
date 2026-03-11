# Rugby App Secure — Hardened Management Platform
![Security: OWASP Top 10](https://img.shields.io/badge/Security-OWASP%20Top%2010-green.svg)
![Docker: Orchestrated](https://img.shields.io/badge/Docker-Orchestrated-blue.svg)
![Backend: FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)
![Status: Protected](https://img.shields.io/badge/Status-Protected-success)

**Rugby App Secure** es un ecosistema de gestión deportiva blindado bajo estándares de **Defensa en Profundidad**. Este proyecto implementa microservicios aislados, autenticación de triple factor y mitigaciones activas contra vulnerabilidades web críticas.

---

## Índice de Contenidos
- [Arquitectura de Infraestructura](#️-arquitectura-de-infraestructura)
- [Especificaciones de Seguridad (OWASP Top 10)](#️-especificaciones-de-seguridad-owasp-top-10)
- [Estructura de Archivos y Configuraciones](#-estructura-de-archivos-y-configuraciones)
- [Guía de Instalación y Despliegue](#-guía-de-instalación-y-despliegue)
- [Ciclo de Integridad (Script de Aduana)](#-ciclo-de-integridad-script-de-aduana)

---

## Arquitectura de Infraestructura
La aplicación se despliega mediante **Docker Compose**, segmentando los servicios en una red privada virtual denominada `rugby-net`.

| Servicio | Imagen | IP Estática | Función de Seguridad |
| :--- | :--- | :--- | :--- |
| **`db`** | `postgres:15-alpine` | `172.20.0.10` | Persistencia aislada sin acceso externo. |
| **`cache`** | `redis:alpine` | `172.20.0.20` | Gestión de sesiones y mitigación de carga. |
| **`api`** | `FastAPI (Custom)` | `172.20.0.30` | Lógica blindada y validación de tokens. |
| **`frontend`** | `Nginx:alpine` | `172.20.0.40` | Proxy Inverso con terminación SSL/TLS. |

---

## Especificaciones de Seguridad (OWASP Top 10)

### 1. Control de Acceso y MFA (A01:2021)
Implementamos un sistema de **Autenticación de Triple Factor** lógico para evitar el acceso no autorizado.
* **Mecanismo**: Al registrarse, el servidor genera un **PIN de 4 dígitos** aleatorio (`random.randint(1000, 9999)`).
* **Validación**: El acceso requiere `Usuario + Password + PIN`.
* **Archivo Clave**: `rugby-app/backend/main.py`.



### 2. Fallas Criptográficas (A02:2021)
* **Bcrypt**: Las contraseñas nunca se guardan en texto plano; utilizamos hashing con sal activa.
* **JWT Stateless**: Sesiones gestionadas por tokens firmados (HS256) con expiración de 60 min.
* **Archivo Clave**: `rugby-app/backend/main.py`.

### 3. Prevención de Inyección (A03:2021)
* **SQLAlchemy ORM**: Neutralizamos ataques de SQL Injection mediante el uso de consultas parametrizadas automáticas.
* **Archivo Clave**: `rugby-app/backend/database.py`.

### 4. Configuración Incorrecta (A05:2021)
* **Nginx Hardening**: Cabeceras de seguridad CSP, HSTS y X-Frame-Options configuradas para mitigar XSS y Clickjacking.
* **Usuario No-Root**: El contenedor de la API corre bajo el usuario `rugbyuser`.
* **Archivo Clave**: `rugby-app/nginx/nginx.conf` y `backend/Dockerfile`.

### 5. Fallas de Identificación (A07:2021)
* **Rate Limiting**: El endpoint `/token` está limitado a **5 intentos por minuto** por IP para bloquear ataques de fuerza bruta.
* **Archivo Clave**: `rugby-app/backend/main.py`.

---

## Estructura de Archivos y Configuraciones

* **`backend/main.py`**: Contiene la lógica de seguridad (FastAPI, JWT, SlowAPI, PIN generation).
* **`backend/database.py`**: Configuración del motor SQLAlchemy con detección dinámica de host (Local/Docker).
* **`frontend/app.js`**: Gestión de la interfaz reactiva y persistencia de tokens en `localStorage`.
* **`docker-compose.yml`**: Orquestación de la red `rugby-net` y asignación de volúmenes persistentes.

---

## 🚀 Guía de Instalación y Despliegue

### 1. Configuración de Secretos
Crea un archivo `.env` en la raíz (ignorado por Git por seguridad):
```bash
POSTGRES_USER=rugby_admin
POSTGRES_PASSWORD=Vir-24
POSTGRES_DB=rugby_db
JWT_SECRET=tu_clave_secreta_maestra
```

### 2. Generación de Capa SSL
Genera los certificados autofirmados necesarios para habilitar el cifrado **HTTPS** en el servidor Nginx:

```bash
mkdir -p nginx/certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/certs/rugby.key -out nginx/certs/rugby.crt
```

### 3. Lanzamiento del Sistema
Despliega la infraestructura completa en segundo plano:

```bash
sudo docker compose up -d --build
```

## Detalle Técnico de la App
Esta sección explica la interacción profunda entre los componentes del backend para garantizar la integridad del sistema.

### Validación de Datos y Esquemas (Pydantic)
* **Integridad Estricta**: Utilizamos Pydantic en `schemas.py` para definir la forma exacta de los datos. Si un usuario intenta enviar un campo adicional o un tipo de dato incorrecto (ej. un número donde debe ir el nombre de un equipo), la API rechaza la petición mediante un error 422 antes de que llegue a la base de datos.
* **Seguridad de Respuesta**: Los esquemas aseguran que nunca se envíen datos sensibles, como el PIN o el hash de la contraseña, de vuelta al cliente en las consultas de jugadores.

### El "Guardián" de Rutas (Middleware & Depends)
* **Inyección de Dependencias**: La función `obtener_usuario_actual` actúa como un checkpoint obligatorio. Se inserta en las rutas de `/jugadores/` mediante `Depends`, garantizando que solo usuarios con un Token JWT válido y no expirado puedan ver o crear registros.
* **CORS (Cross-Origin Resource Sharing)**: En `main.py`, el middleware de CORS está configurado para aceptar únicamente peticiones desde la IP específica del frontend (`https://10.50.58.13`), bloqueando intentos de uso de la API desde dominios no autorizados.

---

## Experiencia de Usuario y Seguridad Frontend
El frontend gestiona la seguridad de forma transparente para el usuario final.

* **Gestión de Sesiones**: El archivo `app.js` gestiona el ciclo de vida del token. Si el backend devuelve un error `401 Unauthorized` (token expirado), el frontend ejecuta automáticamente la función `logout()`, limpiando el `localStorage` y redirigiendo al inicio de sesión.
* **Feedback en Tiempo Real**: El sistema de pestañas en `index.html` cambia dinámicamente el DOM para mostrar u ocultar el campo del PIN, mejorando la usabilidad mientras mantiene el flujo de seguridad estricto.
* **Persistencia Segura**: Todos los datos del jugador se envían como objetos JSON cifrados a través del túnel HTTPS proporcionado por la configuración de Nginx.

---

## Variables de Entorno y Configuración
Configuración detallada para el despliegue correcto de la infraestructura.

| Variable | Propósito | Impacto en Seguridad |
| :--- | :--- | :--- |
| **`POSTGRES_USER`** | Define el dueño de la DB en PostgreSQL. | Evita el uso del usuario por defecto `postgres`. |
| **`DB_HOST`** | Indica a la API dónde buscar la base de datos. | Permite alternar entre el contenedor `db` y `localhost` para pruebas seguras. |
| **`JWT_SECRET`** | Semilla para la firma criptográfica de los tokens. | Crítico: Si se compromete, se pueden falsificar identidades; debe ser robusta. |
| **`ACCESS_TOKEN_EXPIRE_MINUTES`** | Tiempo de vida del token (60 min). | Limita la ventana de tiempo de exposición de un token interceptado. |

---

## Preguntas - Soluciones de Problemas Comunes

**¿Por qué veo un error 502 Bad Gateway?** Generalmente ocurre porque el contenedor `api` ha fallado al arrancar. Revisa los logs con `sudo docker logs rugby-app-api-1`. Suele deberse a una clave incorrecta en el `.env` o a que la base de datos aún no está lista para recibir conexiones.

**¿He olvidado mi PIN, puedo recuperarlo?** Por seguridad "Zero Knowledge", el PIN solo se muestra una vez al registrarse. Si se pierde, un administrador debe resetearlo directamente en la base de datos accediendo al contenedor con `docker exec`.

**¿Por qué Swagger (/api/docs) me da error de carga?** Asegúrate de acceder a través de la ruta del proxy: `https://[IP]/api/docs`. Si intentas acceder directamente al puerto 8000, la configuración de Nginx o el aislamiento de red de Docker bloquearán los recursos estáticos.

**¿Ciclo de Integridad (Script de Aduana)Archivo:?**

Verificar_y_subir.sh
Este script garantiza que ninguna versión insegura o corrupta llegue al despliegue final:

Reinicio DB: Levanta una instancia limpia de Postgres para asegurar puertos libres.

SQL Check: Valida la salud de las tablas ejecutando consultas internas.

Pytest: Ejecuta la suite de pruebas unitarias del backend.CURL Check: Verifica la respuesta HTTPS del servidor Nginx.

Comandos Rápidos de MantenimientoAcción Comando Limpieza Total 

```bash
sudo docker compose down -v

Reinicio Forzado
sudo docker compose up -d --build --force-recreate

Ver Logs API
sudo docker logs -f rugby-app-api-1

Entrar a DB
sudo docker exec -it rugby-app-db-1 psql -U rugby_admin -d rugby_db
```

---

## Notas Finales y Créditos
* **Licencia**: Este proyecto se distribuye bajo fines educativos para la demostración de despliegues seguros en entornos Docker.
* **Autor**: Desarrollado como proyecto de implementación de seguridad (SecDevOps).

---

## Ciclo de Integridad (Script de Aduana)
**Archivo:** `verificar_y_subir.sh`

Este script garantiza que ninguna versión insegura o corrupta llegue al despliegue final. Es obligatorio ejecutarlo antes de realizar cualquier subida al repositorio.

### Flujo de Validación Paso a Paso
1. **Preparación**: Instalación automática de dependencias de test.
2. **Hard Reset DB**: Reinicio del servicio de PostgreSQL y espera de 12 segundos para estabilidad.
3. **Health Check SQL**: Verificación interna de la existencia de la tabla `jugadores`.
4. **Unit Testing**: Ejecución de la suite `pytest` para validar lógica de negocio y seguridad.
5. **Web Check**: Validación final del estado `200 OK` vía HTTPS/Nginx.
6. **Auto-Push**: Si todas las fases son exitosas, sincroniza los cambios con GitHub automáticamente.

### Cómo ejecutar el script
Asegúrate de otorgar permisos de ejecución antes del primer uso:

```bash
chmod +x verificar_y_subir.sh
./verificar_y_subir.sh