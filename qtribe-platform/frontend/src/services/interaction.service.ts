import { apiService } from './api';
import {
  ApiResponse,
  Collection,
  Like,
  Notification,
  PaginatedData,
} from '@app-types/index';

class InteractionService {
  async toggleLike(data: { article?: string; comment?: string }): Promise<ApiResponse<{ is_liked: boolean; like: Like }>> {
    return apiService.post<{ is_liked: boolean; like: Like }>('/interactions/likes/toggle/', data);
  }

  async getLikes(params?: {
    page?: number;
    page_size?: number;
    type?: 'article' | 'comment';
  }): Promise<ApiResponse<PaginatedData<Like>>> {
    return apiService.get<PaginatedData<Like>>('/interactions/likes/', params);
  }

  async toggleCollection(data: { article: string }): Promise<ApiResponse<{ is_collected: boolean; collection: Collection }>> {
    return apiService.post<{ is_collected: boolean; collection: Collection }>('/interactions/collections/toggle/', data);
  }

  async getCollections(params?: {
    page?: number;
    page_size?: number;
  }): Promise<ApiResponse<PaginatedData<Collection>>> {
    return apiService.get<PaginatedData<Collection>>('/interactions/collections/', params);
  }

  async checkCollection(articleId: string): Promise<ApiResponse<{ is_collected: boolean }>> {
    return apiService.get<{ is_collected: boolean }>(`/interactions/collections/check/${articleId}/`);
  }

  async getNotifications(params?: {
    page?: number;
    page_size?: number;
    is_read?: boolean;
  }): Promise<ApiResponse<PaginatedData<Notification> & { unread_count: number }>> {
    return apiService.get<PaginatedData<Notification> & { unread_count: number }>('/interactions/notifications/', params);
  }

  async markNotificationsRead(data: { notification_ids?: string[]; mark_all?: boolean }): Promise<ApiResponse<null>> {
    return apiService.post<null>('/interactions/notifications/mark-read/', data);
  }

  async deleteNotification(notificationId: string): Promise<ApiResponse<null>> {
    return apiService.delete<null>(`/interactions/notifications/${notificationId}/delete/`);
  }

  async getUnreadCount(): Promise<ApiResponse<{ unread_count: number }>> {
    return apiService.get<{ unread_count: number }>('/interactions/notifications/unread-count/');
  }
}

export const interactionService = new InteractionService();
