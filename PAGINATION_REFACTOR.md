# Django 分页查询重构说明

## 重构目的
减少重复代码，统一分页逻辑，提高代码可维护性。

## 重构内容

### 1. 创建分页工具类 `QTribe/utils/pagination.py`

封装了 Django 分页的常用逻辑：
- `CustomPaginator` 类：统一处理分页逻辑
- 自动处理 `PageNotAnInteger` 和 `EmptyPage` 异常
- 生成前端显示的页码列表（显示5个页码）
- 统一返回模板所需的上下文数据

使用方法：
```python
from QTribe.utils import CustomPaginator

def my_view(request):
    page_number = int(request.GET.get('page_number', 1))
    queryset = MyModel.objects.all()
    
    # 使用自定义分页工具（5条/页）
    paginator = CustomPaginator(queryset, 5, page_number)
    
    # 额外的上下文数据（可选）
    extra_context = {
        'custom_data': 'value',
    }
    
    # 获取包含分页数据的上下文
    context = paginator.get_context_data(extra_context)
    return render(request, 'template.html', context)
```

### 2. 已重构的视图文件

**index/views.py:**
- `VideoMall` - 视频广场（5条/页）
- `ArticleMall` - 文章广场（5条/页）
- `LifeMall` - 生活广场（5条/页）
- `OtherUser` - 其他用户列表（10条/页）

**pieces_info/views/article.py:**
- `MyArticle` - 我的文章列表（5条/页）
- `StarArticleList` - 点赞文章列表（2条/页）
- `CollectArticleList` - 收藏文章列表（2条/页）

**pieces_info/views/life.py:**
- `MyLife` - 我的生活列表（5条/页）
- `StarLifeList` - 点赞生活列表（2条/页）
- `CollectLifeList` - 收藏生活列表（2条/页）

**pieces_info/views/video.py:**
- `MyVideo` - 我的视频列表（5条/页）
- `StarVideoList` - 点赞视频列表（2条/页）
- `CollectVideoList` - 收藏视频列表（2条/页）

### 3. 上下文数据结构

分页工具统一返回以下模板变量：
```python
{
    'page_content': Page对象,       # 当前页的内容
    'page_list': range对象,         # 要显示的页码列表
    'current_page': int,            # 当前页码
    'num_pages': int,               # 总页数
    # + 自定义的额外上下文数据
}
```

## 代码优化效果

- 消除了重复的分页逻辑代码（约200行重复代码）
- 统一了分页行为和异常处理
- 简化了视图函数的编写
- 便于后续统一修改分页相关逻辑
