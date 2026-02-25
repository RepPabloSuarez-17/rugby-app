🛡️ Especificaciones de Seguridad (Hardening & OWASP)

Este proyecto no solo es funcional, sino que ha sido "blindado" siguiendo el principio de Defensa en Profundidad. A continuación, se detalla la base teórica de las protecciones implementadas.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

1. Gestión de Identidad y Control de Acceso (A01:2021)

La aplicación implementa un sistema de autenticación de múltiples factores (MFA) lógico:

Doble Factor de Autenticación (2FA): Al registrarse, el sistema genera un PIN único de 4 dígitos. Esto añade una capa de seguridad donde, incluso si la contraseña es comprometida, el atacante no puede acceder sin el PIN personal.

Hashing Criptográfico: No guardamos contraseñas. Utilizamos el algoritmo bcrypt con un factor de sal (salt) para proteger los datos contra ataques de tablas arcoíris y colisiones.

Tokens de Sesión (JWT): Implementamos JSON Web Tokens firmados para manejar sesiones sin estado (stateless), lo que evita el secuestro de sesiones tradicional basado en cookies.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

2. Protección de la Capa de Transporte (HTTPS/TLS)

Toda la comunicación entre el cliente y el servidor está cifrada para evitar ataques de Man-in-the-Middle (MitM):

Cifrado en Tránsito: Mediante certificados SSL/TLS, garantizamos que los datos viajen de forma privada.

HSTS (HTTP Strict Transport Security): Esta cabecera informa al navegador que solo debe comunicarse con este servidor mediante HTTPS, evitando ataques de degradación de protocolo (Downgrade attacks).

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

3. Seguridad en el Servidor Web (Nginx Hardening)

Nginx no solo sirve la web, actúa como un "escudo" mediante cabeceras de seguridad OWASP:

CSP (Content Security Policy): Una política estricta que define qué scripts, estilos e imágenes se pueden cargar. Esto mitiga casi por completo ataques de XSS (Cross-Site Scripting) al prohibir la ejecución de código inyectado desde fuentes no autorizadas.

X-Content-Type-Options: Previene el "MIME-sniffing", obligando al navegador a respetar el tipo de contenido enviado por el servidor y evitando que ejecute archivos maliciosos disfrazados de imágenes.

X-Frame-Options: Establecida en DENY para evitar el Clickjacking, impidiendo que la aplicación sea embebida en marcos (iframes) de sitios maliciosos.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

4. Control de Tasa y Fuerza Bruta (Rate Limiting)

Para proteger los puntos de entrada (login y registro), hemos implementado:

Limitación de Peticiones: El backend restringe a un máximo de 5 intentos por minuto por dirección IP. Esto hace que los ataques de fuerza bruta automatizados sean ineficaces.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

5. Aislamiento y Menor Privilegio (Docker Security)

La seguridad no se limita al código, también al entorno de ejecución:

Usuario No-Root: Dentro del contenedor Docker, la aplicación no corre con privilegios de administrador. Si un atacante lograra vulnerar la API, sus acciones estarían limitadas por los permisos del usuario rugbyuser.

Segmentación de Red: Los contenedores están aislados en una red privada virtual (rugby-net). La base de datos no es accesible desde el exterior, solo la API puede hablar con ella.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

6. Integridad y Pruebas (CI/CD)

Implementamos Integridad de Código mediante GitHub Actions:

Pruebas Automatizadas: Cada cambio en el código es validado por una suite de tests antes de ser considerado seguro para producción, asegurando que nuevas funcionalidades no rompan las protecciones existentes.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🏉 Rugby App Secure - Manual de Despliegue Seguro

Este proyecto es una plataforma de gestión de rugby blindada bajo estándares OWASP. Utiliza una arquitectura de microservicios orquestada con Docker, garantizando el aislamiento de datos y la protección contra ataques comunes.

📋 Requisitos del Sistema

Antes de iniciar, el sistema debe contar con:

Docker Engine v20.10+ y Docker Compose v2.0+ (evita versiones antiguas para prevenir errores de compatibilidad).

Git para la gestión del código.

