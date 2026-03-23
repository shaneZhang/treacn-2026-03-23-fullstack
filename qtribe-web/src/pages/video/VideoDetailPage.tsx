import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { toast } from 'sonner';
import { videoApi, commentApi } from '@/api';
import { useAuthStore } from '@/stores/auth';
import { formatDate, formatNumber, getImageUrl } from '@/lib/utils';

const VideoDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const queryClient = useQueryClient();
  const { isAuthenticated } = useAuthStore();
  const [comment, setComment] = React.useState('');

  const { data, isLoading } = useQuery(
    ['video', id],
    () => videoApi.getDetail(Number(id)),
    { enabled: !!id }
  );

  const video = data?.data?.data;

  const starMutation = useMutation(
    () => videoApi.star(Number(id)),
    {
      onSuccess: (response) => {
        queryClient.invalidateQueries(['video', id]);
        toast.success(response.data.data?.is_starred ? '点赞成功' : '取消点赞');
      },
    }
  );

  const collectMutation = useMutation(
    () => videoApi.collect(Number(id)),
    {
      onSuccess: (response) => {
        queryClient.invalidateQueries(['video', id]);
        toast.success(response.data.data?.is_collected ? '收藏成功' : '取消收藏');
      },
    }
  );

  const commentMutation = useMutation(
    (content: string) => commentApi.create({ content, video: Number(id) }),
    {
      onSuccess: () => {
        setComment('');
        queryClient.invalidateQueries(['video', id]);
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

  if (!video) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">视频不存在</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <div className="relative bg-black">
          <video
            src={getImageUrl(video.video_url)}
            controls
            className="w-full max-h-[70vh]"
            poster={getImageUrl(video.img_path)}
          >
            您的浏览器不支持视频播放
          </video>
        </div>

        <div className="p-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            {video.title || '未命名视频'}
          </h1>

          <div className="flex items-center justify-between text-gray-500 mb-4">
            <div className="flex items-center space-x-4">
              <img
                src={getImageUrl(video.user.icon_url)}
                alt={video.user.username}
                className="w-10 h-10 rounded-full object-cover"
              />
              <div>
                <p className="font-medium text-gray-900">{video.user.username}</p>
                <p className="text-sm">{formatDate(video.create_time)}</p>
              </div>
            </div>
            <span className="text-sm">时长: {video.duration_time || '未知'}</span>
          </div>

          {video.remark && (
            <p className="text-gray-600 mb-4">{video.remark}</p>
          )}

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
                video.is_starred ? 'text-red-500' : 'text-gray-500'
              } hover:text-red-500`}
            >
              <span>❤️</span>
              <span>{formatNumber(video.star_count)}</span>
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
                video.is_collected ? 'text-yellow-500' : 'text-gray-500'
              } hover:text-yellow-500`}
            >
              <span>⭐</span>
              <span>{formatNumber(video.collection_count)}</span>
            </button>
            <span className="text-gray-500">▶ {formatNumber(video.running_count)}</span>
            <span className="text-gray-500">💬 {formatNumber(video.comment_count)}</span>
          </div>
        </div>
      </div>

      <section className="mt-8 bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-6">评论 ({video.comment_count})</h2>

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
            <a href="/login" className="text-primary-600 hover:underline">
              登录
            </a>
            后参与评论
          </p>
        )}
      </section>
    </div>
  );
};

export default VideoDetailPage;
