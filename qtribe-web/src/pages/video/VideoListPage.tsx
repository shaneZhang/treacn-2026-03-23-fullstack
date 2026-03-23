import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import { videoApi } from '@/api';
import { formatDate, formatNumber, getImageUrl } from '@/lib/utils';

const VideoListPage: React.FC = () => {
  const [page, setPage] = React.useState(1);
  const [search, setSearch] = React.useState('');

  const { data, isLoading } = useQuery(
    ['videos', page, search],
    () => videoApi.getList({ page, page_size: 12, search }),
    { keepPreviousData: true }
  );

  const videos = data?.data?.data?.items || [];
  const pagination = data?.data?.data?.pagination;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">视频列表</h1>
      </div>

      <div className="mb-6">
        <input
          type="text"
          placeholder="搜索视频..."
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
      ) : videos.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">暂无视频</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
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
                <div className="p-4">
                  <h3 className="font-medium text-gray-900 line-clamp-2 mb-2">
                    {video.title || '未命名视频'}
                  </h3>
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <span>{video.user.username}</span>
                    <span>{formatDate(video.create_time)}</span>
                  </div>
                  <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                    <span>▶ {formatNumber(video.running_count)}</span>
                    <span>❤️ {formatNumber(video.star_count)}</span>
                    <span>💬 {formatNumber(video.comment_count)}</span>
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

export default VideoListPage;
