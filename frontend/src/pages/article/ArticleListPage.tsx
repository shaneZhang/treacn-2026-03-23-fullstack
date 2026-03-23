import React, { useEffect, useState, useCallback } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import MainLayout from '../../components/layout/MainLayout'
import { articleApi } from '../../services/article'
import { interactionApi } from '../../services/interaction'
import type { Article } from '../../types'
import { useAuthContext } from '../../context/AuthContext'

const ArticleListPage: React.FC = () => {
  const [articles, setArticles] = useState<Article[]>([])
  const [loading, setLoading] = useState(true)
  const [searchParams, setSearchParams] = useSearchParams()
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [totalCount, setTotalCount] = useState(0)
  const [searchKeyword, setSearchKeyword] = useState(searchParams.get('search') || '')
  const [actionLoading, setActionLoading] = useState<number | null>(null)
  
  const { isAuthenticated } = useAuthContext()
  const pageSize = 10

  const fetchArticles = useCallback(async () => {
    setLoading(true)
    try {
      const params: any = { page: currentPage, page_size: pageSize }
      if (searchKeyword) {
        params.search = searchKeyword
      }
      
      const response = await articleApi.getArticles(params)
      if (response.code === 200) {
        setArticles(response.data.results || [])
        setTotalCount(response.data.count || 0)
        setTotalPages(Math.ceil((response.data.count || 0) / pageSize))
      }
    } catch (error) {
      console.error('Failed to fetch articles:', error)
    } finally {
      setLoading(false)
    }
  }, [currentPage, searchKeyword, pageSize])

  useEffect(() => {
    fetchArticles()
  }, [fetchArticles])

  const handleStar = async (articleId: number, isStarred: boolean | undefined) => {
    if (!isAuthenticated) {
      return
    }
    
    setActionLoading(articleId)
    try {
      await interactionApi.star('article', articleId)
      setArticles(prev =>
        prev.map(article =>
          article.id === articleId
            ? {
                ...article,
                is_starred: !isStarred,
                star_count: isStarred ? article.star_count - 1 : article.star_count + 1
              }
            : article
        )
      )
    } catch (error) {
      console.error('Failed to star article:', error)
    } finally {
      setActionLoading(null)
    }
  }

  const handleCollect = async (articleId: number, isCollected: boolean | undefined) => {
    if (!isAuthenticated) {
      return
    }
    
    setActionLoading(articleId)
    try {
      await interactionApi.collect('article', articleId)
      setArticles(prev =>
        prev.map(article =>
          article.id === articleId
            ? {
                ...article,
                is_collected: !isCollected,
                collection_count: isCollected ? article.collection_count - 1 : article.collection_count + 1
              }
            : article
        )
      )
    } catch (error) {
      console.error('Failed to collect article:', error)
    } finally {
      setActionLoading(null)
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setCurrentPage(1)
    setSearchParams(searchKeyword ? { search: searchKeyword } : {})
  }

  const renderPagination = () => {
    const pages = []
    const maxVisiblePages = 5
    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2))
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1)
    
    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1)
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(
        <button
          key={i}
          onClick={() => setCurrentPage(i)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            currentPage === i
              ? 'bg-primary text-white'
              : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
          }`}
        >
          {i}
        </button>
      )
    }

    return (
      <div className="flex items-center justify-center space-x-2">
        <button
          onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
          disabled={currentPage === 1}
          className="px-4 py-2 rounded-lg text-sm font-medium bg-white text-gray-700 hover:bg-gray-100 border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          上一页
        </button>
        {pages}
        <button
          onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
          disabled={currentPage === totalPages}
          className="px-4 py-2 rounded-lg text-sm font-medium bg-white text-gray-700 hover:bg-gray-100 border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          下一页
        </button>
      </div>
    )
  }

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">发现文章</h1>
          <p className="text-gray-600">探索社区中的优质内容</p>
        </div>

        {/* Search Bar */}
        <div className="mb-8">
          <form onSubmit={handleSearch} className="flex gap-4">
            <div className="flex-1 relative">
              <input
                type="text"
                value={searchKeyword}
                onChange={(e) => setSearchKeyword(e.target.value)}
                placeholder="搜索文章标题或内容..."
                className="w-full px-4 py-3 pl-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              />
              <svg
                className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
            <button
              type="submit"
              className="px-6 py-3 bg-primary text-white font-medium rounded-lg hover:bg-primary-dark transition-colors"
            >
              搜索
            </button>
          </form>
        </div>

        {/* Articles Grid */}
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : articles.length === 0 ? (
          <div className="text-center py-16">
            <svg
              className="mx-auto h-16 w-16 text-gray-400 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 mb-2">暂无文章</h3>
            <p className="text-gray-500">
              {searchKeyword ? '没有找到相关文章，尝试其他关键词' : '快来发布第一篇文章吧'}
            </p>
          </div>
        ) : (
          <>
            <div className="space-y-6">
              {articles.map((article) => (
                <article
                  key={article.id}
                  className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow"
                >
                  <div className="md:flex">
                    <div className="md:w-1/3">
                      <Link to={`/articles/${article.id}`}>
                        <div className="h-48 md:h-full bg-gradient-to-br from-gray-200 to-gray-300">
                          {article.default_img ? (
                            <img
                              src={article.default_img.startsWith('http') ? article.default_img : `/media/${article.default_img}`}
                              alt={article.title}
                              className="w-full h-full object-cover"
                            />
                          ) : (
                            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-primary/10 to-secondary/10">
                              <svg className="h-16 w-16 text-primary/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                              </svg>
                            </div>
                          )}
                        </div>
                      </Link>
                    </div>
                    <div className="p-6 md:w-2/3 flex flex-col justify-between">
                      <div>
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
                          <h2 className="text-xl font-semibold text-gray-900 mb-2 hover:text-primary transition-colors">
                            {article.title}
                          </h2>
                        </Link>
                        <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                          {article.content.replace(/<[^>]*>/g, '').substring(0, 150)}...
                        </p>
                      </div>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-6 text-sm text-gray-500">
                          <span className="flex items-center">
                            <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                            </svg>
                            {article.running_count} 阅读
                          </span>
                          <button
                            onClick={() => handleStar(article.id, article.is_starred)}
                            disabled={actionLoading === article.id}
                            className={`flex items-center transition-colors ${
                              article.is_starred ? 'text-red-500' : 'hover:text-red-500'
                            } disabled:opacity-50`}
                          >
                            <svg
                              className={`h-4 w-4 mr-1 ${article.is_starred ? 'fill-current' : ''}`}
                              fill={article.is_starred ? 'currentColor' : 'none'}
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                            >
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                            </svg>
                            {article.star_count} 点赞
                          </button>
                          <button
                            onClick={() => handleCollect(article.id, article.is_collected)}
                            disabled={actionLoading === article.id}
                            className={`flex items-center transition-colors ${
                              article.is_collected ? 'text-yellow-500' : 'hover:text-yellow-500'
                            } disabled:opacity-50`}
                          >
                            <svg
                              className={`h-4 w-4 mr-1 ${article.is_collected ? 'fill-current' : ''}`}
                              fill={article.is_collected ? 'currentColor' : 'none'}
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                            >
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                            </svg>
                            {article.collection_count} 收藏
                          </button>
                          <span className="flex items-center">
                            <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                            </svg>
                            {article.comment_count} 评论
                          </span>
                        </div>
                        <Link
                          to={`/articles/${article.id}`}
                          className="text-primary hover:text-primary-dark text-sm font-medium"
                        >
                          阅读全文 →
                        </Link>
                      </div>
                    </div>
                  </div>
                </article>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-12">
                {renderPagination()}
                <p className="text-center text-sm text-gray-500 mt-4">
                  共 {totalCount} 篇文章，当前第 {currentPage} / {totalPages} 页
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </MainLayout>
  )
}

export default ArticleListPage
