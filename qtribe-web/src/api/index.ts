import apiClient from '@/lib/axios';
import type { 
  ApiResponse, 
  PaginatedData, 
  Article, 
  ArticleCreateRequest,
  Video,
  Comment,
  CommentCreateRequest,
  Message,
  User,
  UpdateProfileRequest,
  ChangePasswordRequest,
} from '@/types';

export const authApi = {
  login: (username: string, password: string) =>
    apiClient.post<ApiResponse<{ user: User; token: { access: string; refresh: string } }>>('/auth/login/', { username, password }),
  
  register: (data: { username: string; password: string; password_confirm: string; phone?: string; email?: string }) =>
    apiClient.post<ApiResponse<{ user: User; token: { access: string; refresh: string } }>>('/auth/register/', data),
  
  logout: () =>
    apiClient.post<ApiResponse<null>>('/auth/logout/'),
  
  getProfile: () =>
    apiClient.get<ApiResponse<User>>('/auth/profile/'),
  
  updateProfile: (data: UpdateProfileRequest) =>
    apiClient.patch<ApiResponse<User>>('/auth/profile/', data),
  
  changePassword: (data: ChangePasswordRequest) =>
    apiClient.post<ApiResponse<null>>('/auth/profile/password/', data),
  
  uploadAvatar: (file: File) => {
    const formData = new FormData();
    formData.append('avatar', file);
    return apiClient.post<ApiResponse<{ icon_url: string }>>('/auth/profile/avatar/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  checkUsername: (username: string) =>
    apiClient.get<ApiResponse<{ exists: boolean; available: boolean }>>(`/auth/check/username/?username=${username}`),
  
  checkPhone: (phone: string) =>
    apiClient.get<ApiResponse<{ exists: boolean; available: boolean }>>(`/auth/check/phone/?phone=${phone}`),
  
  getUser: (id: number) =>
    apiClient.get<ApiResponse<User>>(`/auth/users/${id}/`),
};

export const articleApi = {
  getList: (params?: { page?: number; page_size?: number; search?: string; user?: number }) =>
    apiClient.get<ApiResponse<PaginatedData<Article>>>('/articles/', { params }),
  
  getMyList: (params?: { page?: number; page_size?: number; search?: string }) =>
    apiClient.get<ApiResponse<PaginatedData<Article>>>('/articles/my/', { params }),
  
  getDetail: (id: number) =>
    apiClient.get<ApiResponse<Article>>(`/articles/${id}/`),
  
  create: (data: ArticleCreateRequest) => {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('content', data.content);
    if (data.default_img) {
      formData.append('default_img', data.default_img);
    }
    return apiClient.post<ApiResponse<Article>>('/articles/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  update: (id: number, data: Partial<ArticleCreateRequest>) =>
    apiClient.patch<ApiResponse<Article>>(`/articles/${id}/`, data),
  
  delete: (id: number) =>
    apiClient.delete<ApiResponse<null>>(`/articles/${id}/`),
  
  star: (id: number) =>
    apiClient.post<ApiResponse<{ is_starred: boolean; star_count: number }>>(`/articles/${id}/star/`),
  
  collect: (id: number) =>
    apiClient.post<ApiResponse<{ is_collected: boolean; collection_count: number }>>(`/articles/${id}/collect/`),
  
  top: (id: number) =>
    apiClient.post<ApiResponse<{ is_top: number }>>(`/articles/${id}/top/`),
};

export const videoApi = {
  getList: (params?: { page?: number; page_size?: number; search?: string; user?: number }) =>
    apiClient.get<ApiResponse<PaginatedData<Video>>>('/videos/', { params }),
  
  getMyList: (params?: { page?: number; page_size?: number; search?: string }) =>
    apiClient.get<ApiResponse<PaginatedData<Video>>>('/videos/my/', { params }),
  
  getDetail: (id: number) =>
    apiClient.get<ApiResponse<Video>>(`/videos/${id}/`),
  
  create: (data: { title: string; video: File; remark?: string }) => {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('video', data.video);
    if (data.remark) {
      formData.append('remark', data.remark);
    }
    return apiClient.post<ApiResponse<Video>>('/videos/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  update: (id: number, data: { title?: string; remark?: string }) =>
    apiClient.patch<ApiResponse<Video>>(`/videos/${id}/`, data),
  
  delete: (id: number) =>
    apiClient.delete<ApiResponse<null>>(`/videos/${id}/`),
  
  star: (id: number) =>
    apiClient.post<ApiResponse<{ is_starred: boolean; star_count: number }>>(`/videos/${id}/star/`),
  
  collect: (id: number) =>
    apiClient.post<ApiResponse<{ is_collected: boolean; collection_count: number }>>(`/videos/${id}/collect/`),
  
  top: (id: number) =>
    apiClient.post<ApiResponse<{ is_top: number }>>(`/videos/${id}/top/`),
};

export const commentApi = {
  getList: (params?: { page?: number; page_size?: number; article?: number; video?: number }) =>
    apiClient.get<ApiResponse<PaginatedData<Comment>>>('/comments/', { params }),
  
  getArticleComments: (articleId: number, params?: { page?: number; page_size?: number }) =>
    apiClient.get<ApiResponse<PaginatedData<Comment>>>(`/comments/article/${articleId}/`, { params }),
  
  getVideoComments: (videoId: number, params?: { page?: number; page_size?: number }) =>
    apiClient.get<ApiResponse<PaginatedData<Comment>>>(`/comments/video/${videoId}/`, { params }),
  
  create: (data: CommentCreateRequest) =>
    apiClient.post<ApiResponse<Comment>>('/comments/', data),
  
  delete: (id: number) =>
    apiClient.delete<ApiResponse<null>>(`/comments/${id}/`),
};

export const messageApi = {
  getList: (params?: { page?: number; page_size?: number; type_1?: string; status?: number }) =>
    apiClient.get<ApiResponse<PaginatedData<Message>>>('/messages/', { params }),
  
  getDetail: (id: number) =>
    apiClient.get<ApiResponse<Message>>(`/messages/${id}/`),
  
  markAllRead: () =>
    apiClient.post<ApiResponse<null>>('/messages/read-all/'),
  
  getUnreadCount: () =>
    apiClient.get<ApiResponse<{ count: number }>>('/messages/unread-count/'),
};

export const smsApi = {
  send: (phone: string) =>
    apiClient.post<ApiResponse<{ code: string }>>('/sms/send/', { phone }),
  
  check: (phone: string, code: string) =>
    apiClient.post<ApiResponse<null>>('/sms/check/', { phone, code }),
};
