import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { toast } from 'sonner';
import { articleApi, commentApi } from '@/api';
import { useAuthStore } from '@/stores/auth';
import { formatDate, formatNumber, getImageUrl } from '@/lib/utils';

const ArticleDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const queryClient = useQueryClient();
  const { user, isAuthenticated } = useAuthStore();
  const [comment, setComment] = React.useState('');

  const { data, isLoading } = useQuery(
    ['article', id],
    () => articleApi.getDetail(Number(id)),
    { enabled: !!id }
  );

  const article = data?.data?.data;

  const starMutation = useMutation(
    () => articleApi.star(Number(id)),
    {
      onSuccess: (response) => {
        queryClient.invalidateQueries(['article', id]);
        toast.success(response.data.data?.is_starred ? '点赞成功' : '取消点赞');
      },
    }
  );

  const collectMutation = useMutation(
    () => articleApi.collect(Number(id)),
    {
      onSuccess: (response) => {
        queryClient.invalidateQueries(['article', id]);
        toast.success(response.data.data?.is_collected ? '收藏成功' : '取消收藏');
      },
    }
  );

  const commentMutation = useMutation(
    (content: string) => commentApi.create({ content, article: Number(id) }),
    {
      onSuccess: () => {
        setComment('');
        queryClient.invalidateQueries(['article', id]);
        toast.success('评论成功');
      },
    }
  );

  if (isLoading) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">加载中...</p>
      </div>
    );
  }

  if (!article) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">文章不存在</p>
        <Link to="/articles" className="text-primary-600 hover:underline mt-4 inline-block">
          返回文章列表
        </Link>
      </div>
    );
  }

  const isAuthor = user?.id === article.user.id;

  return (
    <div className="max-w-4xl mx-auto">
      <article className="bg-white rounded-lg shadow-sm p-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">{article.title}</h1>
          <div className="flex items-center justify-between text-gray-500">
            <div className="flex items-center space-x-4">
              <img
                src={getImageUrl(article.user.icon_url)}
                alt={article.user.username}
                className="w-10 h-10 rounded-full object-cover"
              />
              <div>
                <p className="font-medium text-gray-900">{article.user.username}</p>
                <p className="text-sm">{formatDate(article.create_time)}</p>
              </div>
            </div>
            {isAuthor && (
              <Link
                to={`/articles/edit/${article.id}`}
                className="text-primary-600 hover:text-primary-700 text-sm"
              >
                编辑
              </Link>
            )}
          </div>
        </header>

        {article.default_img_url && (
          <img
            src={getImageUrl(article.default_img_url)}
            alt={article.title}
            className="w-full rounded-lg mb-8"
          />
        )}

        <div
          className="prose prose-lg max-w-none mb-8"
          dangerouslySetInnerHTML={{ __html: article.content }}
        />

        <div className="flex items-center space-x-6 py-4 border-t border-b">
          <button
            onClick={() => {
              if (!isAuthenticated) {
                toast.error('请先登录');
                return;
              }
              starMutation.mutate();
            }}
            className={`flex items-center space-x-2 ${
              article.is_starred ? 'text-red-500' : 'text-gray-500'
            } hover:text-red-500`}
          >
            <span>❤️</span>
            <span>{formatNumber(article.star_count)}</span>
          </button>
          <button
            onClick={() => {
              if (!isAuthenticated) {
                toast.error('请先登录');
                return;
              }
              collectMutation.mutate();
            }}
            className={`flex items-center space-x-2 ${
              article.is_collected ? 'text-yellow-500' : 'text-gray-500'
            } hover:text-yellow-500`}
          >
            <span>⭐</span>
            <span>{formatNumber(article.collection_count)}</span>
          </button>
          <span className="text-gray-500">👁 {formatNumber(article.running_count)}</span>
          <span className="text-gray-500">💬 {formatNumber(article.comment_count)}</span>
        </div>
      </article>

      <section className="mt-8 bg-white rounded-lg shadow-sm p-8">
        <h2 className="text-xl font-bold text-gray-900 mb-6">评论 ({article.comment_count})</h2>

        {isAuthenticated ? (
          <div className="mb-6">
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="写下你的评论..."
              className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 resize-none"
              rows={3}
            />
            <button
              onClick={() => {
                if (!comment.trim()) {
                  toast.error('请输入评论内容');
                  return;
                }
                commentMutation.mutate(comment);
              }}
              disabled={commentMutation.isLoading}
              className="mt-2 px-4 py-2 bg-primary-600 text-white rounded-md text-sm hover:bg-primary-700 disabled:opacity-50"
            >
              发表评论
            </button>
          </div>
        ) : (
          <p className="text-gray-500 mb-6">
            <Link to="/login" className="text-primary-600 hover:underline">
              登录
            </Link>
            后参与评论
          </p>
        )}
      </section>
    </div>
  );
};

export default ArticleDetailPage;
