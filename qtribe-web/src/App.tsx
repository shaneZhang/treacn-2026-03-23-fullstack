import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'sonner';

import { useAuthStore } from '@/stores/auth';
import MainLayout from '@/components/layout/MainLayout';
import LoginPage from '@/pages/auth/LoginPage';
import RegisterPage from '@/pages/auth/RegisterPage';
import HomePage from '@/pages/home/HomePage';
import ArticleListPage from '@/pages/article/ArticleListPage';
import ArticleDetailPage from '@/pages/article/ArticleDetailPage';
import ArticleEditPage from '@/pages/article/ArticleEditPage';
import VideoListPage from '@/pages/video/VideoListPage';
import VideoDetailPage from '@/pages/video/VideoDetailPage';
import ProfilePage from '@/pages/profile/ProfilePage';
import MessagePage from '@/pages/message/MessagePage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
};

const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore();
  return !isAuthenticated ? <>{children}</> : <Navigate to="/" replace />;
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route
            path="/login"
            element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            }
          />
          <Route
            path="/register"
            element={
              <PublicRoute>
                <RegisterPage />
              </PublicRoute>
            }
          />
          <Route
            path="/"
            element={
              <MainLayout>
                <HomePage />
              </MainLayout>
            }
          />
          <Route
            path="/articles"
            element={
              <MainLayout>
                <ArticleListPage />
              </MainLayout>
            }
          />
          <Route
            path="/articles/:id"
            element={
              <MainLayout>
                <ArticleDetailPage />
              </MainLayout>
            }
          />
          <Route
            path="/articles/edit"
            element={
              <PrivateRoute>
                <MainLayout>
                  <ArticleEditPage />
                </MainLayout>
              </PrivateRoute>
            }
          />
          <Route
            path="/articles/edit/:id"
            element={
              <PrivateRoute>
                <MainLayout>
                  <ArticleEditPage />
                </MainLayout>
              </PrivateRoute>
            }
          />
          <Route
            path="/videos"
            element={
              <MainLayout>
                <VideoListPage />
              </MainLayout>
            }
          />
          <Route
            path="/videos/:id"
            element={
              <MainLayout>
                <VideoDetailPage />
              </MainLayout>
            }
          />
          <Route
            path="/profile"
            element={
              <PrivateRoute>
                <MainLayout>
                  <ProfilePage />
                </MainLayout>
              </PrivateRoute>
            }
          />
          <Route
            path="/messages"
            element={
              <PrivateRoute>
                <MainLayout>
                  <MessagePage />
                </MainLayout>
              </PrivateRoute>
            }
          />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-center" />
    </QueryClientProvider>
  );
}

export default App;
