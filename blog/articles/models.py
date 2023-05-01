from django.db import models
from django.utils import timezone
from users.models import User


# Create your models here.
class ArticleCategory(models.Model):
    """
    文章分类
    """
    # 分类标题
    title = models.CharField(max_length=100, blank=True)
    # 分类创建的时间
    created = models.DateTimeField(default=timezone.now)

    # admin站点显示，方便调试查看对象
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_category'  # 修改表名
        verbose_name = '类别管理'  # admin站点显示
        verbose_name_plural = verbose_name


class Article(models.Model):
    """
    作者
    文章图片
    标题
    分类
    标签
    摘要
    文章正文
    浏览量
    评论量
    文章创建时间
    文章修改时间
    """
    # 作者
    # 参数 on_delete：当User表中的数据删除后，文章信息也同步删除
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 文章图片
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    # 标题
    title = models.CharField(max_length=20, blank=True)
    # 分类
    category = models.ForeignKey(ArticleCategory, null=True, blank=True, on_delete=models.CASCADE, related_name='article')
    # 标签
    tags = models.CharField(max_length=20, blank=True)
    # 摘要
    summary = models.CharField(max_length=200, null=False, blank=False)
    # 文章正文
    content = models.TextField()
    # 浏览量
    total_views = models.PositiveIntegerField(default=0)
    # 评论量
    comments_count = models.PositiveIntegerField(default=0)
    # 文章创建时间
    created = models.DateTimeField(default=timezone.now)
    # 文章修改时间
    updated = models.DateTimeField(auto_now=True)

    # 修改表名，admin展示的配置信息
    class Meta:
        db_table = 'tb_article'
        ordering = ('-created',)
        verbose_name = '文章管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    评论用户
    评论文章
    评论时间
    评论内容
    """
    # 评论用户
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # 评论文章
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)

    # 评论时间
    created = models.DateTimeField(auto_now_add=True)

    # 评论内容
    content = models.TextField()

    def __str__(self):
        return self.article.title

    class Meta:
        db_table = 'tb_comment'
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name
