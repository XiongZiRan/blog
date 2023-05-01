"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.articles, name='articles')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='articles')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# import logging
# logger = logging.getLogger('django')
#
# from django.http import HttpResponse
#
#
# def log(request):
#
#     logger.info('info')
#
#     return HttpResponse('test')


urlpatterns = [
    path("admin/", admin.site.urls),
    # include的参数中首先设置一个元组 urlconf_module, app_name
    # urlconf_module：子应用的路由
    # app_name：子应用的名字
    # namespace：命名工程
    path('', include(('users.urls', 'users'), namespace='users')),
    path('', include(('articles.urls', 'articles'), namespace='articles')),
    path('', include(('home.urls', 'home'), namespace='home')),
    path('', include(('chatgpt.urls', 'chatgpt'), namespace='chatgpt')),
]

# 图片访问的路由
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
