import os
import markdown
import frontmatter
from pathlib import Path
from django.conf import settings
from datetime import datetime
from typing import List, Dict, Optional

class FilePostService:
    """
    Servicio para manejar posts almacenados como archivos .md
    """
    
    def __init__(self):
        # Apuntar a la carpeta posts_data en el directorio raíz del proyecto
        self.posts_directory = Path(settings.BASE_DIR).parent / 'posts_data'
        self.ensure_posts_directory()
    
    def ensure_posts_directory(self):
        """Asegurar que el directorio de posts existe"""
        self.posts_directory.mkdir(exist_ok=True)
    
    def get_all_posts(self) -> List[Dict]:
        """Obtener todos los posts desde archivos Markdown"""
        posts = []
        
        # Buscar solo archivos .md en el directorio
        for file_path in self.posts_directory.glob('*.md'):
            post_data = self._load_markdown_post(file_path)
            if post_data:
                posts.append(post_data)
        
        # Ordenar por fecha de creación (más recientes primero)
        posts.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return posts
    
    def get_post_by_slug(self, slug: str) -> Optional[Dict]:
        """Obtener un post específico por su slug"""
        posts = self.get_all_posts()
        for post in posts:
            if post.get('slug') == slug:
                return post
        return None
    
    def get_posts_by_category(self, category: str) -> List[Dict]:
        """Obtener posts filtrados por categoría"""
        posts = self.get_all_posts()
        return [post for post in posts if post.get('category', '').lower() == category.lower()]
    
    def search_posts(self, query: str) -> List[Dict]:
        """Buscar posts por título o contenido"""
        posts = self.get_all_posts()
        query = query.lower()
        results = []
        
        for post in posts:
            title = post.get('title', '').lower()
            content = post.get('content', '').lower()
            excerpt = post.get('excerpt', '').lower()
            
            if query in title or query in content or query in excerpt:
                results.append(post)
        
        return results
    
    def get_categories(self) -> List[str]:
        """Obtener todas las categorías únicas"""
        posts = self.get_all_posts()
        categories = set()
        
        for post in posts:
            category = post.get('category')
            if category:
                categories.add(category)
        
        return sorted(list(categories))
    
    def _load_markdown_post(self, file_path: Path) -> Dict:
        """Cargar post desde archivo Markdown con frontmatter"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            # Convertir Markdown a HTML
            html_content = markdown.markdown(post.content, extensions=['codehilite', 'fenced_code'])
            
            # Extraer metadatos del frontmatter
            metadata = post.metadata
            
            return {
                'id': self._generate_id_from_filename(file_path.stem),
                'title': metadata.get('title', file_path.stem),
                'slug': metadata.get('slug', file_path.stem),
                'content': html_content,
                'raw_content': post.content,  # Contenido markdown original
                'excerpt': metadata.get('excerpt', self._generate_excerpt(post.content)),
                'category': metadata.get('category', 'General'),
                'author': metadata.get('author', 'Admin'),
                'featured_image': metadata.get('featured_image', ''),
                'status': metadata.get('status', 'published'),
                'created_at': self._parse_date(metadata.get('created_at', file_path.stat().st_ctime)),
                'updated_at': self._parse_date(metadata.get('updated_at', file_path.stat().st_mtime)),
                'published_at': self._parse_date(metadata.get('published_at', metadata.get('created_at', file_path.stat().st_ctime))),
                'tags': metadata.get('tags', []),
                'file_path': str(file_path),
                'file_type': 'markdown'
            }
        except Exception as e:
            print(f"Error cargando archivo {file_path}: {e}")
            return None
    
    def _generate_id_from_filename(self, filename: str) -> int:
        """Generar un ID único basado en el nombre del archivo"""
        return hash(filename) % (10**8)
    
    def _generate_excerpt(self, content: str, max_length: int = 300) -> str:
        """Generar excerpt automático desde el contenido"""
        # Limpiar markdown básico
        import re
        clean_content = re.sub(r'[#*`\[\]()]', '', content)
        clean_content = ' '.join(clean_content.split())
        
        if len(clean_content) <= max_length:
            return clean_content
        
        return clean_content[:max_length] + '...'
    
    def _parse_date(self, date_value) -> str:
        """Parsear fecha a formato ISO"""
        if isinstance(date_value, (int, float)):
            # Unix timestamp
            return datetime.fromtimestamp(date_value).isoformat()
        elif isinstance(date_value, str):
            try:
                # Intentar parsear como ISO date
                return datetime.fromisoformat(date_value.replace('Z', '+00:00')).isoformat()
            except:
                return datetime.now().isoformat()
        elif hasattr(date_value, 'isoformat'):
            return date_value.isoformat()
        else:
            return datetime.now().isoformat()