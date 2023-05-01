# 进行home自应用的视图路由
from django.urls import path

from chatgpt.views import IndexView
urlpatterns = [
    # path的第一个参数： 路由
    # path的第二个参数： 视图函数名
    path("chatgpt/", IndexView.as_view(), name='index'),
]