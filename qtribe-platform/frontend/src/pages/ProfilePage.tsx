import { useState, useRef } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { authService } from '@services/auth.service';
import { articleService } from '@services/article.service';
import { interactionService } from '@services/interaction.service';
import { useAuthStore } from '@stores/auth.store';
import { Article, Collection, Like } from '@app-types/index';
import { Heart, Bookmark, FileText, User, Camera, Edit2, Save, X } from 'lucide-react';

type TabType = 'articles' | 'collections' | 'likes' | 'settings';

export function ProfilePage() {
  const queryClient = useQueryClient();
  const { user, updateUser } = useAuthStore();
  const [activeTab, setActiveTab] = useState<TabType>('articles');
  const [isEditing, setIsEditing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [editForm, setEditForm] = useState({
    username: user?.username || '',
    signature: user?.signature || '',
    introduction: user?.introduction || '',
    province: user?.province || '',
    city: user?.city || '',
    district: user?.district || '',
    gender: user?.gender || 0,
  });

  const { data: profileData } = useQuery({
    queryKey: ['profile'],
    queryFn: authService.getProfile,
  });

  const { data: myArticles } = useQuery({
    queryKey: ['myArticles'],
    queryFn: () => articleService.getMyArticles(),
    enabled: activeTab === 'articles',
  });

  const { data: myCollections } = useQuery({
    queryKey: ['myCollections'],
    queryFn: () => interactionService.getCollections(),
    enabled: activeTab === 'collections',
  });

  const { data: myLikes } = useQuery({
    queryKey: ['myLikes'],
    queryFn: () => interactionService.getLikes({ type: 'article' }),
    enabled: activeTab === 'likes',
  });

  const updateProfileMutation = useMutation({
    mutationFn: authService.updateProfile,
    onSuccess: (response) => {
      if (response.code === 200) {
        updateUser(response.data);
        setIsEditing(false);
      }
    },
  });

  const uploadAvatarMutation = useMutation({
    mutationFn: authService.uploadAvatar,
    onSuccess: (response) => {
      if (response.code === 200) {
        updateUser({ avatar: response.data.avatar });
        queryClient.invalidateQueries({ queryKey: ['profile'] });
      }
    },
  });

  const handleAvatarClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      uploadAvatarMutation.mutate(file);
    }
  };

  const handleSaveProfile = () => {
    updateProfileMutation.mutate(editForm);
  };

  const profile = profileData?.data;

  const tabs = [
    { id: 'articles' as TabType, label: '我的文章', icon: FileText },
    { id: 'collections' as TabType, label: '我的收藏', icon: Bookmark },
    { id: 'likes' as TabType, label: '我的点赞', icon: Heart },
    { id: 'settings' as TabType, label: '个人设置', icon: User },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
        <div className="flex items-start space-x-6">
          <div className="relative">
            <img
              src={user?.avatar || '/default-avatar.png'}
              alt={user?.username}
              className="h-24 w-24 rounded-full object-cover"
            />
            <button
              onClick={handleAvatarClick}
              className="absolute bottom-0 right-0 bg-blue-600 text-white p-1.5 rounded-full hover:bg-blue-700"
            >
              <Camera className="h-4 w-4" />
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="hidden"
            />
          </div>
          <div className="flex-1">
            <h1 className="text-2xl font-bold text-gray-900">{user?.username}</h1>
            <p className="text-gray-600 mt-1">{user?.signature || '这个人很懒，什么都没写'}</p>
            <div className="flex space-x-6 mt-4 text-sm text-gray-500">
              <span>文章 {profile?.articles_count || 0}</span>
              <span>粉丝 {profile?.followers_count || 0}</span>
              <span>关注 {profile?.following_count || 0}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex space-x-6">
        <div className="w-48 flex-shrink-0">
          <nav className="space-y-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left ${
                    activeTab === tab.id
                      ? 'bg-blue-50 text-blue-600'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        <div className="flex-1 bg-white rounded-lg shadow-sm border p-6">
          {activeTab === 'articles' && (
            <div>
              <h2 className="text-lg font-bold text-gray-900 mb-4">我的文章</h2>
              {myArticles?.data?.results.length === 0 ? (
                <p className="text-gray-500 text-center py-8">还没有发布文章</p>
              ) : (
                <div className="space-y-4">
                  {myArticles?.data?.results.map((article: Article) => (
                    <div key={article.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div>
                        <h3 className="font-medium text-gray-900">{article.title}</h3>
                        <p className="text-sm text-gray-500 mt-1">
                          {new Date(article.create_time).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <span>阅读 {article.view_count}</span>
                        <span>点赞 {article.like_count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'collections' && (
            <div>
              <h2 className="text-lg font-bold text-gray-900 mb-4">我的收藏</h2>
              {myCollections?.data?.results.length === 0 ? (
                <p className="text-gray-500 text-center py-8">还没有收藏文章</p>
              ) : (
                <div className="space-y-4">
                  {myCollections?.data?.results.map((collection: Collection) => (
                    <div key={collection.id} className="p-4 border rounded-lg">
                      <h3 className="font-medium text-gray-900">{collection.article.title}</h3>
                      <p className="text-sm text-gray-500 mt-1">
                        作者: {collection.article.author.username}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'likes' && (
            <div>
              <h2 className="text-lg font-bold text-gray-900 mb-4">我的点赞</h2>
              {myLikes?.data?.results.length === 0 ? (
                <p className="text-gray-500 text-center py-8">还没有点赞文章</p>
              ) : (
                <div className="space-y-4">
                  {myLikes?.data?.results.map((like: Like) => (
                    <div key={like.id} className="p-4 border rounded-lg">
                      {like.article && (
                        <>
                          <h3 className="font-medium text-gray-900">{like.article.title}</h3>
                          <p className="text-sm text-gray-500 mt-1">
                            作者: {like.article.author.username}
                          </p>
                        </>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'settings' && (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold text-gray-900">个人设置</h2>
                {!isEditing ? (
                  <button
                    onClick={() => setIsEditing(true)}
                    className="flex items-center space-x-1 text-blue-600 hover:text-blue-800"
                  >
                    <Edit2 className="h-4 w-4" />
                    <span>编辑</span>
                  </button>
                ) : (
                  <div className="flex space-x-2">
                    <button
                      onClick={handleSaveProfile}
                      disabled={updateProfileMutation.isPending}
                      className="flex items-center space-x-1 text-green-600 hover:text-green-800"
                    >
                      <Save className="h-4 w-4" />
                      <span>保存</span>
                    </button>
                    <button
                      onClick={() => setIsEditing(false)}
                      className="flex items-center space-x-1 text-gray-600 hover:text-gray-800"
                    >
                      <X className="h-4 w-4" />
                      <span>取消</span>
                    </button>
                  </div>
                )}
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">用户名</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.username}
                      onChange={(e) => setEditForm({ ...editForm, username: e.target.value })}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
                    />
                  ) : (
                    <p className="mt-1 text-gray-900">{user?.username}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">个性签名</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.signature}
                      onChange={(e) => setEditForm({ ...editForm, signature: e.target.value })}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
                    />
                  ) : (
                    <p className="mt-1 text-gray-900">{user?.signature || '未设置'}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">个人简介</label>
                  {isEditing ? (
                    <textarea
                      value={editForm.introduction}
                      onChange={(e) => setEditForm({ ...editForm, introduction: e.target.value })}
                      rows={3}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
                    />
                  ) : (
                    <p className="mt-1 text-gray-900">{user?.introduction || '未设置'}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">所在地</label>
                  {isEditing ? (
                    <div className="grid grid-cols-3 gap-2 mt-1">
                      <input
                        type="text"
                        placeholder="省"
                        value={editForm.province}
                        onChange={(e) => setEditForm({ ...editForm, province: e.target.value })}
                        className="px-3 py-2 border border-gray-300 rounded-md"
                      />
                      <input
                        type="text"
                        placeholder="市"
                        value={editForm.city}
                        onChange={(e) => setEditForm({ ...editForm, city: e.target.value })}
                        className="px-3 py-2 border border-gray-300 rounded-md"
                      />
                      <input
                        type="text"
                        placeholder="区"
                        value={editForm.district}
                        onChange={(e) => setEditForm({ ...editForm, district: e.target.value })}
                        className="px-3 py-2 border border-gray-300 rounded-md"
                      />
                    </div>
                  ) : (
                    <p className="mt-1 text-gray-900">
                      {[user?.province, user?.city, user?.district].filter(Boolean).join(' ') || '未设置'}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">性别</label>
                  {isEditing ? (
                    <select
                      value={editForm.gender}
                      onChange={(e) => setEditForm({ ...editForm, gender: Number(e.target.value) })}
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
                    >
                      <option value={0}>保密</option>
                      <option value={1}>男</option>
                      <option value={2}>女</option>
                    </select>
                  ) : (
                    <p className="mt-1 text-gray-900">
                      {user?.gender === 1 ? '男' : user?.gender === 2 ? '女' : '保密'}
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
