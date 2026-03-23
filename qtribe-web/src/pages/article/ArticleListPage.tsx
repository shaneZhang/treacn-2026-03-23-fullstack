import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import { articleApi } from '@/api';
import { formatDate, formatNumber, getImageUrl } from '@/lib/utils';

const ArticleListPage: React.FC = () => {
  const [page, setPage] = React.useState(1);
  const [search, setSearch] = React.useState('');

  const { data, isLoading } = useQuery(
    ['articles', page, search],
    () => articleApi.getList({ page, page_size: 12, search }),
    { keepPreviousData: true }
  );

  const articles = data?.data?.data?.items || [];
  const pagination = data?.data?.data?.pagination;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">文章列表</h1>
        <Link
          to="/articles/edit"
          className="bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-700"
        >
          发布文章
        </Link>
      </div>

      <div className="mb-6">
        <input
          type="text"
          placeholder="搜索文章..."
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
          className="w-full md:w-96 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
        />
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-500">加载中...</p>
        </div>
      ) : articles.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">暂无文章</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article) => (
              <Link
                key={article.id}
                to={`/articles/${article.id}`}
                className="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition-shadow"
              >
                {article.default_img_url && (
                  <img
                    src={getImageUrl(article.default_img_url)}
                    alt={article.title}
                    className="w-full h-48 object-cover"
                  />
                )}
                <div className="p-4">
                  <h2 className="text-lg font-semibold text-gray-900 line-clamp-2 mb-2">
                    {article.title}
                  </h2>
                  <p className="text-gray-600 text-sm line-clamp-2 mb-3">
                    {article.content.replace(/<[^>]*>/g, '').slice(0, 100)}
                  </p>
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <span>{article.user.username}</span>
                    <span>{formatDate(article.create_time)}</span>
                  </div>
                  <div className="flex items-center space-x-4 mt-3 text-sm text-gray-500">
                    <span>👁 {formatNumber(article.running_count)}</span>
                    <span>❤️ {formatNumber(article.star_count)}</span>
                    <span>💬 {formatNumber(article.comment_count)}</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>

          {pagination && pagination.total_pages > 1 && (
            <div className="flex justify-center mt-8 space-x-2">
              <button
                onClick={() => setPage(page - 1)}
                disabled={!pagination.has_previous}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                上一页
              </button>
              <span className="px-4 py-2 text-sm text-gray-700">
                {page} / {pagination.total_pages}
              </span>
              <button
                onClick={() => setPage(page + 1)}
                disabled={!pagination.has_next}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                下一页
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default ArticleListPage;
