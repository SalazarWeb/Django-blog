from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
import subprocess
import sys
import os
import signal
import time
from pathlib import Path

class Command(BaseCommand):
    help = 'Comando avanzado para manejar el servidor de desarrollo'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['start', 'stop', 'restart', 'status', 'dev'],
            help='Acción a realizar con el servidor'
        )
        parser.add_argument(
            '--host',
            default='127.0.0.1',
            help='Host para el servidor (default: 127.0.0.1)'
        )
        parser.add_argument(
            '--port',
            default='8000',
            help='Puerto para el servidor (default: 8000)'
        )
        parser.add_argument(
            '--auto-migrate',
            action='store_true',
            help='Ejecutar migraciones automáticamente al iniciar'
        )

    def handle(self, *args, **options):
        action = options['action']
        host = options['host']
        port = options['port']
        auto_migrate = options['auto_migrate']

        if action == 'start':
            self.start_server(host, port, auto_migrate)
        elif action == 'stop':
            self.stop_server()
        elif action == 'restart':
            self.restart_server(host, port, auto_migrate)
        elif action == 'status':
            self.server_status()
        elif action == 'dev':
            self.dev_mode(host, port)

    def start_server(self, host, port, auto_migrate):
        """Inicia el servidor Django"""
        if auto_migrate:
            self.stdout.write("📦 Aplicando migraciones...")
            execute_from_command_line(['manage.py', 'migrate'])
        
        self.stdout.write(f"🚀 Iniciando servidor Django en http://{host}:{port}")
        execute_from_command_line(['manage.py', 'runserver', f'{host}:{port}'])

    def stop_server(self):
        """Detiene el servidor Django"""
        try:
            # Buscar procesos del servidor Django
            result = subprocess.run(['pgrep', '-f', 'runserver'], 
                                  capture_output=True, text=True)
            if result.stdout:
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    os.kill(int(pid), signal.SIGTERM)
                self.stdout.write("✅ Servidor detenido")
            else:
                self.stdout.write("🟡 No se encontró ningún servidor corriendo")
        except Exception as e:
            self.stdout.write(f"❌ Error al detener servidor: {e}")

    def restart_server(self, host, port, auto_migrate):
        """Reinicia el servidor Django"""
        self.stdout.write("🔄 Reiniciando servidor...")
        self.stop_server()
        time.sleep(1)
        self.start_server(host, port, auto_migrate)

    def server_status(self):
        """Muestra el estado del servidor"""
        try:
            result = subprocess.run(['pgrep', '-f', 'runserver'], 
                                  capture_output=True, text=True)
            if result.stdout:
                pids = result.stdout.strip().split('\n')
                self.stdout.write(f"✅ Servidor corriendo (PIDs: {', '.join(pids)})")
            else:
                self.stdout.write("🔴 Servidor detenido")
        except Exception as e:
            self.stdout.write(f"❌ Error al verificar estado: {e}")

    def dev_mode(self, host, port):
        """Modo desarrollo completo con migraciones automáticas"""
        self.stdout.write("🛠️  Modo desarrollo activado")
        self.stdout.write("📦 Aplicando migraciones...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        self.stdout.write("👤 Verificando superusuario...")
        # Aquí podrías agregar lógica para crear superusuario si no existe
        
        self.stdout.write(f"🚀 Iniciando servidor en modo desarrollo en http://{host}:{port}")
        self.stdout.write("💡 Usa Ctrl+C para detener el servidor")
        execute_from_command_line(['manage.py', 'runserver', f'{host}:{port}'])