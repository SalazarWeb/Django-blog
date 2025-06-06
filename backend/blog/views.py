from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    FilePostListSerializer, FilePostDetailSerializer, FileCategorySerializer
)
from .file_post_service import FilePostService

# Vistas principales que usan archivos
class FilePostListView(generics.GenericAPIView):
    """Vista para listar posts desde archivos"""
    serializer_class = FilePostListSerializer
    
    def get(self, request):
        file_service = FilePostService()
        posts = file_service.get_all_posts()
        
        # Filtrar por categoría si se especifica
        category = request.query_params.get('category', None)
        if category:
            posts = file_service.get_posts_by_category(category)
        
        # Filtrar solo posts publicados
        posts = [post for post in posts if post.get('status') == 'published']
        
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)


class FilePostDetailView(generics.GenericAPIView):
    """Vista para detalle de post desde archivo"""
    serializer_class = FilePostDetailSerializer
    
    def get(self, request, slug):
        file_service = FilePostService()
        post = file_service.get_post_by_slug(slug)
        
        if not post:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if post.get('status') != 'published':
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(post)
        return Response(serializer.data)


class FileCategoryListView(generics.GenericAPIView):
    """Vista para listar categorías desde archivos"""
    serializer_class = FileCategorySerializer
    
    def get(self, request):
        file_service = FilePostService()
        categories = file_service.get_categories()
        
        # Convertir a formato esperado por el serializer
        category_data = [{'name': cat} for cat in categories]
        
        serializer = self.serializer_class(category_data, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def file_posts_by_category(request, category_name):
    """Obtener posts por categoría desde archivos"""
    file_service = FilePostService()
    posts = file_service.get_posts_by_category(category_name)
    
    # Filtrar solo posts publicados
    posts = [post for post in posts if post.get('status') == 'published']
    
    serializer = FilePostListSerializer(posts, many=True)
    return Response({
        'category': {'name': category_name},
        'posts': serializer.data
    })


@api_view(['GET'])
def file_latest_posts(request):
    """Obtener últimos posts desde archivos"""
    file_service = FilePostService()
    posts = file_service.get_all_posts()
    
    # Filtrar solo posts publicados y tomar los primeros 5
    published_posts = [post for post in posts if post.get('status') == 'published'][:5]
    
    serializer = FilePostListSerializer(published_posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def file_search_posts(request):
    """Buscar posts desde archivos"""
    query = request.query_params.get('q', '')
    if query:
        file_service = FilePostService()
        posts = file_service.search_posts(query)
         
        posts = [post for post in posts if post.get('status') == 'published']
        
        serializer = FilePostListSerializer(posts, many=True)
        return Response(serializer.data)
    return Response([])
