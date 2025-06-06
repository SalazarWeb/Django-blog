// Tipos principales para el sistema de archivos
export interface FileCategory {
  name: string;
}

export interface FilePost {
  id: number;
  title: string;
  slug: string;
  author: string; // En archivos es string, no objeto
  content: string;
  raw_content?: string; // Contenido markdown original
  excerpt: string;
  featured_image?: string;
  category: string; // En archivos es string, no objeto
  status: 'draft' | 'published';
  created_at: string;
  updated_at?: string;
  published_at?: string;
  tags?: string[];
  file_path?: string;
  file_type?: 'markdown' | 'json';
}