OpenSSL para la generación de certificados de seguridad.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🚀 Guía de Instalación Paso a Paso

1. Clonar el Repositorio

Descarga el código fuente y accede al directorio raíz:

git clone https://github.com/[tu_nombre_github]/[nombre_app]-app.git

cd nombre_app

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

2. Configuración de Secretos (OWASP A05)

Crea un archivo .env en la raíz para gestionar credenciales sensibles sin exponerlas en el código.

# Contenido recomendado para .env

POSTGRES_USER=[tu_usuario_db]

POSTGRES_PASSWORD=[tu_contraseña_db]

POSTGRES_DB=[tu_nombre_db]

JWT_SECRET=tu_clave_secreta_maestra

Nota: El archivo .env ya está pre-configurado en el .gitignore para no ser subido a GitHub.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

3. Generación de Certificados SSL/TLS

Para habilitar el cifrado HTTPS (obligatorio en esta app), genera los certificados en la carpeta correspondiente:

mkdir -p nginx/certs

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/certs/[tu_nombre_de_certificado].key -out nginx/certs/[tu_nombre_de_certificado].crt

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

4. Despliegue de la Infraestructura

Levanta los 4 servicios integrados (PostgreSQL, Redis, FastAPI y Nginx) en su red interna aislada:

sudo docker compose up -d --build

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🛡️ Medidas de Seguridad Implementadas

A. Capa de Infraestructura y Red

Red Privada Aislada: Los servicios se comunican a través de la red rugby-net (172.20.0.0/16).

IPs Fijas: Cada contenedor tiene asignada una IP estática interna para evitar ataques de redirección.

Usuario No-Root: El contenedor de la API corre bajo el usuario rugbyuser, minimizando riesgos en caso de brecha.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🛡️ Security Specifications (Hardening & OWASP)
This project is not only functional but has been "hardened" following the Defense in Depth principle. Below are the theoretical foundations of the implemented protections.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

1. Identity Management and Access Control (A01:2021)
The application implements a logical Multi-Factor Authentication (MFA) system:

Two-Factor Authentication (2FA): Upon registration, the system generates a unique 4-digit PIN. This adds a security layer where, even if a password is compromised, an attacker cannot gain access without the personal PIN.

Cryptographic Hashing: We do not store plain-text passwords. We use the bcrypt algorithm with a salt factor to protect data against rainbow table and collision attacks.

Session Tokens (JWT): We implement signed JSON Web Tokens to handle stateless sessions, preventing traditional cookie-based session hijacking.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

2. Transport Layer Protection (HTTPS/TLS)
All communication between the client and the server is encrypted to prevent Man-in-the-Middle (MitM) attacks:

Encryption in Transit: Through SSL/TLS certificates, we ensure that data travels privately.

HSTS (HTTP Strict Transport Security): This header informs the browser to only communicate with this server via HTTPS, preventing protocol downgrade attacks.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

3. Web Server Security (Nginx Hardening)
Nginx acts as a "shield" using OWASP security headers:

CSP (Content Security Policy): A strict policy defining which scripts, styles, and images can be loaded. This nearly eliminates XSS (Cross-Site Scripting) attacks by prohibiting the execution of injected code from unauthorized sources.

X-Content-Type-Options: Prevents "MIME-sniffing," forcing the browser to respect the content type sent by the server and preventing it from executing malicious files disguised as images.

X-Frame-Options: Set to DENY to prevent Clickjacking, stopping the application from being embedded in iframes on malicious sites.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

4. Rate Limiting and Brute Force Control
To protect entry points (login and registration), we have implemented:

Request Throttling: The backend restricts access to a maximum of 5 attempts per minute per IP address. This renders automated brute-force attacks ineffective.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

5. Isolation and Least Privilege (Docker Security)
Security extends to the execution environment:

Non-Root User: Inside the Docker container, the application does not run with administrative privileges. If an attacker compromises the API, their actions are limited by the permissions of the rugbyuser.

Network Segmentation: Containers are isolated in a virtual private network (rugby-net). The database is not accessible from the outside; only the API can communicate with it.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

