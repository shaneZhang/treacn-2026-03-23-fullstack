import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';
import { ApiResponse, Tokens } from '@app-types/index';
import { getCSRFToken, setCSRFToken, rateLimiter } from '@utils/security';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

class ApiService {
  private client: AxiosInstance;
  private refreshPromise: Promise<Tokens> | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
      },
      withCredentials: true,
    });

    this.setupInterceptors();
    setCSRFToken();
  }

  private setupInterceptors(): void {
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const tokens = this.getTokens();
        if (tokens?.access) {
          config.headers.Authorization = `Bearer ${tokens.access}`;
        }

        const csrfToken = getCSRFToken();
        if (csrfToken) {
          config.headers['X-CSRF-Token'] = csrfToken;
        }

        const endpoint = config.url || '';
        if (!rateLimiter.isAllowed(endpoint)) {
          return Promise.reject(new Error('请求过于频繁，请稍后再试'));
        }

        return config;
      },
      (error: AxiosError) => Promise.reject(error)
    );

    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError<ApiResponse<unknown>>) => {
        const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const newTokens = await this.refreshToken();
            originalRequest.headers.Authorization = `Bearer ${newTokens.access}`;
            return this.client(originalRequest);
          } catch (refreshError) {
            this.clearTokens();
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  private getTokens(): Tokens | null {
    const tokensStr = localStorage.getItem('tokens');
    return tokensStr ? JSON.parse(tokensStr) : null;
  }

  private setTokens(tokens: Tokens): void {
    localStorage.setItem('tokens', JSON.stringify(tokens));
  }

  private clearTokens(): void {
    localStorage.removeItem('tokens');
    localStorage.removeItem('user');
  }

  private async refreshToken(): Promise<Tokens> {
    if (this.refreshPromise) {
      return this.refreshPromise;
    }

    const tokens = this.getTokens();
    if (!tokens?.refresh) {
      throw new Error('No refresh token available');
    }

    this.refreshPromise = this.client
      .post<ApiResponse<{ tokens: Tokens }>>('/users/auth/refresh/', {
        refresh: tokens.refresh,
      })
      .then((response) => {
        const newTokens = response.data.data.tokens;
        this.setTokens(newTokens);
        return newTokens;
      })
      .finally(() => {
        this.refreshPromise = null;
      });

    return this.refreshPromise;
  }

  public setAuthTokens(tokens: Tokens): void {
    this.setTokens(tokens);
  }

  public clearAuth(): void {
    this.clearTokens();
  }

  public async get<T>(url: string, params?: Record<string, unknown>): Promise<ApiResponse<T>> {
    const response = await this.client.get<ApiResponse<T>>(url, { params });
    return response.data;
  }

  public async post<T>(url: string, data?: unknown): Promise<ApiResponse<T>> {
    const response = await this.client.post<ApiResponse<T>>(url, data);
    return response.data;
  }

  public async put<T>(url: string, data?: unknown): Promise<ApiResponse<T>> {
    const response = await this.client.put<ApiResponse<T>>(url, data);
    return response.data;
  }

  public async patch<T>(url: string, data?: unknown): Promise<ApiResponse<T>> {
    const response = await this.client.patch<ApiResponse<T>>(url, data);
    return response.data;
  }

  public async delete<T>(url: string): Promise<ApiResponse<T>> {
    const response = await this.client.delete<ApiResponse<T>>(url);
    return response.data;
  }

  public async upload<T>(url: string, formData: FormData): Promise<ApiResponse<T>> {
    const response = await this.client.post<ApiResponse<T>>(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
}

export const apiService = new ApiService();
