import React, { useState, useCallback } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthContext } from '../../context/AuthContext'
import { authApi } from '../../services/auth'

const RegisterPage: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    phone: '',
    email: '',
    password: '',
    password2: '',
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)
  const [submitError, setSubmitError] = useState('')
  const [checking, setChecking] = useState<Record<string, boolean>>({})
  const [availability, setAvailability] = useState<Record<string, boolean>>({})
  
  const { register } = useAuthContext()
  const navigate = useNavigate()

  const checkUsername = useCallback(async (username: string) => {
    if (username.length < 3) return
    setChecking(prev => ({ ...prev, username: true }))
    try {
      const response = await authApi.checkUsername(username)
      setAvailability(prev => ({ ...prev, username: !response.data.exists }))
    } catch (error) {
      console.error('Failed to check username:', error)
    } finally {
      setChecking(prev => ({ ...prev, username: false }))
    }
  }, [])

  const checkPhone = useCallback(async (phone: string) => {
    if (!/^1[3-9]\d{9}$/.test(phone)) return
    setChecking(prev => ({ ...prev, phone: true }))
    try {
      const response = await authApi.checkPhone(phone)
      setAvailability(prev => ({ ...prev, phone: !response.data.exists }))
    } catch (error) {
      console.error('Failed to check phone:', error)
    } finally {
      setChecking(prev => ({ ...prev, phone: false }))
    }
  }, [])

  const validate = () => {
    const newErrors: Record<string, string> = {}
    
    if (!formData.username.trim()) {
      newErrors.username = '请输入用户名'
    } else if (formData.username.length < 3) {
      newErrors.username = '用户名至少3个字符'
    } else if (availability.username === false) {
      newErrors.username = '用户名已被使用'
    }
    
    if (!formData.phone.trim()) {
      newErrors.phone = '请输入手机号'
    } else if (!/^1[3-9]\d{9}$/.test(formData.phone)) {
      newErrors.phone = '请输入有效的手机号'
    } else if (availability.phone === false) {
      newErrors.phone = '手机号已被注册'
    }
    
    if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = '请输入有效的邮箱地址'
    }
    
    if (!formData.password) {
      newErrors.password = '请输入密码'
    } else if (formData.password.length < 6) {
      newErrors.password = '密码至少6个字符'
    }
    
    if (!formData.password2) {
      newErrors.password2 = '请确认密码'
    } else if (formData.password !== formData.password2) {
      newErrors.password2 = '两次输入的密码不一致'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validate()) return
    
    setLoading(true)
    setSubmitError('')
    
    try {
      const response = await register({
        username: formData.username,
        phone: formData.phone,
        password: formData.password,
        password2: formData.password2,
        email: formData.email,
      })
      
      if (response.code === 201) {
        navigate('/')
      } else {
        setSubmitError(response.message || '注册失败')
      }
    } catch (error: any) {
      setSubmitError(error.message || '注册失败，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
    if (submitError) {
      setSubmitError('')
    }
    
    if (name === 'username') {
      checkUsername(value)
    } else if (name === 'phone') {
      checkPhone(value)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            创建新账号
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            或者{' '}
            <Link to="/login" className="font-medium text-primary hover:text-primary-dark">
              登录已有账号
            </Link>
          </p>
        </div>
        
        <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
          {submitError && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
              {submitError}
            </div>
          )}
          
          <div className="space-y-4">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
                用户名
              </label>
              <div className="relative">
                <input
                  id="username"
                  name="username"
                  type="text"
                  value={formData.username}
                  onChange={handleChange}
                  className={`appearance-none relative block w-full px-3 py-3 pr-10 border ${
                    errors.username ? 'border-red-300' : 
                    availability.username ? 'border-green-300' : 'border-gray-300'
                  } rounded-lg placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent sm:text-sm`}
                  placeholder="请输入用户名"
                />
                {checking.username && (
                  <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-400"></div>
                  </div>
                )}
                {!checking.username && availability.username && (
                  <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-green-500">
                    <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}
              </div>
              {errors.username && (
                <p className="mt-1 text-sm text-red-600">{errors.username}</p>
              )}
            </div>
            
            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
                手机号
              </label>
              <div className="relative">
                <input
                  id="phone"
                  name="phone"
                  type="tel"
                  value={formData.phone}
                  onChange={handleChange}
                  className={`appearance-none relative block w-full px-3 py-3 pr-10 border ${
                    errors.phone ? 'border-red-300' : 
                    availability.phone ? 'border-green-300' : 'border-gray-300'
                  } rounded-lg placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent sm:text-sm`}
                  placeholder="请输入手机号"
                />
                {checking.phone && (
                  <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-400"></div>
                  </div>
                )}
                {!checking.phone && availability.phone && (
                  <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-green-500">
                    <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}
              </div>
              {errors.phone && (
                <p className="mt-1 text-sm text-red-600">{errors.phone}</p>
              )}
            </div>
            
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                邮箱（可选）
              </label>
              <input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                className={`appearance-none relative block w-full px-3 py-3 border ${
                  errors.email ? 'border-red-300' : 'border-gray-300'
                } rounded-lg placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent sm:text-sm`}
                placeholder="请输入邮箱"
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email}</p>
              )}
            </div>
            
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                密码
              </label>
              <input
                id="password"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                className={`appearance-none relative block w-full px-3 py-3 border ${
                  errors.password ? 'border-red-300' : 'border-gray-300'
                } rounded-lg placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent sm:text-sm`}
                placeholder="请输入密码（至少6位）"
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password}</p>
              )}
            </div>
            
            <div>
              <label htmlFor="password2" className="block text-sm font-medium text-gray-700 mb-1">
                确认密码
              </label>
              <input
                id="password2"
                name="password2"
                type="password"
                value={formData.password2}
                onChange={handleChange}
                className={`appearance-none relative block w-full px-3 py-3 border ${
                  errors.password2 ? 'border-red-300' : 'border-gray-300'
                } rounded-lg placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent sm:text-sm`}
                placeholder="请再次输入密码"
              />
              {errors.password2 && (
                <p className="mt-1 text-sm text-red-600">{errors.password2}</p>
              )}
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
            >
              {loading ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  注册中...
                </div>
              ) : (
                '注册'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default RegisterPage
