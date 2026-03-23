import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react'
import { useAuth } from '../services/auth'
import type { User, UpdateProfileRequest } from '../types'
import { authApi } from '../services/auth'
import { apiClient } from '../utils/api'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  loading: boolean
  login: (data: any) => Promise<any>
  register: (data: any) => Promise<any>
  logout: () => void
  refreshUser: () => Promise<void>
  updateProfile: (data: UpdateProfileRequest, avatar?: File | null) => Promise<any>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const auth = useAuth()

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('access_token')
      if (token) {
        try {
          const response = await authApi.getProfile()
          if (response.code === 200) {
            setUser(response.data)
          } else {
            apiClient.logout()
          }
        } catch (error) {
          apiClient.logout()
        }
      }
      setLoading(false)
    }

    initAuth()
  }, [])

  const login = async (data: any) => {
    const response = await auth.login(data)
    if (response.code === 200 && response.data) {
      setUser(response.data.user)
    }
    return response
  }

  const register = async (data: any) => {
    const response = await auth.register(data)
    if (response.code === 201 && response.data) {
      setUser(response.data.user)
    }
    return response
  }

  const logout = () => {
    auth.logout()
    setUser(null)
  }

  const refreshUser = async () => {
    try {
      const response = await authApi.getProfile()
      if (response.code === 200) {
        setUser(response.data)
      }
    } catch (error) {
      console.error('Failed to refresh user:', error)
    }
  }

  const updateProfile = async (data: UpdateProfileRequest, avatar?: File | null) => {
    const response = await authApi.updateProfile(data, avatar)
    if (response.code === 200) {
      setUser(response.data)
    }
    return response
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: auth.isAuthenticated() && !!user,
        loading,
        login,
        register,
        logout,
        refreshUser,
        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuthContext = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider')
  }
  return context
}
