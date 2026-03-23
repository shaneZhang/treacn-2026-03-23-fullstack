import { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { articleService } from '@services/article.service';
import { interactionService } from '@services/interaction.service';
import { useAuthStore } from '@stores/auth.store';
import { Heart, Bookmark, Eye, MessageCircle, ArrowLeft, Edit, Trash2 } from 'lucide-react';

export function ArticleDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { isAuthenticated } = useAuthStore();
  const [commentContent, setCommentContent] = useState('');

  const { data: articleData, isLoading: articleLoading } = useQuery({
    queryKey: ['article', id],
    queryFn: () => articleService.getArticle(id!),
    enabled: !!id,
  });

  const { data: commentsData } = useQuery({
    queryKey: ['comments', id],
    queryFn: () => articleService.getComments(id!),
    enabled: !!id,
  });

  const likeMutation = useMutation({
    mutationFn: () => interactionService.toggleLike({ article: id! }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['article', id] });
    },
  });

  const collectMutation = useMutation({
    mutationFn: () => interactionService.toggleCollection({ article: id! }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['article', id] });
    },
  });

  const commentMutation = useMutation({
    mutationFn: (content: string) => articleService.createComment(id!, { content }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comments', id] });
      queryClient.invalidateQueries({ queryKey: ['article', id] });
      setCommentContent('');
    },
  });

  const deleteMutation = useMutation({
    mutationFn: () => articleService.deleteArticle(id!),
    onSuccess: () => {
      navigate('/articles');
    },
  });

  if (articleLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const article = articleData?.data;
  const comments = commentsData?.data?.results || [];

  if (!article) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">文章不存在</p>
        <Link to="/articles" className="text-blue-600 hover:underline mt-2 inline-block">
          返回文章列表
        </Link>
      </div>
    );
  }

  const handleLike = () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    likeMutation.mutate();
  };

  const handleCollect = () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    collectMutation.mutate();
  };

  const handleComment = (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentContent.trim()) return;
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    commentMutation.mutate(commentContent);
  };

  const handleDelete = () => {
    if (confirm('确定要删除这篇文章吗？')) {
      deleteMutation.mutate();
    }
  };

  return (
    <article className="max-w-4xl mx-auto">
      <button
        onClick={() => navigate(-1)}
        className="flex items-center text-gray-600 hover:text-gray-900 mb-4"
      >
        <ArrowLeft className="h-4 w-4 mr-1" />
        返回
      </button>

      <div className="bg-white rounded-lg shadow-sm border p-8">
        <div className="flex items-center space-x-2 mb-4">
          {article.is_top && (
            <span className="bg-red-100 text-red-800 text-xs font-medium px-2.5 py-0.5 rounded">
              置顶
            </span>
          )}
          {article.tags.map((tag) => (
            <span
              key={tag.id}
              className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded"
            >
              {tag.name}
            </span>
          ))}
        </div>

        <h1 className="text-3xl font-bold text-gray-900 mb-4">{article.title}</h1>

        <div className="flex items-center justify-between mb-6 pb-6 border-b">
          <div className="flex items-center space-x-3">
            <img
              src={article.author.avatar || '/default-avatar.png'}
              alt={article.author.username}
              className="h-10 w-10 rounded-full object-cover"
            />
            <div>
              <p className="font-medium text-gray-900">{article.author.username}</p>
              <p className="text-sm text-gray-500">
                {new Date(article.published_at || article.create_time).toLocaleDateString()}
              </p>
            </div>
          </div>

          {article.is_author && (
            <div className="flex space-x-2">
              <Link
                to={`/articles/${article.id}/edit`}
                className="flex items-center px-3 py-1.5 text-sm text-blue-600 hover:bg-blue-50 rounded"
              >
                <Edit className="h-4 w-4 mr-1" />
                编辑
              </Link>
              <button
                onClick={handleDelete}
                className="flex items-center px-3 py-1.5 text-sm text-red-600 hover:bg-red-50 rounded"
              >
                <Trash2 className="h-4 w-4 mr-1" />
                删除
              </button>
            </div>
          )}
        </div>

        {article.cover_image && (
          <img
            src={article.cover_image}
            alt={article.title}
            className="w-full h-64 object-cover rounded-lg mb-6"
          />
        )}

        <div
          className="prose max-w-none mb-8"
          dangerouslySetInnerHTML={{ __html: article.content }}
        />

        <div className="flex items-center justify-between pt-6 border-t">
          <div className="flex items-center space-x-6">
            <button
              onClick={handleLike}
              className={`flex items-center space-x-2 ${article.is_liked ? 'text-red-500' : 'text-gray-500'} hover:text-red-500`}
            >
              <Heart className={`h-5 w-5 ${article.is_liked ? 'fill-current' : ''}`} />
              <span>{article.like_count}</span>
            </button>
            <button
              onClick={handleCollect}
              className={`flex items-center space-x-2 ${article.is_collected ? 'text-yellow-500' : 'text-gray-500'} hover:text-yellow-500`}
            >
              <Bookmark className={`h-5 w-5 ${article.is_collected ? 'fill-current' : ''}`} />
              <span>{article.collect_count}</span>
            </button>
            <span className="flex items-center space-x-2 text-gray-500">
              <MessageCircle className="h-5 w-5" />
              <span>{article.comment_count}</span>
            </span>
          </div>
          <span className="flex items-center space-x-2 text-gray-500">
            <Eye className="h-5 w-5" />
            <span>{article.view_count}</span>
          </span>
        </div>
      </div>

      <div className="mt-8 bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4">
          评论 ({article.comment_count})
        </h3>

        {isAuthenticated && (
          <form onSubmit={handleComment} className="mb-6">
            <textarea
              value={commentContent}
              onChange={(e) => setCommentContent(e.target.value)}
              placeholder="写下你的评论..."
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div className="mt-2 flex justify-end">
              <button
                type="submit"
                disabled={commentMutation.isPending || !commentContent.trim()}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {commentMutation.isPending ? '发布中...' : '发布评论'}
              </button>
            </div>
          </form>
        )}

        <div className="space-y-4">
          {comments.length === 0 ? (
            <p className="text-center text-gray-500 py-4">暂无评论，来发表第一条评论吧</p>
          ) : (
            comments.map((comment) => (
              <div key={comment.id} className="flex space-x-3 pb-4 border-b last:border-0">
                <img
                  src={comment.author.avatar || '/default-avatar.png'}
                  alt={comment.author.username}
                  className="h-10 w-10 rounded-full object-cover"
                />
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-gray-900">{comment.author.username}</span>
                    <span className="text-sm text-gray-500">
                      {new Date(comment.create_time).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="text-gray-700 mt-1">{comment.content}</p>
                  <div className="flex items-center space-x-4 mt-2">
                    <button className="flex items-center space-x-1 text-gray-500 hover:text-red-500 text-sm">
                      <Heart className="h-4 w-4" />
                      <span>{comment.like_count}</span>
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </article>
  );
}
