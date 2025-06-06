# Sistema de Posts desde Archivos

## Nuevo Sistema Implementado!

Tu blog ahora puede leer posts directamente desde archivos `.md` y `.json` en lugar de depender únicamente de la base de datos. Esto te da mayor flexibilidad y control sobre tu contenido.

## Estructura de Archivos

Los posts se almacenan en: `backend/posts_data/`

### Formato Markdown (.md)

```markdown
---
title: "Tu título aquí"
slug: "tu-slug-unico"
author: "Tu nombre"
category: "Categoría"
excerpt: "Descripción corta del post"
status: "published"
created_at: "2025-06-06T10:00:00"
tags: ["tag1", "tag2", "tag3"]
---

# Tu Contenido en Markdown

Aquí va el contenido de tu post en **Markdown**.

## Subtítulo

- Lista de elementos
- Otro elemento

```code
Bloques de código también funcionan
```
```

### Formato JSON (.json)

```json
{
  "title": "Tu título aquí",
  "slug": "tu-slug-unico", 
  "author": "Tu nombre",
  "category": "Categoría",
  "excerpt": "Descripción corta del post",
  "status": "published",
  "created_at": "2025-06-06T10:00:00",
  "content_type": "markdown",
  "content": "# Tu Contenido\n\nContenido en Markdown aquí...",
  "tags": ["tag1", "tag2"]
}
```

## APIs Disponibles

### Nuevas APIs (Sistema Principal)
- `GET /api/blog/files/posts/` - Lista todos los posts
- `GET /api/blog/files/posts/{slug}/` - Detalle de un post
- `GET /api/blog/files/categories/` - Lista de categorías
- `GET /api/blog/files/latest/` - Últimos 5 posts
- `GET /api/blog/files/search/?q=término` - Búsqueda

### APIs Originales (Compatibilidad)
- Las APIs originales siguen funcionando para posts en la base de datos

## Flujo de Trabajo

1. **Crear posts**: Agrega archivos `.md` o `.json` en `backend/posts_data/`
2. **Automático**: El sistema los lee sin necesidad de reiniciar
3. **Publicar**: Cambia `status` a `"published"` para hacer visible el post
4. **Editar**: Modifica el archivo directamente y los cambios aparecen inmediatamente

## Ventajas del Nuevo Sistema

- **Control de versiones**: Usa Git para versionar tus posts
- **Portabilidad**: Archivos independientes de la base de datos  
- **Simplicidad**: Edita con cualquier editor de texto
- **Backup fácil**: Solo respalda la carpeta `posts_data/`
- **Markdown nativo**: Soporte completo para Markdown con sintaxis highlighting
- **Tags**: Sistema de etiquetas integrado
- **Búsqueda avanzada**: Busca en título, contenido y excerpt

## Ejemplos Incluidos

He creado dos posts de ejemplo:
- `mi-primer-post.md` - Ejemplo en formato Markdown
- `segundo-post.json` - Ejemplo en formato JSON

## Acceder al Blog

- **Frontend**: http://localhost:5174
- **Backend**: http://localhost:8000
- **API de archivos**: http://localhost:8000/api/blog/files/posts/

¡Tu nuevo sistema de blog basado en archivos está listo para usar!