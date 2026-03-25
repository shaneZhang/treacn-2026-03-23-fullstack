#!/usr/bin/env python
"""测试分页工具类"""

import os
import sys

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QTribe.settings.dev')

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import django
    django.setup()
    print("Django setup OK")
except Exception as e:
    print(f"Django setup failed: {e}")
    sys.exit(1)

try:
    from QTribe.utils import CustomPaginator
    print("CustomPaginator import OK")
except Exception as e:
    print(f"Import CustomPaginator failed: {e}")
    sys.exit(1)

# 模拟一个queryset进行测试
class MockQuerySet:
    def __init__(self, items):
        self.items = items
        self._count = len(items)
    
    def count(self):
        return self._count
    
    def __getitem__(self, key):
        return self.items[key]
    
    def __len__(self):
        return self._count

# 测试数据
test_data = [f'item_{i}' for i in range(100)]
mock_qs = MockQuerySet(test_data)

# 测试分页功能
print("\n=== 测试分页功能 ===")
paginator = CustomPaginator(mock_qs, per_page=10, page_number=3)
print(f"总页数: {paginator.num_pages}")
print(f"当前页内容: {list(paginator.page_content)}")
print(f"页码列表: {list(paginator.get_page_list())}")

context = paginator.get_context_data()
print(f"\n上下文数据: {context.keys()}")

print("\n=== 所有测试通过! ===")
