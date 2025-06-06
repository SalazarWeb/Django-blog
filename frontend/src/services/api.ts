import axios from 'axios';
import type { FilePost, FileCategory } from '../types';

// Configuración de URL base dependiendo del entorno
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://your-backend-app.onrender.com/api/blog'  // Cambia esto por tu URL de backend en Render
  : 'http://localhost:8000/api/blog';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Servicio principal para archivos
export const fileService = {
  // Posts desde archivos
  async getPosts(): Promise<FilePost[]> {
    const response = await api.get('/files/posts/');
    return response.data;
  },

  async getPost(slug: string): Promise<FilePost> {
    const response = await api.get(`/files/posts/${slug}/`);
    return response.data;
  },

  async getLatestPosts(): Promise<FilePost[]> {
    const response = await api.get('/files/latest/');
    return response.data;
  },

  async searchPosts(query: string): Promise<FilePost[]> {
    const response = await api.get(`/files/search/?q=${encodeURIComponent(query)}`);
    return response.data;
  },

  // Categorías desde archivos
  async getCategories(): Promise<FileCategory[]> {
    const response = await api.get('/files/categories/');
    return response.data;
  },

  async getPostsByCategory(categoryName: string): Promise<{ category: FileCategory; posts: FilePost[] }> {
    const response = await api.get(`/files/categories/${encodeURIComponent(categoryName)}/posts/`);
    return response.data;
  },
};

// Exportar fileService como el servicio principal
export default fileService;