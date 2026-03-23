import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import { articleApi, videoApi } from '@/api';
import { formatDate, formatNumber, getImageUrl } from '@/lib/utils';

const HomePage: React.FC = () => {
  const { data: articlesData } = useQuery(
    ['articles', 'featured'],
    () => articleApi.getList({ page_size: 6 }),
    { staleTime: 60000 }
  );

  const { data: videosData } = useQuery(
    ['videos', 'featured'],
    () => videoApi.getList({ page_size: 4 }),
    { staleTime: 60000 }
  );

  const articles = articlesData?.data?.data?.items || [];
  const videos = videosData?.data?.data?.items || [];

  return (
    <div className="space-y-12">
      <section>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">热门文章</h2>
          <Link to="/articles" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
            查看更多 →
          </Link>
        </div>

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
                <h3 className="text-lg font-semibold text-gray-900 line-clamp-2 mb-2">
                  {article.title}
                </h3>
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
      </section>

      <section>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">推荐视频</h2>
          <Link to="/videos" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
            查看更多 →
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {videos.map((video) => (
            <Link
              key={video.id}
              to={`/videos/${video.id}`}
              className="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition-shadow"
            >
              <div className="relative">
                {video.img_path ? (
                  <img
                    src={getImageUrl(video.img_path)}
                    alt={video.title}
                    className="w-full h-40 object-cover"
                  />
                ) : (
                  <div className="w-full h-40 bg-gray-200 flex items-center justify-center">
                    <span className="text-gray-400">暂无封面</span>
                  </div>
                )}
                {video.duration_time && (
                  <span className="absolute bottom-2 right-2 bg-black bg-opacity-70 text-white text-xs px-2 py-1 rounded">
                    {video.duration_time}
                  </span>
                )}
              </div>
              <div className="p-3">
                <h3 className="text-sm font-medium text-gray-900 line-clamp-2">
                  {video.title}
                </h3>
                <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
                  <span>{video.user.username}</span>
                  <span>▶ {formatNumber(video.running_count)}</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
};

export default HomePage;
