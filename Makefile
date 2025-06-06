# Makefile para el proyecto Django Blog
# Uso: make [comando]

.PHONY: help start stop restart dev install migrate shell admin clean

# Comandos disponibles
help:
	@echo "🛠️  Comandos disponibles:"
	@echo "  make start     - Iniciar servidor Django"
	@echo "  make stop      - Detener servidor Django"
	@echo "  make restart   - Reiniciar servidor Django"
	@echo "  make dev       - Iniciar entorno completo (Django + React)"
	@echo "  make install   - Instalar dependencias"
	@echo "  make migrate   - Aplicar migraciones"
	@echo "  make shell     - Abrir shell de Django"
	@echo "  make admin     - Crear superusuario"
	@echo "  make clean     - Limpiar archivos temporales"

# Iniciar solo Django
start:
	@echo "🚀 Iniciando servidor Django..."
	@cd backend && python3 manage.py migrate
	@cd backend && python3 manage.py runserver 0.0.0.0:8000

# Detener servidor
stop:
	@echo "🔴 Deteniendo servidores..."
	@pkill -f "manage.py runserver" || echo "Django ya estaba detenido"
	@pkill -f "npm run dev" || echo "React ya estaba detenido"
	@echo "✅ Servidores detenidos"

# Reiniciar servidor
restart: stop start

# Entorno completo de desarrollo
dev:
	@./dev.sh

# Instalar dependencias
install:
	@echo "📦 Instalando dependencias..."
	@cd frontend && npm install
	@echo "✅ Dependencias instaladas"

# Aplicar migraciones
migrate:
	@echo "📦 Aplicando migraciones..."
	@cd backend && python3 manage.py migrate
	@echo "✅ Migraciones aplicadas"

# Shell de Django
shell:
	@cd backend && python3 manage.py shell

# Crear superusuario
admin:
	@cd backend && python3 manage.py createsuperuser

# Limpiar archivos temporales
clean:
	@echo "🧹 Limpiando archivos temporales..."
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Limpieza completada"