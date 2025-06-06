import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import type { FilePost } from '../types';
import fileService from '../services/api';
import './PostDetail.css';

const PostDetail = () => {
  const { slug } = useParams<{ slug: string }>();
  const [post, setPost] = useState<FilePost | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPost = async () => {
      if (!slug) return;
      
      try {
        setLoading(true);
        const postData = await fileService.getPost(slug);
        setPost(postData);
      } catch (err) {
        setError('Post no encontrado');
        console.error('Error fetching post:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [slug]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="post-detail">
        <div className="container">
          <div className="loading">Cargando...</div>
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="post-detail">
        <div className="container">
          <div className="error">{error || 'Post no encontrado'}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="post-detail">
      <div className="container">
        <article className="post-article">
          <header className="post-header">
            <div className="post-meta">
              <span className="post-category">{post.category}</span>
              <span className="post-date">{formatDate(post.published_at || post.created_at)}</span>
              {post.file_type && (
                <span className="post-file-type">{post.file_type}</span>
              )}
            </div>
            <h1 className="post-title">{post.title}</h1>
            <div className="post-author">
              Por {post.author}
            </div>
            {post.tags && post.tags.length > 0 && (
              <div className="post-tags">
                {post.tags.map((tag, index) => (
                  <span key={index} className="tag">#{tag}</span>
                ))}
              </div>
            )}
          </header>

          {post.featured_image && (
            <div className="post-featured-image">
              <img src={post.featured_image} alt={post.title} />
            </div>
          )}

          <div className="post-content">
            <div dangerouslySetInnerHTML={{ __html: post.content }} />
          </div>

          {post.updated_at && post.updated_at !== post.created_at && (
            <div className="post-updated">
              <small>Última actualización: {formatDate(post.updated_at)}</small>
            </div>
          )}
        </article>
      </div>
    </div>
  );
};

export default PostDetail;