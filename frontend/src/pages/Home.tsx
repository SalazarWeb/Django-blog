import { useState, useEffect } from 'react';
import type { FilePost, FileCategory } from '../types';
import fileService from '../services/api';
import PostCard from '../components/PostCard';
import './Home.css';

const Home = () => {
  const [posts, setPosts] = useState<FilePost[]>([]);
  const [categories, setCategories] = useState<FileCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null); // Limpiar errores previos
        
        const [postsResponse, categoriesResponse] = await Promise.all([
          fileService.getPosts(),
          fileService.getCategories()
        ]);
        
        setPosts(postsResponse || []);
        setCategories(categoriesResponse || []);
      } catch (err) {
        setError('Error al cargar los datos del blog');
        console.error('Error fetching data:', err);
        // Asegurar que los arrays estén vacíos en caso de error
        setPosts([]);
        setCategories([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="home">
        <div className="container">
          <div className="loading">Cargando...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="home">
        <div className="container">
          <div className="error">
            {error}
            <button 
              onClick={() => window.location.reload()} 
              style={{ marginLeft: '10px', padding: '5px 10px' }}
            >
              Reintentar
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="home">
      <div className="container">
        <div className="hero-section">
          <h1>Bienvenido a Mi Blog</h1>
          <p>Descubre artículos sobre tecnología, programación y desarrollo web</p>
        </div>

        <div className="main-layout">
          <main className="posts-section">
            <h2>Últimos Artículos</h2>
            {posts.length > 0 ? (
              <div className="posts-grid">
                {posts.map(post => (
                  <PostCard key={post.id} post={post} />
                ))}
              </div>
            ) : (
              <p>No hay artículos disponibles.</p>
            )}
          </main>

          <aside className="sidebar">
            <div className="categories-widget">
              <h3>Categorías</h3>
              <ul className="categories-list">
                {Array.isArray(categories) && categories.length > 0 ? (
                  categories.map((category, index) => (
                    <li key={index}>
                      <a href={`/category/${encodeURIComponent(category.name)}`}>
                        {category.name}
                      </a>
                    </li>
                  ))
                ) : (
                  <li>No hay categorías disponibles</li>
                )}
              </ul>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
};

export default Home;