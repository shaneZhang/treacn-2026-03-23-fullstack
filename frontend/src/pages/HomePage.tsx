import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import MainLayout from '@/components/layout/MainLayout'
import { articleApi } from '@/services/article'
import type { Article } from '@/types'

const HomePage: React.FC = () => {
  const [articles, setArticles] = useState<Article[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const response = await articleApi.getArticles({ page: 1, page_size: 6 })
        if (response.code === 200) {
          setArticles(response.data.results || [])
        }
      } catch (error) {
        console.error('Failed to fetch articles:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchArticles()
  }, [])

  return (
    <MainLayout>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary to-secondary text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
            发现精彩，分享智慧
          </h1>
          <p className="text-xl md:text-2xl text-white/90 mb-8 max-w-3xl mx-auto">
            在 QTribe，与志同道合的人一起，探索知识的海洋，分享您的见解与创意
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/articles"
              className="px-8 py-3 bg-white text-primary font-semibold rounded-lg hover:bg-gray-100 transition-colors shadow-lg"
            >
              浏览文章
            </Link>
            <Link
              to="/create-article"
              className="px-8 py-3 bg-transparent border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-primary transition-colors"
            >
              发布文章
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-primary">10K+</div>
              <div className="text-gray-600 mt-2">注册用户</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-primary">5K+</div>
              <div className="text-gray-600 mt-2">优质文章</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-primary">50K+</div>
              <div className="text-gray-600 mt-2">互动次数</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-primary">100+</div>
              <div className="text-gray-600 mt-2">活跃作者</div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Articles Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-10">
            <div>
              <h2 className="text-3xl font-bold text-gray-900">最新文章</h2>
              <p className="text-gray-600 mt-2">发现最新发布的优质内容</p>
            </div>
            <Link
              to="/articles"
              className="hidden md:inline-flex items-center text-primary hover:text-primary-dark font-medium"
            >
              查看全部
              <svg className="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>

          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {articles.map((article) => (
                <article
                  key={article.id}
                  className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300"
                >
                  <Link to={`/articles/${article.id}`}>
                    <div className="h-48 bg-gradient-to-br from-gray-200 to-gray-300 overflow-hidden">
                      {article.default_img ? (
                        <img
                          src={article.default_img.startsWith('http') ? article.default_img : `/media/${article.default_img}`}
                          alt={article.title}
                          className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-primary/20 to-secondary/20">
                          <svg className="h-16 w-16 text-primary/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                        </div>
                      )}
                    </div>
                  </Link>
                  <div className="p-6">
                    <div className="flex items-center mb-3">
                      {article.user?.icon ? (
                        <img
                          src={article.user.icon.startsWith('http') ? article.user.icon : `/media/${article.user.icon}`}
                          alt={article.user.username}
                          className="h-8 w-8 rounded-full object-cover"
                        />
                      ) : (
                        <div className="h-8 w-8 rounded-full bg-gradient-to-r from-primary to-secondary flex items-center justify-center text-white text-sm font-medium">
                          {article.user?.username?.charAt(0).toUpperCase()}
                        </div>
                      )}
                      <span className="ml-2 text-sm text-gray-600">{article.user?.username}</span>
                      <span className="mx-2 text-gray-300">•</span>
                      <span className="text-sm text-gray-500">
                        {new Date(article.create_time).toLocaleDateString('zh-CN')}
                      </span>
                    </div>
                    <Link to={`/articles/${article.id}`}>
                      <h3 className="text-xl font-semibold text-gray-900 mb-2 hover:text-primary transition-colors line-clamp-2">
                        {article.title}
                      </h3>
                    </Link>
                    <p className="text-gray-600 text-sm line-clamp-2 mb-4">
                      {article.content.replace(/<[^>]*>/g, '').substring(0, 100)}...
                    </p>
                    <div className="flex items-center justify-between text-sm text-gray-500">
                      <div className="flex items-center space-x-4">
                        <span className="flex items-center">
                          <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                          </svg>
                          {article.running_count}
                        </span>
                        <span className="flex items-center">
                          <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                          </svg>
                          {article.star_count}
                        </span>
                        <span className="flex items-center">
                          <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                          </svg>
                          {article.collection_count}
                        </span>
                      </div>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}

          <div className="mt-8 text-center md:hidden">
            <Link
              to="/articles"
              className="inline-flex items-center px-6 py-3 border border-primary text-primary font-medium rounded-lg hover:bg-primary hover:text-white transition-colors"
            >
              查看全部文章
              <svg className="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-primary to-secondary">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            准备好分享您的故事了吗？
          </h2>
          <p className="text-xl text-white/90 mb-8">
            加入我们，与成千上万的创作者一起，分享您的知识和经验
          </p>
          <Link
            to="/create-article"
            className="inline-block px-8 py-3 bg-white text-primary font-semibold rounded-lg hover:bg-gray-100 transition-colors shadow-lg"
          >
            开始创作
          </Link>
        </div>
      </section>
    </MainLayout>
  )
}

export default HomePage
