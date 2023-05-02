# 进行users自应用的视图路由
from django.urls import path

from users.views import RegisterView, ImageCodeView, SmsCodeView, LoginView, LogoutView, \
    ForgetPasswordView, UserCenterView, WriteBlogView, EmailCodeView

urlpatterns = [
    # path的第一个参数： 路由
    # path的第二个参数： 视图函数名
    path("register/", RegisterView.as_view(), name='register'),

    # 图片验证码路由
    path('imagecode/', ImageCodeView.as_view(), name='imagecode'),

    # 短信验证码路由
    path('smscode/', SmsCodeView.as_view(), name='smscode'),

    # 邮件验证码路由
    path('emailcode/', EmailCodeView.as_view(), name='emailcode'),

    # 登陆路由
    path('login/', LoginView.as_view(), name='login'),

    # 退出登陆路由
    path('logout/', LogoutView.as_view(), name='logout'),

    # 忘记密码路由
    path('forgetpassword/', ForgetPasswordView.as_view(), name='forgetpassword'),

    # 个人中心路由
    path('center/', UserCenterView.as_view(), name='center'),

    # 写文章路由
    path('writeblog/', WriteBlogView.as_view(), name='writeblog'),
]