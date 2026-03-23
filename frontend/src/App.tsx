import React, { Suspense, lazy } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from '@/context/AuthContext'
import { ToastProvider } from '@/components/common/Toast'
import { RequireAuth, RequireGuest } from '@/components/guards/AuthGuard'

// Lazy load components for better performance
const HomePage = lazy(() => import('./pages/HomePage.tsx'))
const LoginPage = lazy(() => import('./pages/auth/LoginPage.tsx'))
const RegisterPage = lazy(() => import('./pages/auth/RegisterPage.tsx'))
const ArticleListPage = lazy(() => import('./pages/article/ArticleListPage.tsx'))
const ArticleDetailPage = lazy(() => import('./pages/article/ArticleDetailPage.tsx'))
const ProfilePage = lazy(() => import('./pages/profile/ProfilePage.tsx'))

// Loading component
const LoadingSpinner: React.FC = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
  </div>
)

const App: React.FC = () => {
  return (
    <Router>
      <ToastProvider>
        <AuthProvider>
          <Suspense fallback={<LoadingSpinner />}>
            <Routes>
            {/* Public routes */}
            <Route path="/" element={<HomePage />} />
            <Route path="/articles" element={<ArticleListPage />} />
            <Route path="/articles/:id" element={<ArticleDetailPage />} />
            
            {/* Guest-only routes (login/register) */}
            <Route
              path="/login"
              element={
                <RequireGuest>
                  <LoginPage />
                </RequireGuest>
              }
            />
            <Route
              path="/register"
              element={
                <RequireGuest>
                  <RegisterPage />
                </RequireGuest>
              }
            />
            
            {/* Protected routes */}
            <Route
              path="/profile"
              element={
                <RequireAuth>
                  <ProfilePage />
                </RequireAuth>
              }
            />
            
            {/* Catch all - 404 */}
            <Route
              path="*"
              element={
                <div className="flex items-center justify-center min-h-screen">
                  <div className="text-center">
                    <h1 className="text-6xl font-bold text-gray-300 mb-4">404</h1>
                    <p className="text-xl text-gray-600 mb-8">页面不存在</p>
                    <a
                      href="/"
                      className="inline-block px-6 py-3 bg-primary text-white font-medium rounded-lg hover:bg-primary-dark transition-colors"
                    >
                      返回首页
                    </a>
                  </div>
                </div>
              }
            />
            </Routes>
          </Suspense>
        </AuthProvider>
      </ToastProvider>
    </Router>
  )
}

export default App
