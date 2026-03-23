import React from 'react';
import { useQuery, useMutation } from 'react-query';
import { messageApi } from '@/api';
import { formatDate, getImageUrl } from '@/lib/utils';
import { toast } from 'sonner';

const MessagePage: React.FC = () => {
  const [page, setPage] = React.useState(1);

  const { data, isLoading, refetch } = useQuery(
    ['messages', page],
    () => messageApi.getList({ page, page_size: 20 }),
    { keepPreviousData: true }
  );

  const { data: unreadData } = useQuery(
    ['unread-count'],
    () => messageApi.getUnreadCount()
  );

  const markAllReadMutation = useMutation(
    () => messageApi.markAllRead(),
    {
      onSuccess: () => {
        refetch();
        toast.success('已全部标记为已读');
      },
    }
  );

  const messages = data?.data?.data?.items || [];
  const pagination = data?.data?.data?.pagination;
  const unreadCount = unreadData?.data?.data?.count || 0;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">消息通知</h1>
          {unreadCount > 0 && (
            <p className="text-sm text-gray-500 mt-1">
              有 {unreadCount} 条未读消息
            </p>
          )}
        </div>
        {unreadCount > 0 && (
          <button
            onClick={() => markAllReadMutation.mutate()}
            disabled={markAllReadMutation.isLoading}
            className="px-4 py-2 text-sm text-primary-600 hover:text-primary-700 disabled:opacity-50"
          >
            全部标记为已读
          </button>
        )}
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-500">加载中...</p>
        </div>
      ) : messages.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm p-8 text-center">
          <p className="text-gray-500">暂无消息</p>
        </div>
      ) : (
        <>
          <div className="bg-white rounded-lg shadow-sm divide-y">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`p-4 flex items-start space-x-4 ${
                  message.status === 1 ? 'bg-blue-50' : ''
                }`}
              >
                <img
                  src={getImageUrl(message.user_1.icon_url)}
                  alt={message.user_1.username}
                  className="w-10 h-10 rounded-full object-cover"
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-gray-900">
                      {message.user_1.username}
                    </p>
                    <p className="text-xs text-gray-500">
                      {formatDate(message.create_time)}
                    </p>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">
                    {message.type_display}
                  </p>
                </div>
                {message.status === 1 && (
                  <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                )}
              </div>
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

export default MessagePage;
