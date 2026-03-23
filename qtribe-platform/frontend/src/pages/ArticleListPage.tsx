import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { articleService } from '@services/article.service';
import { Article } from '@app-types/index';
import { Heart, Bookmark, Eye, MessageCircle, Search } from 'lucide-react';

function ArticleCard({ article }: { article: Article }) {
  return (
    <article className="bg-white rounded-lg shadow-sm border hover:shadow-md transition-shadow">
      <Link to={`/articles/${article.id}`}>
        {article.cover_image && (
          <img
            src={article.cover_image}
            alt={article.title}
            className="w-full h-48 object-cover rounded-t-lg"
          />
        )}
        <div className="p-6">
          <div className="flex items-center space-x-2 mb-3">
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
          
          <h2 className="text-xl font-bold text-gray-900 mb-2 line-clamp-2">
            {article.title}
          </h2>
          
          <p className="text-gray-600 text-sm mb-4 line-clamp-3">
            {article.summary || '暂无摘要'}
          </p>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <img
                src={article.author.avatar || '/default-avatar.png'}
                alt={article.author.username}
                className="h-8 w-8 rounded-full object-cover"
              />
              <span className="text-sm text-gray-700">{article.author.username}</span>
            </div>
            
            <div className="flex items-center space-x-4 text-gray-500 text-sm">
              <span className="flex items-center space-x-1">
                <Eye className="h-4 w-4" />
                <span>{article.view_count}</span>
              </span>
              <span className="flex items-center space-x-1">
                <Heart className={`h-4 w-4 ${article.is_liked ? 'fill-red-500 text-red-500' : ''}`} />
                <span>{article.like_count}</span>
              </span>
              <span className="flex items-center space-x-1">
                <Bookmark className={`h-4 w-4 ${article.is_collected ? 'fill-yellow-500 text-yellow-500' : ''}`} />
                <span>{article.collect_count}</span>
              </span>
              <span className="flex items-center space-x-1">
                <MessageCircle className="h-4 w-4" />
                <span>{article.comment_count}</span>
              </span>
            </div>
          </div>
        </div>
      </Link>
    </article>
  );
}

export function ArticleListPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);

  const { data, isLoading, error } = useQuery({
    queryKey: ['articles', 'list', currentPage, searchQuery],
    queryFn: () =>
      articleService.getArticles({
        page: currentPage,
        page_size: 12,
        search: searchQuery || undefined,
      }),
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">加载失败，请稍后重试</p>
      </div>
    );
  }

  const articles = data?.data?.results || [];
  const pagination = data?.data?.pagination;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-2xl font-bold text-gray-900">文章列表</h1>
        
        <form onSubmit={handleSearch} className="flex w-full sm:w-auto">
          <div className="relative flex-1 sm:flex-none">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="搜索文章..."
              className="w-full sm:w-64 pl-10 pr-4 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
          </div>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-r-md hover:bg-blue-700"
          >
            搜索
          </button>
        </form>
      </div>

      {articles.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          暂无文章
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>

          {pagination && pagination.total_pages > 1 && (
            <div className="flex justify-center space-x-2 mt-8">
              <button
                onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                disabled={!pagination.has_previous}
                className="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                上一页
              </button>
              <span className="px-4 py-2 text-gray-700">
                {currentPage} / {pagination.total_pages}
              </span>
              <button
                onClick={() => setCurrentPage((p) => Math.min(pagination.total_pages, p + 1))}
                disabled={!pagination.has_next}
                className="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                下一页
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
