from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_page_list(paginator, page_number):
    """
    获取页码列表，用于前端分页导航显示
    
    Args:
        paginator: Django Paginator 对象
        page_number: 当前页码
        
    Returns:
        range: 页码范围对象
    """
    num_pages = paginator.num_pages
    if num_pages > 5:
        if page_number - 2 <= 1:
            return range(1, 6)
        elif page_number + 2 >= num_pages:
            return range(num_pages - 4, num_pages + 1)
        else:
            return range(page_number - 1, page_number + 4)
    return paginator.page_range


def get_pagination_data(queryset, page_number, per_page=5):
    """
    获取分页数据，用于普通视图
    
    Args:
        queryset: Django QuerySet 对象
        page_number: 当前页码
        per_page: 每页显示数量，默认为5
        
    Returns:
        dict: 包含分页相关数据的字典
            - page_content: 当前页的内容对象
            - page_list: 页码列表
            - current_page: 当前页码
            - num_pages: 总页数
            - paginator: Paginator 对象
    """
    paginator = Paginator(queryset, per_page)
    num_pages = paginator.num_pages
    
    try:
        page_content = paginator.page(page_number)
    except PageNotAnInteger:
        page_content = paginator.page(1)
    except EmptyPage:
        page_content = paginator.page(num_pages)
    
    page_list = get_page_list(paginator, page_content.number)
    
    return {
        'page_content': page_content,
        'page_list': page_list,
        'current_page': page_content.number,
        'num_pages': num_pages,
        'paginator': paginator,
    }


def get_search_pagination_data(paginator, page):
    """
    获取搜索分页数据，用于 Haystack SearchView
    
    Args:
        paginator: Django Paginator 对象
        page: 当前页对象
        
    Returns:
        dict: 包含分页相关数据的字典
            - page_list: 页码列表
            - current_page: 当前页码
            - num_pages: 总页数
    """
    num_pages = paginator.num_pages
    page_list = get_page_list(paginator, page.number)
    
    return {
        'page_list': page_list,
        'current_page': page.number,
        'num_pages': num_pages,
    }


class PaginationMixin:
    """
    分页混入类，用于 Django View
    
    使用方法:
        class MyView(PaginationMixin, View):
            per_page = 5  # 可选，默认为5
            
            def get(self, request):
                queryset = MyModel.objects.all()
                page_number = int(request.GET.get('page_number', 1))
                pagination_data = self.get_pagination_data(queryset, page_number)
                return render(request, 'template.html', pagination_data)
    """
    per_page = 5
    
    def get_pagination_data(self, queryset, page_number=None, per_page=None):
        """
        获取分页数据
        
        Args:
            queryset: Django QuerySet 对象
            page_number: 当前页码，如果为None则从请求中获取
            per_page: 每页显示数量，如果为None则使用类属性 per_page
            
        Returns:
            dict: 分页数据字典
        """
        if page_number is None:
            page_number = int(self.request.GET.get('page_number', 1))
        if per_page is None:
            per_page = self.per_page
            
        return get_pagination_data(queryset, page_number, per_page)


class SearchPaginationMixin:
    """
    搜索分页混入类，用于 Haystack SearchView
    
    使用方法:
        class MySearchView(SearchPaginationMixin, SearchView):
            def get_context(self):
                (paginator, page) = self.build_page()
                context = super().get_context()
                pagination_data = self.get_search_pagination_data(paginator, page)
                context.update(pagination_data)
                return context
    """
    
    def get_search_pagination_data(self, paginator, page):
        """
        获取搜索分页数据
        
        Args:
            paginator: Django Paginator 对象
            page: 当前页对象
            
        Returns:
            dict: 分页数据字典
        """
        return get_search_pagination_data(paginator, page)
