import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import type { FilePost } from '../types';
import fileService from '../services/api';
import PostCard from '../components/PostCard';

const SearchResults = () => {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q') || '';
  const [posts, setPosts] = useState<FilePost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSearchResults = async () => {
      if (!query) {
        setPosts([]);
        setLoading(false);
        return;
      }
      
      try {
        setLoading(true);
        const results = await fileService.searchPosts(query);
        setPosts(results);
      } catch (err) {
        setError('Error al realizar la búsqueda');
        console.error('Error searching posts:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSearchResults();
  }, [query]);

  if (loading) {
    return (
      <div className="search-results">
        <div className="container">
          <div className="loading">Buscando...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="search-results">
        <div className="container">
          <div className="error">{error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="search-results">
      <div className="container">
        <div className="search-header">
          <h1>Resultados de búsqueda</h1>
          <p className="search-query">
            Buscando: "<strong>{query}</strong>"
          </p>
          <p className="results-count">
            {posts.length} resultado(s) encontrado(s)
          </p>
        </div>

        <div className="posts-grid">
          {posts.length > 0 ? (
            posts.map(post => (
              <PostCard key={post.id} post={post} />
            ))
          ) : (
            <div className="no-results">
              <p>No se encontraron artículos que coincidan con tu búsqueda.</p>
              <p>Intenta con otros términos de búsqueda.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SearchResults;