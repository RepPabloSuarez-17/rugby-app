🛡️ Seguridad y Cumplimiento (OWASP Top 10) Este proyecto ha sido auditado bajo los estándares de OWASP, implementando controles específicos para mitigar las vulnerabilidades más críticas en aplicaciones web modernas.

📊 Matriz de Mitigación ID Categoría OWASP Medida Técnica Implementada Estado A01 Broken Access Control Roles de usuario (Admin/User) y validación de PIN de 4 dígitos personal para cada cuenta.

✅A02 Cryptographic Failures Hashing de contraseñas con Bcrypt (Salt factor 12) y cifrado forzado en tránsito mediante TLS/SSL.

✅A03 Injection Uso de SQLAlchemy ORM para parametrizar todas las consultas, neutralizando ataques de SQL Injection.

✅A05 Security Misconfiguration Hardening de Nginx con cabeceras HSTS, CSP, X-Content-Type y X-Frame-Options.

✅A07 Identification & Auth Implementación de JWT (JSON Web Tokens) con firma criptográfica y Rate Limiting (5 intentos/min).

✅Exportar a Hojas de cálculo

🏗️ Arquitectura de Defensa en Profundidad La aplicación no solo es código seguro, sino que reside en una infraestructura blindada mediante contenedores orquestados.

Aislamiento de Red (Network Sandboxing) Todos los microservicios se comunican a través de una red privada virtual denominada rugby-net.
Zero Trust: La base de datos PostgreSQL y el servidor Redis no exponen puertos al exterior; solo son accesibles para la API de FastAPI.

Proxy Inverso: Nginx actúa como única puerta de enlace, filtrando el tráfico malicioso antes de que llegue al backend.

Principio de Menor Privilegio (Least Privilege) Usuario No-Root: El contenedor de la API ha sido configurado para correr bajo el usuario rugbyuser.
Restricción de Ejecución: En caso de una brecha de seguridad, el atacante no tendría privilegios de administrador (root) para escalar posiciones dentro del servidor.

🛠️ Stack Tecnológico Profesional Capa Tecnología Función de Seguridad API FastAPI (Python 3.11) Validación estricta de esquemas de datos (Pydantic). 
Proxy Nginx 1.29 Terminación SSL y cabeceras de seguridad OWASP. Database PostgreSQL 15 Almacenamiento persistente con acceso restringido por IP interna. 
Cache Redis Manejo eficiente de sesiones y listas negras de tokens. DevSecOps GitHub Actions Pipeline de CI/CD para validación automática de integridad en cada push.

🛡️ Rugby App Secure - Manual de Proyecto BlindadoRugby App Secure es un ecosistema de gestión deportiva diseñado bajo el paradigma de Defensa en Profundidad. 
La aplicación utiliza microservicios aislados para garantizar que la información de los jugadores y usuarios esté protegida contra los ataques más comunes de la web moderna.

🛠️ Stack Tecnológico y Ubicación de ArchivosCapaTecnologíaUbicación del ArchivoFunción PrincipalBackendFastAPI (Python 3.11)rugby-app/backend/main.pyLógica de negocio, JWT y Rate Limiting. 
FrontendJS Vanilla / HTML5rugby-app/frontend/Interfaz de usuario y consumo de API. Base de DatosPostgreSQL 15 rugby-app/docker-compose.yml

Almacenamiento persistente de datos. Proxy/WebNginxrugby-app/nginx/nginx.confCifrado SSL/TLS y seguridad de cabeceras.AutomatizaciónBash Script./verificar_y_subir.shValidación local e integridad CI/CD.

🏗️ Arquitectura de Infraestructura (Docker)El proyecto se despliega mediante Docker Compose, creando una red virtual privada donde los servicios están segmentados.
Red Aislada (rugby-net): Subred 172.20.0.0/16 que impide que la base de datos sea vista desde el exterior.IPs Estáticas: Cada servicio tiene una IP fija para evitar ataques de suplantación interna:
DB: 172.20.0.10 
Redis: 172.20.0.20 
API: 172.20.0.30 
Nginx: 172.20.0.40

