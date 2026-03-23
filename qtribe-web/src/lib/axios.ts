import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import type { ApiResponse } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error: AxiosError<ApiResponse<unknown>>) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && originalRequest) {
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (refreshToken) {
        try {
          const response = await axios.post<ApiResponse<{ access: string }>>(
            `${API_BASE_URL}/auth/token/refresh/`,
            { refresh: refreshToken }
          );
          
          if (response.data.success && response.data.data.access) {
            localStorage.setItem('access_token', response.data.data.access);
            
            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${response.data.data.access}`;
            }
            
            return apiClient(originalRequest);
          }
        } catch {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      } else {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
