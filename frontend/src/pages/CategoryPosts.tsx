import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import type { FilePost, FileCategory } from '../types';
import fileService from '../services/api';
import PostCard from '../components/PostCard';

const CategoryPosts = () => {
  const { categoryName } = useParams<{ categoryName: string }>();
  const [posts, setPosts] = useState<FilePost[]>([]);
  const [category, setCategory] = useState<FileCategory | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCategoryPosts = async () => {
      if (!categoryName) return;
      
      try {
        setLoading(true);
        const decodedCategoryName = decodeURIComponent(categoryName);
        const data = await fileService.getPostsByCategory(decodedCategoryName);
        setPosts(data.posts);
        setCategory(data.category);
      } catch (err) {
        setError('Error al cargar los posts de la categoría');
        console.error('Error fetching category posts:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCategoryPosts();
  }, [categoryName]);

  if (loading) {
    return (
      <div className="category-posts">
        <div className="container">
          <div className="loading">Cargando...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="category-posts">
        <div className="container">
          <div className="error">{error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="category-posts">
      <div className="container">
        <div className="category-header">
          <h1>Categoría: {category?.name}</h1>
          <p className="posts-count">{posts.length} artículo(s) encontrado(s)</p>
        </div>

        <div className="posts-grid">
          {posts.length > 0 ? (
            posts.map(post => (
              <PostCard key={post.id} post={post} />
            ))
          ) : (
            <p>No hay artículos en esta categoría.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default CategoryPosts;