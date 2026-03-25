#!/usr/bin/env python
"""测试代码语法"""

# 测试分页工具类的语法
class MockPaginator:
    def __init__(self, queryset, per_page):
        self.object_list = queryset
        self.per_page = per_page
        self.count = len(queryset)
        self.num_pages = (self.count + per_page - 1) // per_page
        self.page_range = range(1, self.num_pages + 1)
    
    def page(self, number):
        if number < 1:
            raise Exception("PageNotAnInteger")
        if number > self.num_pages:
            raise Exception("EmptyPage")
        start = (number - 1) * self.per_page
        end = start + self.per_page
        return MockPage(self.object_list[start:end], number)

class MockPage:
    def __init__(self, object_list, number):
        self.object_list = object_list
        self.number = number
    def __iter__(self):
        return iter(self.object_list)

class CustomPaginator:
    def __init__(self, queryset, per_page, page_number=1, show_pages=5):
        self.paginator = MockPaginator(queryset, per_page)
        self.page_number = int(page_number)
        self.show_pages = show_pages
        self.num_pages = self.paginator.num_pages

        try:
            self.page_content = self.paginator.page(self.page_number)
        except:  # PageNotAnInteger
            self.page_content = self.paginator.page(1)
            self.page_number = 1
        except:  # EmptyPage
            self.page_content = self.paginator.page(self.num_pages)
            self.page_number = self.num_pages

    def get_page_list(self):
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
        context = {
            'page_content': self.page_content,
            'page_list': self.get_page_list(),
            'current_page': self.page_content.number,
            'num_pages': self.num_pages,
        }

        if extra_context and isinstance(extra_context, dict):
            context.update(extra_context)

        return context

# 测试
test_data = [f'item_{i}' for i in range(100)]
paginator = CustomPaginator(test_data, per_page=10, page_number=3)
print(f"总页数: {paginator.num_pages}")
print(f"当前页: {paginator.page_content.number}")
print(f"页码列表: {list(paginator.get_page_list())}")
context = paginator.get_context_data()
print(f"上下文键: {context.keys()}")
print("语法测试通过!")
