import React from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '@/stores/auth';
import { getImageUrl } from '@/lib/utils';

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const { user, isAuthenticated, logout } = useAuthStore();
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link to="/" className="text-2xl font-bold text-primary-600">
                QTribe
              </Link>
              <nav className="hidden md:ml-10 md:flex md:space-x-8">
                <Link
                  to="/"
                  className="text-gray-900 inline-flex items-center px-1 pt-1 text-sm font-medium hover:text-primary-600"
                >
                  首页
                </Link>
                <Link
                  to="/articles"
                  className="text-gray-500 inline-flex items-center px-1 pt-1 text-sm font-medium hover:text-primary-600"
                >
                  文章
                </Link>
                <Link
                  to="/videos"
                  className="text-gray-500 inline-flex items-center px-1 pt-1 text-sm font-medium hover:text-primary-600"
                >
                  视频
                </Link>
              </nav>
            </div>

            <div className="flex items-center">
              {isAuthenticated && user ? (
                <div className="relative">
                  <button
                    onClick={() => setIsMenuOpen(!isMenuOpen)}
                    className="flex items-center space-x-2 text-sm focus:outline-none"
                  >
                    <img
                      src={getImageUrl(user.icon_url)}
                      alt={user.username}
                      className="w-8 h-8 rounded-full object-cover"
                    />
                    <span className="hidden md:block text-gray-700">{user.username}</span>
                  </button>

                  {isMenuOpen && (
                    <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
                      <Link
                        to="/profile"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        onClick={() => setIsMenuOpen(false)}
                      >
                        个人中心
                      </Link>
                      <Link
                        to="/messages"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        onClick={() => setIsMenuOpen(false)}
                      >
                        消息通知
                      </Link>
                      <Link
                        to="/articles/edit"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        onClick={() => setIsMenuOpen(false)}
                      >
                        发布文章
                      </Link>
                      <button
                        onClick={handleLogout}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        退出登录
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <div className="flex items-center space-x-4">
                  <Link
                    to="/login"
                    className="text-gray-700 hover:text-primary-600 text-sm font-medium"
                  >
                    登录
                  </Link>
                  <Link
                    to="/register"
                    className="bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-700"
                  >
                    注册
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      <footer className="bg-white border-t mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            © 2024 QTribe. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default MainLayout;
