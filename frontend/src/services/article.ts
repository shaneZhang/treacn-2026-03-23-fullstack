import { apiClient, type PageData } from '../utils/api'
import type { Article, Comment, PageParams } from '../types'

export const articleApi = {
  getArticles: (params?: PageParams) => {
    return apiClient.get<PageData<Article>>('/pieces/article/', { params })
  },

  getArticle: (id: number) => {
    return apiClient.get<Article>(`/pieces/article/${id}/`)
  },

  createArticle: (data: FormData) => {
    return apiClient.post<Article>('/pieces/article/', data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    })
  },

  updateArticle: (id: number, data: Partial<Article>) => {
    return apiClient.patch<Article>(`/pieces/article/${id}/`, data)
  },

  deleteArticle: (id: number) => {
    return apiClient.delete(`/pieces/article/${id}/`)
  },

  getMyArticles: (params?: PageParams) => {
    return apiClient.get<PageData<Article>>('/pieces/article/my_articles/', { params })
  },

  toggleTop: (id: number) => {
    return apiClient.post(`/pieces/article/${id}/top/`)
  },

  getComments: (articleId: number) => {
    return apiClient.get<Comment[]>(`/pieces/article/${articleId}/comments/`)
  },

  addComment: (articleId: number, content: string, commentId?: number) => {
    const data: any = { content }
    if (commentId) {
      data.comment = commentId
    }
    return apiClient.post<Comment>(`/pieces/article/${articleId}/add_comment/`, data)
  },

  deleteComment: (commentId: number) => {
    return apiClient.delete(`/pieces/comment/${commentId}/`)
  },

  searchArticles: (keyword: string, params?: PageParams) => {
    return apiClient.get<PageData<Article>>('/pieces/article/', {
      params: { search: keyword, ...params }
    })
  },
}
