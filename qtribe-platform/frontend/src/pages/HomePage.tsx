import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { articleService } from '@services/article.service';
import { Article } from '@app-types/index';
import { Heart, Bookmark, Eye, MessageCircle } from 'lucide-react';

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

export function HomePage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['articles', 'home'],
    queryFn: () => articleService.getArticles({ page_size: 10 }),
  });

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

  return (
    <div className="space-y-8">
      <div className="text-center py-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg text-white">
        <h1 className="text-4xl font-bold mb-4">欢迎来到 QTribe</h1>
        <p className="text-xl mb-6">分享你的故事，连接世界</p>
        <Link
          to="/articles/create"
          className="inline-block bg-white text-blue-600 px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors"
        >
          开始创作
        </Link>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">最新文章</h2>
        {articles.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            暂无文章，来发表第一篇吧！
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        )}
      </div>

      {articles.length > 0 && (
        <div className="text-center">
          <Link
            to="/articles"
            className="inline-block text-blue-600 hover:text-blue-800 font-medium"
          >
            查看更多文章 →
          </Link>
        </div>
      )}
    </div>
  );
}
