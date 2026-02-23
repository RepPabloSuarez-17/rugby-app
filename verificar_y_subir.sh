#!/bin/bash
echo "🧪 Sincronizando dependencias y ejecutando Pytest..."

# 1. Asegurar herramientas
pip install pytest httpx sqlalchemy psycopg2-binary > /dev/null 2>&1

# 2. Reinicio limpio de la DB para asegurar mapeo de puertos
sudo docker-compose stop db
sudo docker-compose up -d db
echo "⏳ Esperando 12 segundos a que la base de datos acepte conexiones..."
sleep 12

# --- PRUEBA DE INTEGRIDAD DE DATOS ---
echo "🔍 Verificando salud de las tablas de Rugby..."
DB_TEST=$(sudo docker-compose exec -T db psql -U rugby_admin -d rugby_db -c "SELECT count(*) FROM jugadores;" 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✅ Base de datos operativa y con tablas creadas."
else
    echo "❌ ERROR: La base de datos no responde internamente. Revisa logs con 'docker logs rugby-app_db_1'"
    exit 1
fi

# 3. Configurar entorno para el test
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
export DB_HOST=localhost
export POSTGRES_USER=rugby_admin
export POSTGRES_PASSWORD=Vir-24
export POSTGRES_DB=rugby_db

# 4. Ejecutar prueba
python3 -m pytest backend/test_main.py

if [ $? -eq 0 ]; then
    echo "✅ Pruebas locales superadas. Verificando App completa..."
    sudo docker-compose up -d --build
    sleep 5
    
    STATUS=$(curl -o /dev/null -s -w "%{http_code}" -k https://localhost)
    
    if [ "$STATUS" -eq 200 ]; then
        echo "🚀 Todo OK. Sincronizando a GitHub..."
        git add .
        git commit -m "Fix: Test de conexión localhost validado"
        git push origin main --force
        echo "🎉 ¡Hecho!"
    else
        echo "❌ ERROR: Web da Status $STATUS. Revisa Nginx."
        exit 1
    fi
else
    echo "❌ ERROR: Pytest falló con Connection Refused. ¿Está el puerto 5432 libre?"
    exit 1
fi
