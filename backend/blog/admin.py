# Admin eliminado - Posts manejados desde archivos
# Si en el futuro necesitas reactivar el admin, descomenta el código siguiente:

# from django.contrib import admin
# from .models import Category, Post, Comment

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'created_at']
#     search_fields = ['name']
#     prepopulated_fields = {}

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ['title', 'author', 'category', 'status', 'created_at', 'published_at']
#     list_filter = ['status', 'category', 'created_at', 'published_at']
#     search_fields = ['title', 'content']
#     prepopulated_fields = {'slug': ('title',)}
#     list_editable = ['status']
#     date_hierarchy = 'created_at'
    
#     fieldsets = (
#         ('Contenido', {
#             'fields': ('title', 'slug', 'content', 'excerpt')
#         }),
#         ('Metadatos', {
#             'fields': ('author', 'category', 'featured_image', 'status')
#         }),
#         ('Fechas', {
#             'fields': ('published_at',),
#             'classes': ('collapse',)
#         })
#     )

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['author_name', 'post', 'created_at', 'is_approved']
#     list_filter = ['is_approved', 'created_at']
#     search_fields = ['author_name', 'author_email', 'content']
#     list_editable = ['is_approved']
#     readonly_fields = ['created_at']
