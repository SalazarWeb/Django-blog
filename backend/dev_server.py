#!/usr/bin/env python3
"""
Script de conveniencia para manejar el servidor de desarrollo Django
Uso: python3 dev_server.py [start|stop|restart|status]
"""
import os
import sys
import subprocess
import signal
import time
from pathlib import Path

# Configuración
HOST = '0.0.0.0'
PORT = '8000'
PID_FILE = Path(__file__).parent / 'django_server.pid'

def get_server_pid():
    """Obtiene el PID del servidor si está corriendo"""
    if PID_FILE.exists():
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            # Verificar si el proceso existe
            os.kill(pid, 0)
            return pid
        except (ValueError, OSError):
            # El archivo PID existe pero el proceso no
            PID_FILE.unlink()
    return None

def start_server():
    """Inicia el servidor Django"""
    if get_server_pid():
        print("El servidor ya está corriendo!")
        return
    
    print(f"Iniciando servidor Django en http://{HOST}:{PORT}")
    
    # Ejecutar migraciones automáticamente
    print("Aplicando migraciones...")
    subprocess.run(['python3', 'manage.py', 'migrate'], check=True)
    
    # Iniciar servidor en background
    process = subprocess.Popen(
        ['python3', 'manage.py', 'runserver', f'{HOST}:{PORT}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Guardar PID
    with open(PID_FILE, 'w') as f:
        f.write(str(process.pid))
    
    print(f"Servidor iniciado con PID {process.pid}")
    print(f"Accesible en: http://localhost:{PORT}")
    print(f"API disponible en: http://localhost:{PORT}/api/")
    
    # Esperar un poco y verificar que el servidor esté corriendo
    time.sleep(2)
    if get_server_pid():
        print("Servidor verificado y funcionando correctamente")
    else:
        print("Error al iniciar el servidor")

def stop_server():
    """Detiene el servidor Django"""
    pid = get_server_pid()
    if not pid:
        print("El servidor no está corriendo")
        return
    
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        
        # Verificar si se detuvo
        try:
            os.kill(pid, 0)
            # Si llegamos aquí, el proceso sigue vivo, forzar
            os.kill(pid, signal.SIGKILL)
            print("Servidor detenido forzadamente")
        except OSError:
            print("Servidor detenido correctamente")
            
    except OSError:
        print("Error al detener el servidor")
    
    # Limpiar archivo PID
    if PID_FILE.exists():
        PID_FILE.unlink()

def restart_server():
    """Reinicia el servidor Django"""
    print("Reiniciando servidor...")
    stop_server()
    time.sleep(1)
    start_server()

def server_status():
    """Muestra el estado del servidor"""
    pid = get_server_pid()
    if pid:
        print(f"Servidor corriendo con PID {pid}")
        print(f"Disponible en: http://localhost:{PORT}")
    else:
        print("Servidor detenido")

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 dev_server.py [start|stop|restart|status]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'start':
        start_server()
    elif command == 'stop':
        stop_server()
    elif command == 'restart':
        restart_server()
    elif command == 'status':
        server_status()
    else:
        print("Comando no reconocido. Usa: start, stop, restart, o status")
        sys.exit(1)

if __name__ == '__main__':
    main()