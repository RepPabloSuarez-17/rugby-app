#!/bin/bash
echo "🧪 Sincronizando dependencias y ejecutando Pytest..."

# 1. Instalación de dependencias para el test local
pip install pytest httpx sqlalchemy psycopg2-binary > /dev/null 2>&1

# 2. Levantar la base de datos y esperar a que acepte conexiones
sudo docker-compose up -d db
echo "⏳ Esperando a que la base de datos esté lista..."
sleep 8

# 3. Configurar entorno para el test
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
export DB_HOST=localhost

# 4. Ejecutar el test de tu imagen
python3 -m pytest backend/test_main.py

if [ $? -eq 0 ]; then
    echo "✅ Pruebas locales superadas. Verificando App completa..."
    sudo docker-compose up -d --build
    sleep 5
    
    # Verificamos si la web responde por HTTPS
    STATUS=$(curl -o /dev/null -s -w "%{http_code}" -k https://localhost)
    
    if [ "$STATUS" -eq 200 ]; then
        echo "🚀 Todo funcionando. Subiendo cambios a GitHub..."
        git add .
        git commit -m "Fix: Conexión de base de datos validada y botones operativos"
        git push origin main
    else
        echo "❌ ERROR: La web no responde (Status $STATUS). Revisa Nginx."
        exit 1
    fi
else
    echo "❌ ERROR: Pytest ha fallado. Revisa la conexión en backend/database.py"
    exit 1
fi