🛡️ Implementación de Seguridad (Hardening)1. Gestión de Identidad (OWASP A01)Doble Factor Lógico (PIN): Al registrarse en main.py, el sistema genera un PIN único (random.randint(1000, 9999)) 
que se almacena junto al hash de la contraseña.

Hashing Criptográfico: Las contraseñas se cifran usando Bcrypt con un factor de sal adecuado en el backend.2. Control de Tasa (Rate Limiting)Protección de Login: 
El endpoint /token en main.py utiliza slowapi para limitar los intentos a 5 por minuto, neutralizando ataques de fuerza bruta.

Seguridad de Capa de TransporteCifrado SSL/TLS: Configurado en nginx.conf y guardado en nginx/certs/, garantizando que toda comunicación sea HTTPS.Cabeceras HSTS: Obliga al navegador a usar siempre conexiones seguras.
🚀 Guía de Instalación Paso a PasoPaso 1: Clonar y Preparar SecretosDescarga el código y configura las variables de entorno para cumplir con OWASP A05 (evitar subir secretos al código). 
git clone https://github.com/RepPabloSuarez-17/rugby-app.git cd rugby-app

Crear archivo .env en la raíz
echo "POSTGRES_USER=rugby_admin" > .env echo "POSTGRES_PASSWORD=Vir-24" >> .env echo "POSTGRES_DB=rugby_db" >> .env echo "JWT_SECRET=tu_clave_maestra" >> .env

Paso 2: Generar Certificados de SeguridadCrea los certificados necesarios para que Nginx levante el sitio de forma segura.

mkdir -p nginx/certs openssl req -x509 -nodes -days 365 -newkey rsa:2048
-keyout nginx/certs/rugby.key -out nginx/certs/rugby.crt

Paso 3: Validación con el "Script de Aduana"Antes de realizar cualquier despliegue final o subida a GitHub, ejecuta el script de integridad local. chmod +x verificar_y_subir.sh

./verificar_y_subir.sh

¿Qué hace este script? Reinicia la base de datos db para asegurar puertos limpios.Espera 12 segundos y verifica la salud de las tablas con una consulta SQL directa.

Ejecuta los tests automáticos con pytest.Realiza un curl de seguridad a localhost para validar el estado de Nginx.

📊 Manual de Uso de la AplicaciónRegistro: Crea un usuario en la pestaña "Nuevo Usuario". El sistema te entregará un PIN naranja; anótalo.

Acceso: Introduce tu Usuario, Contraseña y el PIN. El sistema generará un Token JWT que se guarda en el localStorage del navegador.

Gestión: Una vez dentro, podrás dar de alta jugadores en la base de datos PostgreSQL y ver la plantilla actualizada en tiempo real.
Configuración Final Verificada: Puerto 443 expuesto, Puerto 8000 y 5432 protegidos tras el firewall de Docker.

Esta es la sección de Gestión de Copias de Seguridad diseñada específicamente para tu infraestructura. En un entorno profesional blindado, la disponibilidad de los datos es tan importante como su confidencialidad.

Añade este bloque al final de tu README.md para documentar cómo proteger la información de la plantilla ante fallos del sistema.

💾 Gestión de Copias de Seguridad (Backup & Restore)
Para garantizar la disponibilidad (OWASP A00) de la información de los jugadores, hemos definido protocolos de respaldo para el volumen persistente postgres_data.

Copia de Seguridad en Caliente (Hot Backup) Este método permite generar un archivo .sql sin detener los contenedores. Utiliza la herramienta pg_dump interna de la imagen postgres:15-alpine.
Comando para exportar:

Genera un volcado de la base de datos 'rugby_db'
sudo docker exec -t rugby-app-db-1 pg_dump -U rugby_admin rugby_db > backup_rugby_$(date +%F).sql Archivo: El backup se guardará en la raíz de tu VM con la fecha actual.

