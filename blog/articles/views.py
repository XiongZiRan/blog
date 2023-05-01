from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect, reverse
from django.views import View
from articles.models import ArticleCategory, Article, Comment
from django.http.response import HttpResponseNotFound


# Create your views here.
class IndexView(View):

    def get(self, request):
        """
        1.获取所有分类信息
        2.接受用户点击的分类id
        3.根据分类id进行查询
        4.获取分页参数
        5.根据分类信息查询文章数据
        6.创建分页器
        7.进行分页处理
        8.组织数据传递给template
        """
        # 1.获取所有分类信息
        categories = ArticleCategory.objects.all()

        # 2.接受用户点击的分类id
        category_id = request.GET.get('cat_id', 1)

        # 3.根据分类id进行查询
        try:
            category = ArticleCategory.objects.get(id=category_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('没有此分类')

        # 4.获取分页参数
        page_num = request.GET.get('page_num', 1)
        page_size = request.GET.get('page_size', 10)

        # 5.根据分类信息查询文章数据
        articles = Article.objects.filter(category=category)

        # 6.创建分页器
        paginator = Paginator(articles, per_page=page_size)

        # 7.进行分页处理
        try:
            page_articles = paginator.page(page_num)
        except EmptyPage:
            return HttpResponseNotFound('Empty Page')

        # 总页数参数
        total_page = paginator.num_pages

        # 8.组织数据传递给template
        context = {
            'categories': categories,
            'category': category,
            'articles': page_articles,
            'page_size': page_size,
            'page_num': page_num,
            'total_page': total_page
        }

        return render(request, 'articles_index.html', context=context)


class DetailView(View):

    def get(self, request):
        """
        1.接受文章id
        2.根据id查询
        3.查询分类数据
        4.组织template数据
        """
        # 1.接受文章id
        id = request.GET.get('id')

        # 2.根据id查询
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return render(request, '404.html')
        else:
            article.total_views += 1
            article.save()

        # 3.查询分类数据
        categories = ArticleCategory.objects.all()

        # 查询浏览量前十的文章数据
        hot_articles = Article.objects.order_by('-total_views')[:9]


        # 获取分页参数
        page_num = request.GET.get('page_num', 1)
        page_size = request.GET.get('page_size', 10)
        # 查询评论信息
        comments = Comment.objects.filter(article_id=article.id).order_by('-created')
        total_comment = comments.count()
        # 创建分页器
        paginator = Paginator(comments, per_page=page_size)
        # 进行分页处理
        try:
            page_comments = paginator.page(page_num)
        except EmptyPage:
            return HttpResponseNotFound('Empty Page')

        # 总页数参数
        total_page = paginator.num_pages

        # 4.组织template数据
        context = {
            'article': article,
            'categories': categories,
            'category': article.category,
            'hot_articles': hot_articles,
            'comments': page_comments,
            'total_page': total_page,
            'total_comment': total_comment,
            'page_num': page_num,
            'page_size': page_size
        }

        return render(request, 'articles_detail.html', context=context)

    def post(self, request):
        """
        1.接受用户信息
        2.判断用户是否登陆
        3.登陆用户则可以接受form数据
            3.1 接受评论数据
            3.2 验证文章是否存在
            3.3 保存评论数据
            3.4 修改文章的评论数量
        4.未登录用户跳转到登陆页面
        """
        # 1.接受用户信息
        user = request.user

        # 2.判断用户是否登陆
        if user and user.is_authenticated:
            # 3.登陆用户则可以接受form数据
            #     3.1 接受评论数据
            id = request.POST.get('id')
            content = request.POST.get('content')

            #     3.2 验证文章是否存在
            try:
                article = Article.objects.get(id=id)
            except Article.DoesNotExist:
                return HttpResponseNotFound('评论文章不存在')

            #     3.3 保存评论数据
            Comment.objects.create(
                content=content,
                user=user,
                article=article
            )

            #     3.4 修改文章的评论数量
            article.comments_count += 1
            article.save()

            # 刷新当前页面
            path = reverse('articles:detail')+'?id={}'.format(article.id)
            return redirect(path)
        else:
            # 4.未登录用户跳转到登陆页面
            return redirect(reverse('users:login'))
