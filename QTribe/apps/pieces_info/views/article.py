
#自己的文章列表页面
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.db.models import F
from pieces_info.models import ArticleModel,ImageModel

# #上传文章
from user.models import StarModel,CollectionModel

from QTribe.tasks import send_message


class PublishArticle(LoginRequiredMixin, View):
       def get(self,request):
            return render(request,'pieces/publish_article.html')
       def post(self,request):
           title=request.POST.get('title')
           content=request.POST.get('content')
           image=request.FILES.get('image')
           try:
               with transaction.atomic():#数据库绑定事物
                   article=ArticleModel.objects.create(title=title,content=content,default_img=image,user=request.user)
                   ImageModel.objects.create(image=image,user=request.user,article=article)
                   return JsonResponse({'code': 200})
           except:
               return JsonResponse({'code': 401})
#文章列表页面
class MyArticle(LoginRequiredMixin, View):
    def get(self,request):
        page_number = int(request.GET.get('page_number', 1))
        articles=ArticleModel.objects.filter(user=request.user)
        # 创建分页对象
        paginator = Paginator(articles, 5)
        num_pages = paginator.num_pages
        # 获取页码数列，用于前端遍历
        if paginator.num_pages > 5:
            if page_number - 2 <= 1:
                page_list = range(1, 6)
            elif page_number + 2 >= num_pages:
                page_list = range(num_pages - 4, num_pages + 1)
            else:
                page_list = range(page_number - 1, page_number + 4)

        else:
            page_list = paginator.page_range
        try:
            # 获取对应页数的全部视频
            page_content = paginator.page(page_number)
        except PageNotAnInteger:
            page_content = paginator.page(1)
        except EmptyPage:
            page_content = paginator.page(num_pages)
        return render(request, 'pieces/my_article.html', {'page_content': page_content,
                                                        'page_list': page_list,
                                                        'current_page': page_content.number,
                                                        'num_pages': num_pages})


#文章点赞量
class StarArticle(View):
    def get(self,request):
        a_id=int(request.GET.get('a_id'))
        current_page=int(request.GET.get('current_page'))
        q = request.GET.get('q')
        args = request.GET.get('args')  # 判断是从看点广场页面进入，还是从点赞列表页面进入
        article = ArticleModel.objects.get(id=a_id)
        try:
            is_star=StarModel.objects.get(user_id=request.user.id,article_id=a_id)
            flag=is_star.flag
        except:
            is_star=0
        if is_star and flag=='1':
            article.star_count-=1
            article.save()
            is_star.flag = '0'
            is_star.save()
            if args == 'mall':
                return redirect(f'/index/article_mall?page_number={current_page}')
            if args == 'star':  # 有可能用户取消点赞后，当页就没有内容，防止报错，加一个try
                try:
                    return redirect(f'/pieces/star_article_list?page_number={current_page}')
                except:
                    return redirect(f'/pieces/star_article_list?page_number={current_page - 1}')
            if args == 'collect':
                return redirect(f'/pieces/collect_article_list?page_number={current_page}')
            if args=='search':
                return redirect(f'/pieces/search_article/?page={current_page}&q={q}')
        else:
            article.star_count+=1
            article.save()
            data={'u_id':request.user.id,'type_2':'star_article','p_id':a_id}
            send_message.delay(data)
            if not is_star:
                StarModel.objects.create(user=request.user,article=article,flag='1')
            else:
                is_star.flag = '1'
                is_star.save()
            if args == 'mall':
                return redirect(f'/index/article_mall?page_number={current_page}')
            if args == 'collect':
                return redirect(f'/pieces/collect_article_list?page_number={current_page}')
            if args=='search':
                return redirect(f'/pieces/search_article/?page={current_page}&q={q}')

#文章收藏量
class CollectArticle(View):
    def get(self,request):
        a_id=int(request.GET.get('a_id'))
        current_page=int(request.GET.get('current_page'))
        q = request.GET.get('q')
        args = request.GET.get('args')  # 判断是从看点广场页面进入，还是从收藏列表页面进入
        article = ArticleModel.objects.get(id=a_id)
        try:
            is_collect=CollectionModel.objects.get(user_id=request.user.id,article_id=a_id)
            flag=is_collect.flag
        except:
            is_collect=0
        if is_collect and flag=='1':
            article.collection_count-=1
            article.save()
            is_collect.flag = '0'
            is_collect.save()
            if args == 'mall':
                return redirect(f'/index/article_mall?page_number={current_page}')
            if args == 'collect':
                try:
                    return redirect(f'/pieces/collect_article_list?page_number={current_page}')
                except:
                    return redirect(f'/pieces/collect_article_list?page_number={current_page - 1}')
            if args == 'star':
                return redirect(f'/pieces/star_article_list?page_number={current_page}')
            if args=='search':
                return redirect(f'/pieces/search_article/?page={current_page}&q={q}')
        else:
            article.collection_count+=1
            article.save()
            data={'u_id':request.user.id,'type_2':'collect_article','p_id':a_id}
            send_message.delay(data)
            if not is_collect:
                CollectionModel.objects.create(user=request.user,article=article,flag='1')
            else:
                is_collect.flag = '1'
                is_collect.save()
            if args == 'mall':
                return redirect(f'/index/article_mall?page_number={current_page}')
            if args == 'star':
                return redirect(f'/pieces/star_article_list?page_number={current_page}')
            if args=='search':
                return redirect(f'/pieces/search_article/?page={current_page}&q={q}')

