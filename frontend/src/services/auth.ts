import { apiClient } from '../utils/api'
import type { 
  User, 
  LoginRequest, 
  RegisterRequest, 
  UpdateProfileRequest,
  CheckUsernameResponse,
  CheckPhoneResponse
} from '../types'

// 认证响应类型
interface AuthResponse {
  access: string
  refresh: string
  user: User
}

export const authApi = {
  login: (data: LoginRequest) => {
    return apiClient.post<AuthResponse>('/auth/login/', data)
  },

  register: (data: RegisterRequest) => {
    return apiClient.post<AuthResponse>('/auth/register/', data)
  },

  logout: () => {
    return apiClient.post('/auth/logout/')
  },

  changePassword: (old_password: string, new_password: string, new_password2: string) => {
    return apiClient.post('/auth/change_password/', {
      old_password,
      new_password,
      new_password2
    })
  },

  getProfile: () => {
    return apiClient.get<User>('/user/profile/')
  },

  updateProfile: (data: UpdateProfileRequest, avatar?: File | null) => {
    if (avatar) {
      const formData = new FormData()
      formData.append('icon', avatar)
      if (data.username) formData.append('username', data.username)
      if (data.email) formData.append('email', data.email)
      if (data.bio) formData.append('bio', data.bio)
      return apiClient.patch<User>('/user/update_profile/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      })
    }
    return apiClient.patch<User>('/user/update_profile/', data)
  },

  uploadAvatar: (file: File) => {
    const formData = new FormData()
    formData.append('icon', file)
    return apiClient.post<User>('/user/upload_avatar/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    })
  },

  checkUsername: (username: string) => {
    return apiClient.post<CheckUsernameResponse>('/check_username/', { username })
  },

  checkPhone: (phone: string) => {
    return apiClient.post<CheckPhoneResponse>('/check_phone/', { phone })
  },

  checkEmail: (email: string) => {
    return apiClient.post<{ exists: boolean; count: number }>('/check_email/', { email })
  },

  getUserProfile: (userId: number) => {
    return apiClient.get<User>(`/user/${userId}/public_profile/`)
  },
}

export const useAuth = () => {
  const login = async (data: LoginRequest) => {
    const response = await authApi.login(data)
    if (response.code === 200 && response.data) {
      apiClient.setToken(response.data.access)
      apiClient.setRefreshToken(response.data.refresh)
    }
    return response
  }

  const register = async (data: RegisterRequest) => {
    const response = await authApi.register(data)
    if ((response.code === 200 || response.code === 201) && response.data) {
      apiClient.setToken(response.data.access)
      apiClient.setRefreshToken(response.data.refresh)
    }
    return response
  }

  const logout = () => {
    apiClient.logout()
  }

  const isAuthenticated = () => {
    return apiClient.isAuthenticated()
  }

  return {
    login,
    register,
    logout,
    isAuthenticated,
  }
}
