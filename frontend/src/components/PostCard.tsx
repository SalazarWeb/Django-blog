import { Link } from 'react-router-dom';
import type { FilePost } from '../types';
import './PostCard.css';

interface PostCardProps {
  post: FilePost;
}

const PostCard = ({ post }: PostCardProps) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <article className="post-card">
      {post.featured_image && (
        <div className="post-image">
          <img src={post.featured_image} alt={post.title} />
        </div>
      )}
      
      <div className="post-content">
        <div className="post-meta">
          <span className="post-category">{post.category}</span>
          <span className="post-date">{formatDate(post.published_at || post.created_at)}</span>
        </div>
        
        <h2 className="post-title">
          <Link to={`/post/${post.slug}`}>{post.title}</Link>
        </h2>
        
        <p className="post-excerpt">{post.excerpt}</p>
        
        <div className="post-footer">
          <span className="post-author">Por {post.author}</span>
          {post.tags && post.tags.length > 0 && (
            <div className="post-tags">
              {post.tags.map((tag, index) => (
                <span key={index} className="tag">#{tag}</span>
              ))}
            </div>
          )}
        </div>
      </div>
    </article>
  );
};

export default PostCard;