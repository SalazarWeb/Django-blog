from django.urls import path
from . import views

urlpatterns = [ 
    path('files/posts/', views.FilePostListView.as_view(), name='file-post-list'),
    path('files/posts/<slug:slug>/', views.FilePostDetailView.as_view(), name='file-post-detail'),
    path('files/categories/', views.FileCategoryListView.as_view(), name='file-category-list'),
    path('files/categories/<str:category_name>/posts/', views.file_posts_by_category, name='file-posts-by-category'),
    path('files/latest/', views.file_latest_posts, name='file-latest-posts'),
    path('files/search/', views.file_search_posts, name='file-search-posts'),
]