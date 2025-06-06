from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class SecurityMiddleware(MiddlewareMixin):
    """
    Middleware de seguridad personalizado para el blog.
    """
    
    # Paths bloqueados por seguridad
    BLOCKED_PATHS = [
        '/admin',
        '/phpmyadmin',
        '/wp-admin',
        '/wp-login',
        '/.env',
        '/config',
        '/dashboard',
        '/phpinfo',
        '/mysql',
        '/db',
        '/database',
        '/backup',
        '/panel',
        '/control',
        '/manager',
    ]
    
    # User agents sospechosos
    SUSPICIOUS_USER_AGENTS = [
        'sqlmap',
        'nikto',
        'nmap',
        'masscan',
        'gobuster',
        'dirb',
        'dirbuster',
        'wpscan',
    ]
    
    def process_request(self, request):
        # Verificar paths bloqueados
        path = request.path.lower()
        for blocked_path in self.BLOCKED_PATHS:
            if path.startswith(blocked_path):
                logger.warning(f"Blocked access attempt to {request.path} from {self.get_client_ip(request)}")
                return JsonResponse({
                    'error': 'Access Denied',
                    'message': 'This resource is not available.'
                }, status=403)
        
        # Verificar user agents sospechosos
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        for suspicious_ua in self.SUSPICIOUS_USER_AGENTS:
            if suspicious_ua in user_agent:
                logger.warning(f"Suspicious user agent detected: {user_agent} from {self.get_client_ip(request)}")
                return JsonResponse({
                    'error': 'Access Denied',
                    'message': 'Request blocked for security reasons.'
                }, status=403)
        
        return None
    
    def get_client_ip(self, request):
        """Obtener la IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip