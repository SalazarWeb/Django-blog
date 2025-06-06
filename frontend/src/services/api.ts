import axios from 'axios';
import type { FilePost, FileCategory } from '../types';

const API_BASE_URL = 'http://localhost:8000/api/blog';

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