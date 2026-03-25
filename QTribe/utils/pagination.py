from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class CustomPaginator:
    """
    自定义分页工具类，封装常用的分页逻辑
    """

    def __init__(self, queryset, per_page, page_number=1, show_pages=5):
        """
        初始化分页对象
        :param queryset: 要分页的数据查询集
        :param per_page: 每页显示数量
        :param page_number: 当前页码，默认为1
        :param show_pages: 前端显示的页码数量，默认为5
        """
        self.paginator = Paginator(queryset, per_page)
        self.page_number = int(page_number)
        self.show_pages = show_pages
        self.num_pages = self.paginator.num_pages

        try:
            self.page_content = self.paginator.page(self.page_number)
        except (PageNotAnInteger, ValueError, TypeError):
            self.page_content = self.paginator.page(1)
            self.page_number = 1
        except EmptyPage:
            self.page_content = self.paginator.page(self.num_pages)
            self.page_number = self.num_pages

    def get_page_list(self):
        """
        获取要显示的页码列表
        :return: 页码range对象
        """
        if self.num_pages > self.show_pages:
            if self.page_number - 2 <= 1:
                page_list = range(1, self.show_pages + 1)
            elif self.page_number + 2 >= self.num_pages:
                page_list = range(self.num_pages - 4, self.num_pages + 1)
            else:
                page_list = range(self.page_number - 1, self.page_number + 4)
        else:
            page_list = self.paginator.page_range

        return page_list

    def get_context_data(self, extra_context=None):
        """
        获取分页上下文数据，用于模板渲染
        :param extra_context: 额外需要添加到上下文的数据
        :return: 包含分页数据的上下文字典
        """
        context = {
            'page_content': self.page_content,
            'page_list': self.get_page_list(),
            'current_page': self.page_content.number,
            'num_pages': self.num_pages,
        }

        if extra_context and isinstance(extra_context, dict):
            context.update(extra_context)

        return context