6. Integrity and Testing (CI/CD)
We implement code integrity through GitHub Actions:

Automated Testing: Every code change is validated by a test suite before being considered production-ready, ensuring that new features do not break existing security protections.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🏉 Rugby App Secure - Deployment Manual
This project is a rugby management platform hardened under OWASP standards. It uses a microservices architecture orchestrated with Docker, ensuring data isolation and protection against common attacks.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

📋 System Requirements
Before starting, ensure the system has:

Docker Engine v20.10+ and Docker Compose v2.0+ (avoid older versions to prevent compatibility errors).

Git for code management.

OpenSSL for security certificate generation.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🚀 Step-by-Step Installation Guide
1. Clone the Repository
   
Download the source code and enter the root directory:

git clone https://github.com/[your_github_username]/[app_name]-app.git

cd app_name

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

2. Secret Configuration (OWASP A05)
   
Create a .env file in the root to manage sensitive credentials without exposing them in the code.

# Recommended .env content
POSTGRES_USER=[your_db_user]
POSTGRES_PASSWORD=[your_db_password]
POSTGRES_DB=[your_db_name]
JWT_SECRET=your_master_secret_key
Note: The .env file is pre-configured in .gitignore to prevent it from being uploaded to GitHub.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

3. SSL/TLS Certificate Generation
To enable mandatory HTTPS, generate certificates in the appropriate folder:

mkdir -p nginx/certs

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/certs/[cert_name].key -out nginx/certs/[cert_name].crt

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

4. Infrastructure Deployment
Launch the 4 integrated services (PostgreSQL, Redis, FastAPI, and Nginx) in their isolated network:
sudo docker compose up -d --build

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🛠️ Validation Environment Setup (Virtual Machine)
To ensure the code is secure and functional before reaching the public repository, you have configured a Local Continuous Integrity environment based on these pillars:

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

1. Execution Environment and Dependencies
Your VM acts as a "mirror" of the Docker production environment:

Docker Engine & Compose V2: Installed to support the orchestration of the 4 services.

Python 3.11 Environment: Configured to run pytest and necessary libraries like httpx and sqlalchemy.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

2. The Custom Script: verificar_y_subir.sh
This script acts as the final security filter, automating total verification before allowing a push:

Clean Restart: Stops previous instances and launches the DB in isolation to ensure port 5432 is free for testing.

DB Health Check: Implements a 12-second sleep and a direct SQL query to confirm tables were created correctly.

Code Integrity Tests: Runs pytest on the backend. Any failure stops the process immediately (exit 1), preventing errors from reaching GitHub.

Web Server Validation: Uses curl on port 443 (HTTPS) to verify Nginx responds with 200 OK and valid SSL certificates.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

3. Hardened Synchronization with GitHub
Once the local script gives the "green light," the upload is automated:

Git Automation: Executes git add ., git commit, and git push automatically.

Secret Protection: Certificates and .env files are never indexed by Git, complying with OWASP A05.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🔐 CI/CD Secret Management (GitHub Secrets)
To comply with OWASP A05, sensitive data (like JWT_SECRET) must never be written directly in Workflow files.

1. GitHub Secrets Interface
Configure these in your GitHub repository under Settings > Secrets and variables > Actions:

POSTGRES_USER: Database user defined in database.py.

POSTGRES_PASSWORD: Your secure database password.

JWT_SECRET: Master key for signing security tokens.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

2. Workflow Injection
In tests.yml, secrets are invoked using ${{ secrets.SECRET_NAME }}. This allows pytest to access the test database without exposing real passwords.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🛠️ Local vs. GitHub Workflow
Step 1 (Your VM): Run verificar_y_subir.sh. It uses your local .env (hidden from Git) to validate the VM environment.

Step 2 (GitHub): Upon push, GitHub Actions takes over. It uses GitHub Secrets to run pytest and provide the final "Build Success" badge.

Security Benefit: This design ensures that anyone cloning the repo cannot see your keys, as neither the .env nor the GitHub Secrets are visible to third parties.

Final Access: Once deployed, access the platform at https://[your_ip].
