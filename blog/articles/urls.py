# 进行home自应用的视图路由
from django.urls import path

from articles.views import IndexView, DetailView

urlpatterns = [
    # path的第一个参数： 路由
    # path的第二个参数： 视图函数名
    path("articles/", IndexView.as_view(), name='index'),

    # 详情视图
    path("articles/detail/", DetailView.as_view(), name='detail'),
]