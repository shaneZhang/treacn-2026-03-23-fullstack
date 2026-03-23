import React from 'react';
import { useMutation, useQuery } from 'react-query';
import { toast } from 'sonner';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { authApi } from '@/api';
import { useAuthStore } from '@/stores/auth';
import { getImageUrl } from '@/lib/utils';

const profileSchema = z.object({
  email: z.string().email('请输入正确的邮箱').optional().or(z.literal('')),
  phone: z.string().regex(/^1[3-9]\d{9}$/, '请输入正确的手机号').optional().or(z.literal('')),
  personalized_signature: z.string().max(256, '个性签名最多256个字符').optional(),
  personal_introduce: z.string().max(1024, '个人介绍最多1024个字符').optional(),
  province: z.string().max(32).optional(),
  city: z.string().max(32).optional(),
  county: z.string().max(32).optional(),
  sex: z.enum(['1', '2']).optional(),
  age: z.number().min(1).max(150).optional(),
});

type ProfileFormData = z.infer<typeof profileSchema>;

const ProfilePage: React.FC = () => {
  const { user, setUser } = useAuthStore();
  const [avatarFile, setAvatarFile] = React.useState<File | null>(null);

  const { data: unreadData } = useQuery(
    ['unread-count'],
    () => authApi.getProfile(),
    { enabled: false }
  );

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      email: user?.email || '',
      phone: user?.phone || '',
      personalized_signature: user?.personalized_signature || '',
      personal_introduce: user?.personal_introduce || '',
      province: user?.province || '',
      city: user?.city || '',
      county: user?.county || '',
      sex: user?.sex || '1',
      age: user?.age || undefined,
    },
  });

  const updateMutation = useMutation(
    (data: ProfileFormData) => authApi.updateProfile(data),
    {
      onSuccess: (response) => {
        if (response.data.data) {
          setUser(response.data.data);
        }
        toast.success('更新成功');
      },
    }
  );

  const avatarMutation = useMutation(
    (file: File) => authApi.uploadAvatar(file),
    {
      onSuccess: (response) => {
        if (response.data.data && user) {
          setUser({ ...user, icon_url: response.data.data.icon_url });
        }
        toast.success('头像上传成功');
        setAvatarFile(null);
      },
    }
  );

  const onSubmit = (data: ProfileFormData) => {
    updateMutation.mutate(data);
  };

  if (!user) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">请先登录</p>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">个人中心</h1>

      <div className="bg-white rounded-lg shadow-sm p-8">
        <div className="flex items-center space-x-6 mb-8">
          <div className="relative">
            <img
              src={getImageUrl(user.icon_url)}
              alt={user.username}
              className="w-24 h-24 rounded-full object-cover"
            />
            <label className="absolute bottom-0 right-0 bg-primary-600 text-white rounded-full p-2 cursor-pointer hover:bg-primary-700">
              <input
                type="file"
                accept="image/*"
                className="hidden"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) {
                    setAvatarFile(file);
                    avatarMutation.mutate(file);
                  }
                }}
              />
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </label>
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-900">{user.username}</h2>
            <p className="text-gray-500">{user.personalized_signature || '这个人很懒，什么都没写'}</p>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-8 text-center">
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-2xl font-bold text-gray-900">{user.articles_count}</p>
            <p className="text-sm text-gray-500">文章</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-2xl font-bold text-gray-900">{user.followers_count}</p>
            <p className="text-sm text-gray-500">粉丝</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-2xl font-bold text-gray-900">{user.following_count}</p>
            <p className="text-sm text-gray-500">关注</p>
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
              <input
                {...register('email')}
                type="email"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">手机号</label>
              <input
                {...register('phone')}
                type="tel"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
              {errors.phone && (
                <p className="mt-1 text-sm text-red-600">{errors.phone.message}</p>
              )}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">个性签名</label>
            <input
              {...register('personalized_signature')}
              type="text"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              placeholder="一句话介绍自己"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">个人介绍</label>
            <textarea
              {...register('personal_introduce')}
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 resize-none"
              placeholder="详细介绍自己"
            />
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">省份</label>
              <input
                {...register('province')}
                type="text"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">城市</label>
              <input
                {...register('city')}
                type="text"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">区县</label>
              <input
                {...register('county')}
                type="text"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">性别</label>
              <select
                {...register('sex')}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="1">男</option>
                <option value="2">女</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">年龄</label>
              <input
                {...register('age', { valueAsNumber: true })}
                type="number"
                min={1}
                max={150}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={updateMutation.isLoading}
              className="px-6 py-2 bg-primary-600 text-white rounded-md text-sm font-medium hover:bg-primary-700 disabled:opacity-50"
            >
              {updateMutation.isLoading ? '保存中...' : '保存'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProfilePage;
