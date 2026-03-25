from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.db.models import F
from haystack.query import EmptySearchQuerySet
from haystack.views import SearchView
from pieces_info.models import ArticleModel, ImageModel

from user.models import StarModel, CollectionModel

from QTribe.tasks import send_message
from QTribe.utils.pagination import get_pagination_data, get_search_pagination_data


class PublishArticle(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'pieces/publish_article.html')

    def post(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        try:
            with transaction.atomic():
                article = ArticleModel.objects.create(title=title, content=content, default_img=image, user=request.user)
                ImageModel.objects.create(image=image, user=request.user, article=article)
                return JsonResponse({'code': 200})
        except:
            return JsonResponse({'code': 401})


class MyArticle(LoginRequiredMixin, View):
    def get(self, request):
        page_number = int(request.GET.get('page_number', 1))
        articles = ArticleModel.objects.filter(user=request.user)
        pagination_data = get_pagination_data(articles, page_number, per_page=5)
        return render(request, 'pieces/my_article.html', pagination_data)


class StarArticle(View):
    def get(self, request):
        a_id = int(request.GET.get('a_id'))
        current_page = int(request.GET.get('current_page'))
        q = request.GET.get('q')
        args = request.GET.get('args')
        article = ArticleModel.objects.get(id=a_id)
        try:
            is_star = StarModel.objects.get(user_id=request.user.id, article_id=a_id)
            flag = is_star.flag
        except:
            is_star = 0
        if is_star and flag == '1':
            article.star_count -= 1
            article.save()
            is_star.flag = '0'
            is_star.save()
            if args == 'mall':
                return redirect(f'/index/article_mall?page_number={current_page}')
            if args == 'star':
                try:
                    return redirect(f'/pieces/star_article_list?page_number={current_page}')
                except:
                    return redirect(f'/pieces/star_article_list?page_number={current_page - 1}')
            if args == 'collect':
                return redirect(f'/pieces/collect_article_list?page_number={current_page}')
            if args == 'search':
                return redirect(f'/pieces/search_article/?page={current_page}&q={q}')
        else:
            article.star_count += 1
            article.save()
            data = {'u_id': request.user.id, 'type_2': 'star_article', 'p_id': a_id}
            send_message.delay(data)
            if not is_star:
                StarModel.objects.create(user=request.user, article=article, flag='1')
            else:
                is_star.flag = '1'
                is_star.save()
            if args == 'mall':
                return redirect(f'/index/article_mall?page_number={current_page}')
            if args == 'collect':
                return redirect(f'/pieces/collect_article_list?page_number={current_page}')
            if args == 'search':
                return redirect(f'/pieces/search_article/?page={current_page}&q={q}')


class CollectArticle(View):
    def get(self, request):
        a_id = int(request.GET.get('a_id'))
        current_page = int(request.GET.get('current_page'))
        q = request.GET.get('q')
        args = request.GET.get('args')
        article = ArticleModel.objects.get(id=a_id)
        try:
            is_collect = CollectionModel.objects.get(user_id=request.user.id, article_id=a_id)
            flag = is_collect.flag
        except:
            is_collect = 0
        if is_collect and flag == '1':
            article.collection_count -= 1
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
            if args == 'search':
                return redirect(f'/pieces/search_article/?page={current_page}&q={q}')
        else:
            article.collection_count += 1
            article.save()
            data = {'u_id': request.user.id, 'type_2': 'collect_article', 'p_id': a_id}
            send_message.delay(data)
            if not is_collect:
                CollectionModel.objects.create(user=request.user, article=article, flag='1')
            else:
                is_collect.flag = '1'
                is_collect.save()
            if args == 'mall':
                return redirect(f'/index/article_mall?page_number={current_page}')
            if args == 'star':
                return redirect(f'/pieces/star_article_list?page_number={current_page}')
            if args == 'search':
                return redirect(f'/pieces/search_article/?page={current_page}&q={q}')


class TopArticle(View):
    def get(self, request):
        a_id = int(request.GET.get('a_id'))
        is_top = int(request.GET.get('is_top'))
        current_page = int(request.GET.get('current_page'))
        if is_top == 1:
            ArticleModel.objects.filter(id=a_id).update(is_top=0)
            return redirect(f'/pieces/my_article/?page_number={current_page}')
        if is_top == 0:
            ArticleModel.objects.filter(id=a_id).update(is_top=1)
            return redirect(f'/pieces/my_article/?page_number={current_page}')


class DetailsArticle(View):
    def get(self, request):
        a_id = int(request.GET.get('a_id'))
        article = ArticleModel.objects.get(id=a_id)
        article.running_count += 1
        article.save()
        return render(request, 'pieces/article_details.html', {'article': article})


class DeleteArticle(View):
    def get(self, request):
        a_id = int(request.GET.get('a_id'))
        current_page = int(request.GET.get('current_page'))
        ArticleModel.objects.filter(id=a_id).delete()
        try:
            return redirect(f'/pieces/my_article?page_number={current_page}')
        except:
            return redirect(f'/pieces/my_article?page_number={current_page - 1}')


class StarArticleList(LoginRequiredMixin, View):
    def get(self, request):
        page_number = int(request.GET.get('page_number', 1))
        star_ids = []
        objs = request.user.starmodel_set.all()
        for obj in objs:
            if obj.flag == '1':
                star_ids.append(obj.article_id)
        articles = ArticleModel.objects.filter(id__in=star_ids)
        collection_ids = []
        for article in articles:
            objs = request.user.collectionmodel_set.all()
            for obj in objs:
                if obj.article == article and obj.flag == '1':
                    collection_ids.append(article.id)
        pagination_data = get_pagination_data(articles, page_number, per_page=2)
        pagination_data['collection_ids'] = collection_ids
        return render(request, 'pieces/star_article.html', pagination_data)


class CollectArticleList(LoginRequiredMixin, View):
    def get(self, request):
        page_number = int(request.GET.get('page_number', 1))
        collection_ids = []
        objs = request.user.collectionmodel_set.all()
        for obj in objs:
            if obj.flag == '1':
                collection_ids.append(obj.article_id)
        articles = ArticleModel.objects.filter(id__in=collection_ids)
        star_ids = []
        for article in articles:
            objs = request.user.starmodel_set.all()
            for obj in objs:
                if obj.article == article and obj.flag == '1':
                    star_ids.append(article.id)
        pagination_data = get_pagination_data(articles, page_number, per_page=2)
        pagination_data['star_ids'] = star_ids
        return render(request, 'pieces/collect_article.html', pagination_data)


class ArticleSearchView(SearchView):

    template = 'search/article_search.html'
    results = EmptySearchQuerySet()
    results_per_page = 2

    def __init__(self):
        from haystack.query import SearchQuerySet
        sqs = SearchQuerySet().using('default')
        super(ArticleSearchView, self).__init__(searchqueryset=sqs)

    def get_query(self):
        queryset = super(ArticleSearchView, self).get_query()
        return queryset

    def get_results(self):
        result = []
        for obj in self.form.search():
            if obj.model_name == 'articlemodel':
                result.append(obj)
        return result

    def get_context(self):
        (paginator, page) = self.build_page()
        pagination_data = get_search_pagination_data(paginator, page)
        piece_list = []
        star_ids = []
        collection_ids = []
        for article in page:
            piece_list.append(article.object)
            if self.request.user.is_authenticated:
                stars_obj = article.object.starmodel_set.all()
                collections_obj = article.object.collectionmodel_set.all()
                for obj in stars_obj:
                    if obj.user == self.request.user and obj.flag == '1':
                        star_ids.append(obj.article_id)
                for obj in collections_obj:
                    if obj.user == self.request.user and obj.flag == '1':
                        collection_ids.append(obj.article_id)
        context = {
            "query": self.query,
            "form": self.form,
            "page": page,
            "piece_list": piece_list,
            "paginator": paginator,
            "q": self.get_query(),
            "suggestion": None,
            "star_ids": star_ids,
            "collection_ids": collection_ids,
        }
        context.update(pagination_data)

        if (
            hasattr(self.results, "query")
            and self.results.query.backend.include_spelling
        ):
            context["suggestion"] = self.form.get_suggestion()
        return context
