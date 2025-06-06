from rest_framework import serializers


# Serializers para el sistema de archivos (principal)
class FilePostListSerializer(serializers.Serializer):
    """Serializer para lista de posts desde archivos"""
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    author = serializers.CharField()
    excerpt = serializers.CharField()
    featured_image = serializers.CharField(allow_blank=True)
    category = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.CharField()
    published_at = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    file_type = serializers.CharField()


class FilePostDetailSerializer(serializers.Serializer):
    """Serializer para detalle de post desde archivo"""
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    author = serializers.CharField()
    content = serializers.CharField()
    raw_content = serializers.CharField()
    excerpt = serializers.CharField()
    featured_image = serializers.CharField(allow_blank=True)
    category = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.CharField()
    updated_at = serializers.CharField()
    published_at = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    file_path = serializers.CharField()
    file_type = serializers.CharField()


class FileCategorySerializer(serializers.Serializer):
    """Serializer para categorías extraídas de archivos"""
    name = serializers.CharField()