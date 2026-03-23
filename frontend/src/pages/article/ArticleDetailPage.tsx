import React, { useEffect, useState, useCallback } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import MainLayout from '../../components/layout/MainLayout'
import { articleApi } from '../../services/article'
import { interactionApi } from '../../services/interaction'
import type { Article, Comment } from '../../types'
import { useAuthContext } from '../../context/AuthContext'

const ArticleDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const [article, setArticle] = useState<Article | null>(null)
  const [comments, setComments] = useState<Comment[]>([])
  const [loading, setLoading] = useState(true)
  const [commentLoading, setCommentLoading] = useState(false)
  const [actionLoading, setActionLoading] = useState(false)
  const [newComment, setNewComment] = useState('')
  const [submitError, setSubmitError] = useState('')
  
  const { user, isAuthenticated } = useAuthContext()
  const navigate = useNavigate()

  const fetchArticle = useCallback(async () => {
    if (!id) return
    
    setLoading(true)
    try {
      const [articleResponse, commentsResponse] = await Promise.all([
        articleApi.getArticle(parseInt(id)),
        articleApi.getComments(parseInt(id))
      ])
      
      if (articleResponse.code === 200) {
        setArticle(articleResponse.data)
      }
      if (commentsResponse.code === 200) {
        setComments(commentsResponse.data || [])
      }
    } catch (error) {
      console.error('Failed to fetch article:', error)
    } finally {
      setLoading(false)
    }
  }, [id])

  useEffect(() => {
    fetchArticle()
  }, [fetchArticle])

  const handleStar = async () => {
    if (!isAuthenticated || !article) {
      navigate('/login')
      return
    }
    
    setActionLoading(true)
    try {
      await interactionApi.star('article', article.id)
      setArticle(prev =>
        prev ? {
          ...prev,
          is_starred: !prev.is_starred,
          star_count: prev.is_starred ? prev.star_count - 1 : prev.star_count + 1
        } : null
      )
    } catch (error) {
      console.error('Failed to star article:', error)
    } finally {
      setActionLoading(false)
    }
  }

  const handleCollect = async () => {
    if (!isAuthenticated || !article) {
      navigate('/login')
      return
    }
    
    setActionLoading(true)
    try {
      await interactionApi.collect('article', article.id)
      setArticle(prev =>
        prev ? {
          ...prev,
          is_collected: !prev.is_collected,
          collection_count: prev.is_collected ? prev.collection_count - 1 : prev.collection_count + 1
        } : null
      )
    } catch (error) {
      console.error('Failed to collect article:', error)
    } finally {
      setActionLoading(false)
    }
  }

  const handleSubmitComment = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!isAuthenticated) {
      navigate('/login')
      return
    }
    
    if (!newComment.trim() || !article) {
      return
    }
    
    setCommentLoading(true)
    setSubmitError('')
    
    try {
      const response = await articleApi.addComment(article.id, newComment.trim())
      if (response.code === 201) {
        setComments(prev => [response.data, ...prev])
        setNewComment('')
        setArticle(prev =>
          prev ? { ...prev, comment_count: prev.comment_count + 1 } : null
        )
      } else {
        setSubmitError(response.message || '评论失败')
      }
    } catch (error: any) {
      setSubmitError(error.message || '评论失败，请稍后重试')
    } finally {
      setCommentLoading(false)
    }
  }

  if (loading) {
    return (
      <MainLayout>
        <div className="flex justify-center items-center min-h-screen">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      </MainLayout>
    )
  }

  if (!article) {
    return (
      <MainLayout>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">文章不存在</h1>
            <Link to="/articles" className="text-primary hover:text-primary-dark">
              返回文章列表
            </Link>
          </div>
        </div>
      </MainLayout>
    )
  }

  return (
    <MainLayout>
      <article className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Article Header */}
        <header className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            {article.title}
          </h1>
          
          <div className="flex items-center flex-wrap gap-4 mb-6">
            <div className="flex items-center">
              {article.user?.icon ? (
                <img
                  src={article.user.icon.startsWith('http') ? article.user.icon : `/media/${article.user.icon}`}
                  alt={article.user.username}
                  className="h-10 w-10 rounded-full object-cover"
                />
              ) : (
                <div className="h-10 w-10 rounded-full bg-gradient-to-r from-primary to-secondary flex items-center justify-center text-white font-medium">
                  {article.user?.username?.charAt(0).toUpperCase()}
                </div>
              )}
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-900">{article.user?.username}</p>
                <p className="text-sm text-gray-500">
                  {new Date(article.create_time).toLocaleDateString('zh-CN', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </p>
              </div>
            </div>
          </div>

          {/* Cover Image */}
          {article.default_img && (
            <div className="rounded-xl overflow-hidden mb-6">
              <img
                src={article.default_img.startsWith('http') ? article.default_img : `/media/${article.default_img}`}
                alt={article.title}
                className="w-full h-64 md:h-96 object-cover"
              />
            </div>
          )}

          {/* Action Bar */}
          <div className="flex items-center justify-between py-4 border-y border-gray-200">
            <div className="flex items-center space-x-6">
              <span className="flex items-center text-gray-500">
                <svg className="h-5 w-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                {article.running_count} 阅读
              </span>
              <span className="flex items-center text-gray-500">
                <svg className="h-5 w-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                {article.comment_count} 评论
              </span>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={handleStar}
                disabled={actionLoading}
                className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                  article.is_starred
                    ? 'bg-red-50 text-red-500'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                } disabled:opacity-50`}
              >
                <svg
                  className={`h-5 w-5 mr-1 ${article.is_starred ? 'fill-current' : ''}`}
                  fill={article.is_starred ? 'currentColor' : 'none'}
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
                {article.star_count} 点赞
              </button>
              
              <button
                onClick={handleCollect}
                disabled={actionLoading}
                className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                  article.is_collected
                    ? 'bg-yellow-50 text-yellow-600'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                } disabled:opacity-50`}
              >
                <svg
                  className={`h-5 w-5 mr-1 ${article.is_collected ? 'fill-current' : ''}`}
                  fill={article.is_collected ? 'currentColor' : 'none'}
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                </svg>
                {article.collection_count} 收藏
              </button>
            </div>
          </div>
        </header>

        {/* Article Content */}
        <div className="mb-12">
          <div 
            className="prose prose-lg max-w-none text-gray-700 leading-relaxed"
            dangerouslySetInnerHTML={{ __html: article.content }}
          />
        </div>

        {/* Tags (if any) */}
        <div className="flex flex-wrap gap-2 mb-12 pb-8 border-b border-gray-200">
          <span className="text-sm text-gray-500">标签：</span>
          <span className="px-3 py-1 bg-gray-100 text-gray-600 text-sm rounded-full">
            技术分享
          </span>
          <span className="px-3 py-1 bg-gray-100 text-gray-600 text-sm rounded-full">
            编程
          </span>
        </div>

        {/* Comments Section */}
        <section>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            评论 ({article.comment_count})
          </h2>

          {/* Comment Form */}
          {isAuthenticated ? (
            <form onSubmit={handleSubmitComment} className="mb-8">
              {submitError && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm mb-4">
                  {submitError}
                </div>
              )}
              <div className="flex items-start space-x-4">
                {user?.icon ? (
                  <img
                    src={user.icon.startsWith('http') ? user.icon : `/media/${user.icon}`}
                    alt={user.username}
                    className="h-10 w-10 rounded-full object-cover"
                  />
                ) : (
                  <div className="h-10 w-10 rounded-full bg-gradient-to-r from-primary to-secondary flex items-center justify-center text-white font-medium flex-shrink-0">
                    {user?.username?.charAt(0).toUpperCase()}
                  </div>
                )}
                <div className="flex-1">
                  <textarea
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    placeholder="写下您的评论..."
                    rows={3}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
                  />
                  <div className="flex justify-end mt-2">
                    <button
                      type="submit"
                      disabled={commentLoading || !newComment.trim()}
                      className="px-6 py-2 bg-primary text-white font-medium rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {commentLoading ? '发布中...' : '发布评论'}
                    </button>
                  </div>
                </div>
              </div>
            </form>
          ) : (
            <div className="bg-gray-50 rounded-lg p-6 text-center mb-8">
              <p className="text-gray-600 mb-4">登录后即可发表评论</p>
              <Link
                to="/login"
                className="inline-block px-6 py-2 bg-primary text-white font-medium rounded-lg hover:bg-primary-dark transition-colors"
              >
                立即登录
              </Link>
            </div>
          )}

          {/* Comments List */}
          <div className="space-y-6">
            {comments.length === 0 ? (
              <div className="text-center py-8">
                <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                <p className="text-gray-500">暂无评论，快来抢沙发吧！</p>
              </div>
            ) : (
              comments.map((comment) => (
                <div key={comment.id} className="flex space-x-4">
                  {comment.user?.icon ? (
                    <img
                      src={comment.user.icon.startsWith('http') ? comment.user.icon : `/media/${comment.user.icon}`}
                      alt={comment.user.username}
                      className="h-10 w-10 rounded-full object-cover flex-shrink-0"
                    />
                  ) : (
                    <div className="h-10 w-10 rounded-full bg-gradient-to-r from-primary to-secondary flex items-center justify-center text-white font-medium flex-shrink-0">
                      {comment.user?.username?.charAt(0).toUpperCase()}
                    </div>
                  )}
                  <div className="flex-1">
                    <div className="bg-gray-50 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium text-gray-900">{comment.user?.username}</span>
                        <span className="text-sm text-gray-500">
                          {new Date(comment.create_time).toLocaleDateString('zh-CN', {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </span>
                      </div>
                      <p className="text-gray-700">{comment.content}</p>
                    </div>
                    
                    {/* Comment Actions */}
                    <div className="flex items-center space-x-4 mt-2 ml-2">
                      <button className="text-sm text-gray-500 hover:text-primary">
                        回复
                      </button>
                    </div>

                    {/* Nested Replies */}
                    {comment.replies && comment.replies.length > 0 && (
                      <div className="mt-4 ml-6 space-y-4">
                        {comment.replies.map((reply) => (
                          <div key={reply.id} className="flex space-x-3">
                            {reply.user?.icon ? (
                              <img
                                src={reply.user.icon.startsWith('http') ? reply.user.icon : `/media/${reply.user.icon}`}
                                alt={reply.user.username}
                                className="h-8 w-8 rounded-full object-cover flex-shrink-0"
                              />
                            ) : (
                              <div className="h-8 w-8 rounded-full bg-gradient-to-r from-primary to-secondary flex items-center justify-center text-white text-sm font-medium flex-shrink-0">
                                {reply.user?.username?.charAt(0).toUpperCase()}
                              </div>
                            )}
                            <div className="flex-1 bg-gray-50 rounded-lg p-3">
                              <div className="flex items-center justify-between mb-1">
                                <span className="text-sm font-medium text-gray-900">{reply.user?.username}</span>
                                <span className="text-xs text-gray-500">
                                  {new Date(reply.create_time).toLocaleDateString('zh-CN')}
                                </span>
                              </div>
                              <p className="text-sm text-gray-700">{reply.content}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </section>
      </article>
    </MainLayout>
  )
}

export default ArticleDetailPage
