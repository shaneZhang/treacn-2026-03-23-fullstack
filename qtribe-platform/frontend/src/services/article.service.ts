import { apiService } from './api';
import {
  ApiResponse,
  Article,
  ArticleDetail,
  Comment,
  PaginatedData,
  Tag,
} from '@app-types/index';

export interface CreateArticleData {
  title: string;
  content: string;
  summary?: string;
  cover_image?: File;
  tag_ids?: string[];
  is_published?: boolean;
}

export interface UpdateArticleData {
  title?: string;
  content?: string;
  summary?: string;
  cover_image?: File;
  tag_ids?: string[];
  is_published?: boolean;
  is_top?: boolean;
}

export interface CreateCommentData {
  content: string;
  parent?: string;
}

class ArticleService {
  async getArticles(params?: {
    page?: number;
    page_size?: number;
    tag?: string;
    author_id?: string;
    ordering?: string;
    search?: string;
  }): Promise<ApiResponse<PaginatedData<Article>>> {
    return apiService.get<PaginatedData<Article>>('/articles/', params);
  }

  async getMyArticles(params?: {
    page?: number;
    page_size?: number;
    is_published?: boolean;
    status?: number;
    is_top?: boolean;
  }): Promise<ApiResponse<PaginatedData<Article>>> {
    return apiService.get<PaginatedData<Article>>('/articles/my/', params);
  }

  async getArticle(id: string): Promise<ApiResponse<ArticleDetail>> {
    return apiService.get<ArticleDetail>(`/articles/${id}/`);
  }

  async createArticle(data: CreateArticleData): Promise<ApiResponse<ArticleDetail>> {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('content', data.content);
    if (data.summary) formData.append('summary', data.summary);
    if (data.cover_image) formData.append('cover_image', data.cover_image);
    if (data.tag_ids) formData.append('tag_ids', JSON.stringify(data.tag_ids));
    if (data.is_published !== undefined) formData.append('is_published', String(data.is_published));

    return apiService.upload<ArticleDetail>('/articles/create/', formData);
  }

  async updateArticle(id: string, data: UpdateArticleData): Promise<ApiResponse<ArticleDetail>> {
    const formData = new FormData();
    if (data.title) formData.append('title', data.title);
    if (data.content) formData.append('content', data.content);
    if (data.summary) formData.append('summary', data.summary);
    if (data.cover_image) formData.append('cover_image', data.cover_image);
    if (data.tag_ids) formData.append('tag_ids', JSON.stringify(data.tag_ids));
    if (data.is_published !== undefined) formData.append('is_published', String(data.is_published));
    if (data.is_top !== undefined) formData.append('is_top', String(data.is_top));

    return apiService.upload<ArticleDetail>(`/articles/${id}/update/`, formData);
  }

  async deleteArticle(id: string): Promise<ApiResponse<null>> {
    return apiService.delete<null>(`/articles/${id}/delete/`);
  }

  async toggleTop(id: string): Promise<ApiResponse<{ is_top: boolean }>> {
    return apiService.post<{ is_top: boolean }>(`/articles/${id}/toggle-top/`);
  }

  async getComments(articleId: string, params?: {
    page?: number;
    page_size?: number;
  }): Promise<ApiResponse<PaginatedData<Comment>>> {
    return apiService.get<PaginatedData<Comment>>(`/articles/${articleId}/comments/`, params);
  }

  async createComment(articleId: string, data: CreateCommentData): Promise<ApiResponse<Comment>> {
    return apiService.post<Comment>(`/articles/${articleId}/comments/create/`, data);
  }

  async deleteComment(commentId: string): Promise<ApiResponse<null>> {
    return apiService.delete<null>(`/articles/comments/${commentId}/delete/`);
  }

  async getTags(params?: {
    page?: number;
    page_size?: number;
    search?: string;
  }): Promise<ApiResponse<PaginatedData<Tag>>> {
    return apiService.get<PaginatedData<Tag>>('/articles/tags/', params);
  }

  async createTag(data: { name: string; description?: string }): Promise<ApiResponse<Tag>> {
    return apiService.post<Tag>('/articles/tags/create/', data);
  }

  async uploadImage(articleId: string, file: File): Promise<ApiResponse<{ image: string }>> {
    const formData = new FormData();
    formData.append('article_id', articleId);
    formData.append('image', file);
    return apiService.upload<{ image: string }>('/articles/images/upload/', formData);
  }
}

export const articleService = new ArticleService();
