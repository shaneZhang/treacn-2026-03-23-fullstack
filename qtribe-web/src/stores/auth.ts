import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User, AuthResponse } from '@/types';
import apiClient from '@/lib/axios';
import type { ApiResponse } from '@/types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  
  login: (username: string, password: string) => Promise<void>;
  register: (data: {
    username: string;
    password: string;
    password_confirm: string;
    phone?: string;
    email?: string;
  }) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
  setUser: (user: User) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      
      login: async (username: string, password: string) => {
        set({ isLoading: true });
        try {
          const response = await apiClient.post<ApiResponse<AuthResponse>>('/auth/login/', {
            username,
            password,
          });
          
          if (response.data.success && response.data.data) {
            const { user, token } = response.data.data;
            localStorage.setItem('access_token', token.access);
            localStorage.setItem('refresh_token', token.refresh);
            set({ user, isAuthenticated: true, isLoading: false });
          } else {
            throw new Error(response.data.message || '登录失败');
          }
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },
      
      register: async (data) => {
        set({ isLoading: true });
        try {
          const response = await apiClient.post<ApiResponse<AuthResponse>>('/auth/register/', data);
          
          if (response.data.success && response.data.data) {
            const { user, token } = response.data.data;
            localStorage.setItem('access_token', token.access);
            localStorage.setItem('refresh_token', token.refresh);
            set({ user, isAuthenticated: true, isLoading: false });
          } else {
            throw new Error(response.data.message || '注册失败');
          }
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },
      
      logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        set({ user: null, isAuthenticated: false });
      },
      
      fetchUser: async () => {
        const token = localStorage.getItem('access_token');
        if (!token) {
          set({ user: null, isAuthenticated: false });
          return;
        }
        
        set({ isLoading: true });
        try {
          const response = await apiClient.get<ApiResponse<User>>('/auth/profile/');
          
          if (response.data.success && response.data.data) {
            set({ user: response.data.data, isAuthenticated: true, isLoading: false });
          } else {
            set({ user: null, isAuthenticated: false, isLoading: false });
          }
        } catch {
          set({ user: null, isAuthenticated: false, isLoading: false });
        }
      },
      
      setUser: (user: User) => {
        set({ user });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
    }
  )
);
