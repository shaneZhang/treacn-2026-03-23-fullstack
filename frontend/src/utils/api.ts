import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios'

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface PageData<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

class ApiClient {
  private instance: AxiosInstance
  private token: string | null = null

  constructor(baseURL: string = '/api') {
    this.instance = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.setupInterceptors()
    this.token = localStorage.getItem('access_token')
  }

  private setupInterceptors() {
    this.instance.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    this.instance.interceptors.response.use(
      (response: AxiosResponse<ApiResponse>) => response,
      async (error) => {
        const originalRequest = error.config
        
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true
          
          try {
            const refreshToken = localStorage.getItem('refresh_token')
            if (refreshToken) {
              const response = await axios.post<ApiResponse<{ access: string }>>(
                '/api/token/refresh/',
                { refresh: refreshToken }
              )
              
              const newAccessToken = response.data.data.access
              this.setToken(newAccessToken)
              originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
              
              return this.instance(originalRequest)
            }
          } catch (refreshError) {
            this.logout()
            window.location.href = '/login'
          }
        }
        
        return Promise.reject(error)
      }
    )
  }

  setToken(token: string) {
    this.token = token
    localStorage.setItem('access_token', token)
  }

  setRefreshToken(token: string) {
    localStorage.setItem('refresh_token', token)
  }

  logout() {
    this.token = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  isAuthenticated() {
    return !!this.token
  }

  async request<T = any>(config: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.instance.request<ApiResponse<T>>(config)
      return response.data
    } catch (error: any) {
      if (error.response?.data) {
        throw error.response.data
      }
      throw {
        code: error.response?.status || 500,
        message: error.message || '请求失败',
        data: null
      }
    }
  }

  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ method: 'GET', url, ...config })
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ method: 'POST', url, data, ...config })
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ method: 'PUT', url, data, ...config })
  }

  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ method: 'PATCH', url, data, ...config })
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>({ method: 'DELETE', url, ...config })
  }

  async upload<T = any>(url: string, file: File, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    const formData = new FormData()
    formData.append('file', file)
    
    return this.request<T>({
      method: 'POST',
      url,
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      ...config,
    })
  }
}

export const apiClient = new ApiClient()