Seguridad: El archivo generado contiene las sentencias para reconstruir todas las tablas y registros.

Restauración de Datos En caso de corrupción de datos o migración de servidor, sigue estos pasos:
Asegúrate de que el contenedor db esté corriendo.

Ejecuta la importación del archivo:

cat backup_rugby_2026-03-09.sql | sudo docker exec -i rugby-app-db-1 psql -U rugby_admin -d rugby_db

Copia de Seguridad del Volumen (Cold Backup)
Si necesitas hacer una copia física de los archivos de la base de datos almacenados en /var/lib/postgresql/data:

Detener servicios para evitar inconsistencias
sudo docker compose stop db

Crear un comprimido del volumen físico
sudo tar -cvzf backup_volumen_postgres.tar.gz ./postgres_data

Reiniciar servicio
sudo docker compose start db

🛡️ Verificación de Integridad Post-Backup Después de restaurar una copia, es obligatorio ejecutar el Script de Aduana para confirmar que la aplicación sigue siendo funcional:

./verificar_y_subir.sh

Si el script devuelve ✅ Base de datos operativa, la restauración ha sido un éxito.

🚀 Instalación y Puesta en Marcha Sigue estos pasos para desplegar el ecosistema Rugby App Secure en tu propia infraestructura. Esta guía garantiza que las medidas de seguridad se activen desde el primer segundo.

📋 Requisitos Previos Antes de comenzar, asegúrate de tener instalado:

Docker Engine v20.10+ y Docker Compose v2.0+.

Git para la gestión de versiones.

OpenSSL para la generación de la capa de cifrado.

1️⃣ Clonación del Repositorio Descarga el código fuente y accede al directorio raíz del proyecto:

git clone https://github.com/RepPabloSuarez-17/rugby-app.git cd rugby-app

2️⃣ Configuración de Secretos (OWASP A05) Crea un archivo .env para gestionar tus credenciales de forma aislada del código.

Archivo: .env
POSTGRES_USER=rugby_admin POSTGRES_PASSWORD=Vir-24 POSTGRES_DB=rugby_db JWT_SECRET=tu_clave_secreta_maestra_2026 Nota de Seguridad: El archivo .env está incluido en .gitignore para evitar filtraciones en repositorios públicos.

3️⃣ Generación de Certificados SSL (HTTPS) Para habilitar el túnel cifrado en Nginx, genera los certificados en la carpeta correspondiente:

mkdir -p nginx/certs openssl req -x509 -nodes -days 365 -newkey rsa:2048
-keyout nginx/certs/rugby.key
-out nginx/certs/rugby.crt Este paso es obligatorio para que el contenedor frontend arranque correctamente.

4️⃣ Validación e Integridad (Script de Aduana) No lances la aplicación sin antes verificar que todo el "blindaje" es funcional. Ejecuta el script de validación automatizada:

chmod +x verificar_y_subir.sh ./verificar_y_subir.sh ¿Qué está ocurriendo internamente?:

Reinicio de DB: Se levanta una instancia limpia de Postgres.

Health Check: El script espera 12 segundos y verifica las tablas mediante SQL.

Pruebas Pytest: Se valida la lógica de la API y la conexión a la base de datos.

CURL Check: Se verifica que Nginx responde con un estado 200 OK vía HTTPS.

5️⃣ Lanzamiento Final

Una vez que el script de aduana dé el visto bueno (✅ Todo OK), la aplicación estará lista en segundo plano:

sudo docker-compose up -d --build

🔍 Verificación del Despliegue Para confirmar que los 4 servicios están operativos y aislados en la red rugby-net, ejecuta:

sudo docker ps Acceso Final:

Frontend: https://localhost (o tu IP asignada).

API Docs: https://[ip_maquina / o_ip_app]/api/docs.