#文章顶置
class TopArticle(View):
    def get(self,request):
        a_id=int(request.GET.get('a_id'))
        is_top=int(request.GET.get('is_top'))
        current_page = int(request.GET.get('current_page'))
        if is_top==1:
            ArticleModel.objects.filter(id=a_id).update(is_top=0)
            return redirect(f'/pieces/my_article/?page_number={current_page}')
        if is_top==0:
            ArticleModel.objects.filter(id=a_id).update(is_top=1)
            return redirect(f'/pieces/my_article/?page_number={current_page}')

#观看文章内容,增加浏览次数，并且打开文章内容页面
class DetailsArticle(View):
    def get(self,request):
        a_id=int(request.GET.get('a_id'))
        article=ArticleModel.objects.get(id=a_id)
        article.running_count+=1
        article.save()
        return render(request,'pieces/article_details.html',{'article':article})
#删除文章
class DeleteArticle(View):
    def get(self,request):
        a_id=int(request.GET.get('a_id'))
        current_page=int(request.GET.get('current_page'))
        ArticleModel.objects.filter(id=a_id).delete()
        try:
            return redirect(f'/pieces/my_article?page_number={current_page}')
        except:
            return redirect(f'/pieces/my_article?page_number={current_page-1}')

#点赞文章列表页面
class StarArticleList(LoginRequiredMixin, View):
    def get(self,request):
        page_number = int(request.GET.get('page_number', 1))
        star_ids=[]
        objs=request.user.starmodel_set.all()
        for obj in objs:
            if obj.flag=='1':
                star_ids.append(obj.article_id)
        articles=ArticleModel.objects.filter(id__in=star_ids)
        collection_ids=[]
        for article in articles:
            objs=request.user.collectionmodel_set.all()
            for obj in objs:
                if obj.article==article and obj.flag=='1':
                    collection_ids.append(article.id)
        # 创建分页对象
        paginator = Paginator(articles, 2)
        num_pages = paginator.num_pages
        # 获取页码数列，用于前端遍历
        if paginator.num_pages > 5:
            if page_number - 2 <= 1:
                page_list = range(1, 6)
            elif page_number + 2 >= num_pages:
                page_list = range(num_pages - 4, num_pages + 1)
            else:
                page_list = range(page_number - 1, page_number + 4)

        else:
            page_list = paginator.page_range
        try:
            # 获取对应页数的全部视频
            page_content = paginator.page(page_number)
        except PageNotAnInteger:
            page_content = paginator.page(1)
        except EmptyPage:
            page_content = paginator.page(num_pages)
        return render(request, 'pieces/star_article.html', {'page_content': page_content,
                                                        'page_list': page_list,
                                                        'current_page': page_content.number,
                                                        'num_pages': num_pages,
                                                         'collection_ids':collection_ids})
#收藏文章列表页面
class CollectArticleList(LoginRequiredMixin, View):
    def get(self,request):
        page_number = int(request.GET.get('page_number', 1))
        collection_ids=[]
        objs=request.user.collectionmodel_set.all()
        for obj in objs:
            if obj.flag=='1':
                collection_ids.append(obj.article_id)
        articles=ArticleModel.objects.filter(id__in=collection_ids)
        star_ids=[]
        for article in articles:
            objs=request.user.starmodel_set.all()
            for obj in objs:
                if obj.article==article and obj.flag=='1':
                    star_ids.append(article.id)
        # 创建分页对象
        paginator = Paginator(articles, 2)
        num_pages = paginator.num_pages
        # 获取页码数列，用于前端遍历
        if paginator.num_pages > 5:
            if page_number - 2 <= 1:
                page_list = range(1, 6)
            elif page_number + 2 >= num_pages:
                page_list = range(num_pages - 4, num_pages + 1)
            else:
                page_list = range(page_number - 1, page_number + 4)

        else:
            page_list = paginator.page_range
        try:
            # 获取对应页数的全部视频
            page_content = paginator.page(page_number)
        except PageNotAnInteger:
            page_content = paginator.page(1)
        except EmptyPage:
            page_content = paginator.page(num_pages)
        return render(request, 'pieces/collect_article.html', {'page_content': page_content,
                                                        'page_list': page_list,
                                                        'current_page': page_content.number,
                                                        'num_pages': num_pages,
                                                         'star_ids':star_ids})
class ArticleSearchView(View):
    template = 'search/article_search.html'
    results_per_page = 2

    def get(self, request):
        query = request.GET.get('q', '')
        page_number = int(request.GET.get('page', 1))
        
        if query:
            articles = ArticleModel.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) | 
                Q(user__username__icontains=query)
            )
        else:
            articles = ArticleModel.objects.all()
        
        paginator = Paginator(articles, self.results_per_page)
        num_pages = paginator.num_pages
        
        if num_pages > 5:
            if page_number - 2 <= 1:
                page_list = range(1, 6)
            elif page_number + 2 >= num_pages:
                page_list = range(num_pages - 4, num_pages + 1)
            else:
                page_list = range(page_number - 1, page_number + 4)
        else:
            page_list = paginator.page_range
        
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(num_pages)
        
        piece_list = []
        star_ids = []
        collection_ids = []
        
        for article in page:
            piece_list.append(article)
            if request.user.is_authenticated:
                stars_obj = article.starmodel_set.all()
                collections_obj = article.collectionmodel_set.all()
                for obj in stars_obj:
                    if obj.user == request.user and obj.flag == '1':
                        star_ids.append(obj.article_id)
                for obj in collections_obj:
                    if obj.user == request.user and obj.flag == '1':
                        collection_ids.append(obj.article_id)
        
        context = {
            "query": query,
            "page": page,
            "page_list": page_list,
            "piece_list": piece_list,
            'current_page': page.number,
            'num_pages': num_pages,
            "paginator": paginator,
            "q": query,
            "star_ids": star_ids,
            "collection_ids": collection_ids,
        }
        
        return render(request, self.template, context)
