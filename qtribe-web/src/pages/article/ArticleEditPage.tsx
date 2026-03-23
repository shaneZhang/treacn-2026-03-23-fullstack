import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { toast } from 'sonner';
import { useMutation, useQuery } from 'react-query';
import { articleApi } from '@/api';

const articleSchema = z.object({
  title: z.string().min(1, '请输入标题').max(100, '标题最多100个字符'),
  content: z.string().min(1, '请输入内容'),
});

type ArticleFormData = z.infer<typeof articleSchema>;

const ArticleEditPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [imageFile, setImageFile] = React.useState<File | null>(null);
  const isEdit = !!id;

  const { data } = useQuery(
    ['article', id],
    () => articleApi.getDetail(Number(id)),
    { enabled: isEdit }
  );

  const article = data?.data?.data;

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<ArticleFormData>({
    resolver: zodResolver(articleSchema),
    defaultValues: {
      title: article?.title || '',
      content: article?.content || '',
    },
  });

  React.useEffect(() => {
    if (article) {
      setValue('title', article.title);
      setValue('content', article.content);
    }
  }, [article, setValue]);

  const createMutation = useMutation(
    (data: ArticleFormData) => articleApi.create({ ...data, default_img: imageFile || undefined }),
    {
      onSuccess: (response) => {
        toast.success('发布成功');
        navigate(`/articles/${response.data.data?.id}`);
      },
    }
  );

  const updateMutation = useMutation(
    (data: ArticleFormData) => articleApi.update(Number(id), { ...data }),
    {
      onSuccess: () => {
        toast.success('更新成功');
        navigate(`/articles/${id}`);
      },
    }
  );

  const onSubmit = (data: ArticleFormData) => {
    if (isEdit) {
      updateMutation.mutate(data);
    } else {
      createMutation.mutate(data);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">
        {isEdit ? '编辑文章' : '发布文章'}
      </h1>

      <form onSubmit={handleSubmit(onSubmit)} className="bg-white rounded-lg shadow-sm p-8">
        <div className="space-y-6">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
              标题
            </label>
            <input
              {...register('title')}
              type="text"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              placeholder="请输入文章标题"
            />
            {errors.title && (
              <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
            )}
          </div>

          <div>
            <label htmlFor="default_img" className="block text-sm font-medium text-gray-700 mb-2">
              封面图片
            </label>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setImageFile(e.target.files?.[0] || null)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            />
            {article?.default_img_url && !imageFile && (
              <img
                src={article.default_img_url}
                alt="当前封面"
                className="mt-2 w-48 h-32 object-cover rounded"
              />
            )}
          </div>

          <div>
            <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
              内容
            </label>
            <textarea
              {...register('content')}
              rows={15}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 resize-none"
              placeholder="请输入文章内容（支持HTML）"
            />
            {errors.content && (
              <p className="mt-1 text-sm text-red-600">{errors.content.message}</p>
            )}
          </div>

          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              取消
            </button>
            <button
              type="submit"
              disabled={createMutation.isLoading || updateMutation.isLoading}
              className="px-4 py-2 bg-primary-600 text-white rounded-md text-sm font-medium hover:bg-primary-700 disabled:opacity-50"
            >
              {createMutation.isLoading || updateMutation.isLoading
                ? '提交中...'
                : isEdit
                ? '更新'
                : '发布'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default ArticleEditPage;
