import { apiService } from './api';
import {
  ApiResponse,
  LoginCredentials,
  RegisterData,
  Tokens,
  User,
  UserDetail,
} from '@app-types/index';

export interface AuthResponse {
  user: User;
  tokens: Tokens;
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<ApiResponse<AuthResponse>> {
    return apiService.post<AuthResponse>('/users/auth/login/', credentials);
  }

  async register(data: RegisterData): Promise<ApiResponse<AuthResponse>> {
    return apiService.post<AuthResponse>('/users/auth/register/', data);
  }

  async logout(refreshToken: string): Promise<ApiResponse<null>> {
    return apiService.post<null>('/users/auth/logout/', { refresh: refreshToken });
  }

  async getProfile(): Promise<ApiResponse<UserDetail>> {
    return apiService.get<UserDetail>('/users/profile/');
  }

  async updateProfile(data: Partial<User>): Promise<ApiResponse<UserDetail>> {
    return apiService.patch<UserDetail>('/users/profile/', data);
  }

  async uploadAvatar(file: File): Promise<ApiResponse<{ avatar: string }>> {
    const formData = new FormData();
    formData.append('avatar', file);
    return apiService.upload<{ avatar: string }>('/users/profile/avatar/', formData);
  }

  async changePassword(data: {
    old_password: string;
    new_password: string;
    new_password_confirm: string;
  }): Promise<ApiResponse<null>> {
    return apiService.post<null>('/users/profile/change-password/', data);
  }

  async checkUsername(username: string): Promise<ApiResponse<{ exists: boolean }>> {
    return apiService.get<{ exists: boolean }>('/users/auth/check-username/', { username });
  }

  async checkPhone(phone: string): Promise<ApiResponse<{ exists: boolean }>> {
    return apiService.get<{ exists: boolean }>('/users/auth/check-phone/', { phone });
  }
}

export const authService = new AuthService();
