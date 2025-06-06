from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["GET"])
def secure_root_view(request):
    return JsonResponse({
        'message': 'Blog API',
        'version': '1.0'
    })

@csrf_exempt
@require_http_methods(["GET"])
def not_found_view(request, exception=None):
    return JsonResponse({
        'error': 'Not Found',
        'message': 'The requested resource was not found.'
    }, status=404)