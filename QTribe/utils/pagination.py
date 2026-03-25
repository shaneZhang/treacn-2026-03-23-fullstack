"""
分页工具模块 - 封装Django分页功能，减少重复代码

使用方法:
    1. 在视图中使用 paginate_queryset 函数:
        from utils.pagination import paginate_queryset

        def my_view(request):
            queryset = MyModel.objects.all()
            context = paginate_queryset(request, queryset, per_page=10)
            return render(request, 'template.html', context)

    2. 在Haystack SearchView中使用 PaginationMixin:
        from utils.pagination import PaginationMixin

        class MySearchView(PaginationMixin, SearchView):
            results_per_page = 2
            # ... 其他代码
"""

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_page_list(paginator, current_page, max_display_pages=5):
    """
    获取用于前端遍历的页码列表

    Args:
        paginator: Paginator对象
        current_page: 当前页码
        max_display_pages: 最多显示的页码数量，默认为5

    Returns:
        range对象: 页码范围
    """
    num_pages = paginator.num_pages

    if num_pages <= max_display_pages:
        return paginator.page_range

    half_display = max_display_pages // 2

    if current_page - half_display <= 1:
        return range(1, max_display_pages + 1)
    elif current_page + half_display >= num_pages:
        return range(num_pages - max_display_pages + 1, num_pages + 1)
    else:
        return range(current_page - half_display + 1, current_page + half_display + 2)


def paginate_queryset(request, queryset, per_page=5, page_param='page_number', max_display_pages=5):
    """
    对查询集进行分页处理

    Args:
        request: HttpRequest对象
        queryset: 需要分页的查询集
        per_page: 每页显示数量，默认为5
        page_param: URL中页码参数的名称，默认为'page_number'
        max_display_pages: 页码导航栏最多显示的页码数，默认为5

    Returns:
        dict: 包含分页相关数据的字典，可直接用于模板渲染
        {
            'page_content': 当前页的内容(Page对象),
            'page_list': 页码列表,
            'current_page': 当前页码,
            'num_pages': 总页数
        }
    """
    page_number = int(request.GET.get(page_param, 1))

    paginator = Paginator(queryset, per_page)
    num_pages = paginator.num_pages

    page_list = get_page_list(paginator, page_number, max_display_pages)

    try:
        page_content = paginator.page(page_number)
    except PageNotAnInteger:
        page_content = paginator.page(1)
    except EmptyPage:
        page_content = paginator.page(num_pages)

    return {
        'page_content': page_content,
        'page_list': page_list,
        'current_page': page_content.number,
        'num_pages': num_pages
    }


def paginate_search_results(paginator, page, page_number, max_display_pages=5):
    """
    为Haystack搜索结果生成分页上下文

    Args:
        paginator: Paginator对象
        page: 当前页对象
        page_number: 当前页码
        max_display_pages: 页码导航栏最多显示的页码数，默认为5

    Returns:
        dict: 包含分页相关数据的字典
        {
            'page': 当前页对象,
            'page_list': 页码列表,
            'current_page': 当前页码,
            'num_pages': 总页数,
            'paginator': paginator对象
        }
    """
    num_pages = paginator.num_pages
    page_list = get_page_list(paginator, page_number, max_display_pages)

    return {
        'page': page,
        'page_list': page_list,
        'current_page': page.number,
        'num_pages': num_pages,
        'paginator': paginator
    }


class PaginationMixin:
    """
    Haystack SearchView 分页Mixin

    为继承自SearchView的搜索视图提供统一的分页功能

    使用方法:
        class MySearchView(PaginationMixin, SearchView):
            results_per_page = 2

            def get_context(self):
                context = super().get_context()
                # 添加其他上下文数据...
                return context
    """
    max_display_pages = 5
    page_param = 'page'

    def get_pagination_context(self, paginator, page):
        """
        获取分页上下文

        Returns:
            dict: 分页相关上下文
        """
        page_number = int(self.request.GET.get(self.page_param, 1))
        return paginate_search_results(
            paginator,
            page,
            page_number,
            self.max_display_pages
        )

    def get_context(self):
        """
        重写get_context方法，添加分页数据
        """
        (paginator, page) = self.build_page()
        context = self.get_pagination_context(paginator, page)
        context.update({
            "query": self.query,
            "form": self.form,
            "suggestion": None,
        })

        if (
            hasattr(self.results, "query")
            and self.results.query.backend.include_spelling
        ):
            context["suggestion"] = self.form.get_suggestion()

        return context
