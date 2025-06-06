#!/bin/bash

# Script de desarrollo completo para Django + React
# Uso: ./dev.sh

echo "Iniciando entorno de desarrollo completo..."

# Función para manejar la limpieza al salir
cleanup() {
    echo ""
    echo "Limpiando procesos..."
    pkill -f "manage.py runserver"
    pkill -f "npm run dev"
    pkill -f "vite"
    echo "Procesos detenidos"
    exit 0
}

# Configurar trap para limpieza
trap cleanup SIGINT SIGTERM

# Obtener el directorio base del script (absoluto)
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

# Iniciar backend Django
echo "Iniciando backend Django..."
cd "$BASE_DIR/backend"
echo "Aplicando migraciones..."
python3 manage.py migrate

echo "Iniciando servidor Django en http://localhost:8000"
python3 manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Esperar un poco para que Django se inicie
sleep 3

# Iniciar frontend React
echo "Iniciando frontend React..."
cd "$BASE_DIR/frontend"

if [ ! -d "node_modules" ]; then
    echo "Instalando dependencias de Node.js..."
    npm install
fi

echo "Iniciando servidor de desarrollo React en http://localhost:5173"
npm run dev &
REACT_PID=$!

echo ""
echo "Entorno de desarrollo iniciado:"
echo "   Backend Django: http://localhost:8000"
echo "   Frontend React: http://localhost:5173"
echo "   API: http://localhost:8000/api/"
echo ""
echo "Presiona Ctrl+C para detener ambos servidores"

# Esperar a que uno de los procesos termine
wait