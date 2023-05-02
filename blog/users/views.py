import re

from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from articles.models import ArticleCategory, Article
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from utils.response_code import RETCODE
import logging
logger = logging.getLogger('django')
from random import randint
from libs.yuntongxun.sms import CCP
from users.models import User
from django.db import DatabaseError
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# 短信注册视图
# class RegisterView(View):
#
#     def get(self, request):
#
#         return render(request, 'users_register.html')
#
#     def post(self, request):
#         """
#         1.接收数据
#         2.验证数据
#             2.1 验证参数是否齐全
#             2.2 验证手机号格式是否正确
#             2.3 验证密码是否正确
#             2.4 密码和确认密码一致
#             2.5 短信验证码是否和redis中一致
#         3.保存注册信息
#         4.返回响应跳转到指定页面
#         """
#         # 1.接收数据
#         mobile = request.POST.get('mobile')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
#         smscode = request.POST.get('sms_code')
#         # 2.验证数据
#         #     2.1 验证参数是否齐全
#         if not all([mobile, password, password2, smscode]):
#             return HttpResponseBadRequest('缺少必要参数')
#         #     2.2 验证手机号格式是否正确
#         if not re.match(r'^1[3-9]\d{9}$', mobile):
#             return HttpResponseBadRequest('手机号不符合规则')
#         #     2.3 验证密码是否正确
#         if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
#             return HttpResponseBadRequest('请输入8-20位密码，密码是数字+字母')
#         #     2.4 密码和确认密码一致
#         if password != password2:
#             return HttpResponseBadRequest('两次密码不一致')
#         #     2.5 短信验证码是否和redis中一致
#         redis_conn = get_redis_connection('default')
#         redis_sms_code = redis_conn.get('smscode:%s'%mobile)
#         if redis_sms_code is None:
#             return HttpResponseBadRequest('短信验证码已过期')
#         # print('smscode='+smscode)
#         # print('redis_sms_code='+redis_sms_code.decode())
#         if smscode != redis_sms_code.decode():
#             return HttpResponseBadRequest('短信验证码错误')
#         # 3.保存注册信息
#         # create_user 可以使用系统的方法对密码加密
#         try:
#             user = User.objects.create_user(username=mobile,
#                                             mobile=mobile,
#                                             password=password)
#         except DatabaseError as e:
#             logger.error(e)
#             return HttpResponseBadRequest('注册失败')
#
#         # 登陆状态保持
#         from django.contrib.auth import login
#         login(request, user)
#
#         # 4.返回响应跳转到指定页面
#         # redirect 重定向
#         # reverse 通过namespace:name获取视图对应的路由
#         response = redirect(reverse('home:index'))
#
#         # 设置cookie信息，方便首页中用户信息展示的判断
#         response.set_cookie('is_login', True)
#         response.set_cookie('username', user.username, max_age=7*24*3600)
#
#         return response

# 邮箱注册视图
class RegisterView(View):

    def get(self, request):

        return render(request, 'users_register.html')

    def post(self, request):
        """
        1.接收数据
        2.验证数据
            2.1 验证参数是否齐全
            2.2 验证手机号格式是否正确
            2.3 验证密码是否正确
            2.4 密码和确认密码一致
            2.5 短信验证码是否和redis中一致
        3.保存注册信息
        4.返回响应跳转到指定页面
        """
        # 1.接收数据
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        emailcode = request.POST.get('email_code')
        # 2.验证数据
        #     2.1 验证参数是否齐全
        if not all([mobile, password, password2, emailcode]):
            return HttpResponseBadRequest('缺少必要参数')
        #     2.2 验证手机号格式是否正确
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号不符合规则')
        #     2.3 验证邮箱格式是否正确
        if not re.match(r'^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$', email):
            return HttpResponseBadRequest('邮箱不符合规则')
        #     2.4 验证密码是否正确
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseBadRequest('请输入8-20位密码，密码是数字+字母')
        #     2.5 密码和确认密码一致
        if password != password2:
            return HttpResponseBadRequest('两次密码不一致')
        #     2.6 短信验证码是否和redis中一致
        redis_conn = get_redis_connection('default')
        redis_email_code = redis_conn.get('emailcode:%s'%mobile)
        if redis_email_code is None:
            return HttpResponseBadRequest('短信验证码已过期')
        # print('smscode='+smscode)
        # print('redis_sms_code='+redis_sms_code.decode())
        if emailcode != redis_email_code.decode():
            return HttpResponseBadRequest('邮件验证码错误')
        # 3.保存注册信息
        # create_user 可以使用系统的方法对密码加密
        try:
            user = User.objects.create_user(username=mobile,
                                            mobile=mobile,
                                            email=email,
                                            password=password)
        except DatabaseError as e:
            logger.error(e)
            return HttpResponseBadRequest('注册失败')

        # 登陆状态保持
        from django.contrib.auth import login
        login(request, user)

        # 4.返回响应跳转到指定页面
        # redirect 重定向
        # reverse 通过namespace:name获取视图对应的路由
        response = redirect(reverse('home:index'))

        # 设置cookie信息，方便首页中用户信息展示的判断
        response.set_cookie('is_login', True)
        response.set_cookie('username', user.username, max_age=7*24*3600)

        return response


class ImageCodeView(View):

    def get(self, request):

        """
        1. 接收前端传递过来的uuid
        2. 判断uuid是否获取到
        3. 通过调用captcha来生成图片验证码（图片二进制和图片内容）
        4. 将图片内容保存到redis中，uuid作为key，图片内容作为value，同时设置时效
        5. 返回图片二进制
        """

        uuid = request.GET.get('uuid')

        if uuid is None:
            return HttpResponseBadRequest('没有传递uuid')

        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('default')
        redis_conn.setex('imagecode:%s'%uuid, 300, text)

        return HttpResponse(image, content_type='image/jepg')


class EmailCodeView(View):

    def get(self, request):
        """
        1.接收参数
        2.参数验证
            2.1 验证参数是否齐全
            2.2 验证图片验证码
                2.2.1 链接redis，获取redis中的图片验证码
                2.2.2 判断图片验证码是否存在
                2.2.3 如果未过期，获取然后删除已有图片验证码
                2.2.4 比对图片验证码
        3.生成短信验证码
        4.保存验证码到redis
        5.发送短信
        6.返回响应
        """
        # 1.接收参数
        mobile = request.GET.get('mobile')
        email = request.GET.get('email')
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        # 2.参数验证
        #     2.1 验证参数是否齐全
        if not all([mobile, email, image_code, uuid]):
            return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必要的参数'})
        #     2.2 验证图片验证码
        #         2.2.1 链接redis，获取redis中的图片验证码
        redis_conn = get_redis_connection('default')
        redis_image_code = redis_conn.get('imagecode:%s' % uuid)
        #         2.2.2 判断图片验证码是否存在
        if redis_image_code is None:
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图片验证码已过期'})
        #         2.2.3 如果未过期，获取然后删除已有图片验证码
        try:
            redis_conn.delete('imagecode:%s' % uuid)
        except Exception as e:
            logger.error(e)
        #         2.2.4 比对图片验证码，注意大小写，redis数据是bytes类型
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图片验证码错误'})

        # 3.生成短信验证码，为了比对方便，将短信验证码记录到日志中
        email_code = '%06d' % randint(0, 999999)
        logger.info(email_code)
        # 4.保存验证码到redis
        redis_conn.setex('emailcode:%s' % mobile, 300, email_code)
        # 5.发送短信
        send_status = send_mail(
            # 发送邮件的主题
            subject='NaaturrBee注册邮件',
            # 发送的内容
            message="您的验证码是："+email_code+"，验证码5分钟内有效。",
            # 发送邮件的邮箱
            from_email=settings.EMAIL_HOST_USER,
            # 把这条邮件信息发送给xxxx@qq.com的邮箱
            recipient_list=[email]
        )
        if send_status:
            return JsonResponse({'code': RETCODE.OK, 'errmsg': '邮件发送成功'})
        else:
            return HttpResponseBadRequest('测试邮件为发送成功，请检查邮箱是否正确')

        # CCP().send_template_sms('18806128897', [email_code, 5], 1)
        # # 6.返回响应
        # return JsonResponse({'code': RETCODE.OK, 'errmsg': '短信发送成功'})
        #
        # pass


class SmsCodeView(View):

    def get(self, request):
        """
        1.接收参数
        2.参数验证
            2.1 验证参数是否齐全
            2.2 验证图片验证码
                2.2.1 链接redis，获取redis中的图片验证码
                2.2.2 判断图片验证码是否存在
                2.2.3 如果未过期，获取然后删除已有图片验证码
                2.2.4 比对图片验证码
        3.生成短信验证码
        4.保存验证码到redis
        5.发送短信
        6.返回响应
        """
        # 1.接收参数
        mobile = request.GET.get('mobile')
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        # 2.参数验证
        #     2.1 验证参数是否齐全
        if not all([mobile, image_code, uuid]):
            return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必要的参数'})
        #     2.2 验证图片验证码
        #         2.2.1 链接redis，获取redis中的图片验证码
        redis_conn = get_redis_connection('default')
        redis_image_code = redis_conn.get('imagecode:%s'%uuid)
        #         2.2.2 判断图片验证码是否存在
        if redis_image_code is None:
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图片验证码已过期'})
        #         2.2.3 如果未过期，获取然后删除已有图片验证码
        try:
            redis_conn.delete('imagecode:%s'%uuid)
        except Exception as e:
            logger.error(e)
        #         2.2.4 比对图片验证码，注意大小写，redis数据是bytes类型
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图片验证码错误'})
        # 3.生成短信验证码，为了比对方便，将短信验证码记录到日志中
        sms_code = '%04d' % randint(0, 9999)
        logger.info(sms_code)
        # 4.保存验证码到redis
        redis_conn.setex('smscode:%s' % mobile, 300, sms_code)
        # 5.发送短信
        CCP().send_template_sms('18806128897', [sms_code, 5], 1)
        # 6.返回响应
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '短信发送成功'})


class LoginView(View):

    def get(self, request):

        return render(request, 'users_login.html')

    def post(self, request):
        """
        1.接受参数
        2.参数验证
            2.1 验证手机号
            2.2 验证密码
        3.用户认证登陆
        4.状态保持
        5.判断用户选择的是否保持登录
        6.为了首页显示，设置cookie信息
        7.返回响应
        """
        # 1.接受参数
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        # 2.参数验证
        #     2.1 验证手机号
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号不符合规则')
        #     2.2 验证密码
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return HttpResponseBadRequest('密码不符合规则')
        # 3.用户认证登陆
        from django.contrib.auth import authenticate
        # 默认的认证方法是针对username字段进行用户名的判断
        # 当前的判断信息是手机号，需要修改认证字段
        user = authenticate(mobile=mobile, password=password)
        if user is None:
            return HttpResponseBadRequest('用户名或密码错误')
        # 4.状态保持
        from django.contrib.auth import login
        login(request, user)
        # 5.判断用户选择的是否保持登录
        # 6.为了首页显示，
        next_page = request.GET.get('next')
        if next_page:
            response = redirect(next_page)
        else:
            response = redirect(reverse('home:index'))

        # avatar_url = user.avatar.url if user.avatar else None
        # print(avatar_url)
        # print(type(avatar_url))

        if remember != 'on':  #没有记住用户信息
            #浏览器关闭之后
            request.session.set_expiry(0)
            response.set_cookie('is_login', True)
            response.set_cookie('username', user.username, max_age=14*24*3600)
            # response.set_cookie('avatar', avatar_url, max_age=14*24*3600)
        else:                 # 记住用户信息
            # 默认是记住 2周
            request.session.set_expiry(None)
            response.set_cookie('is_login', True, max_age=14*24*3600)
            response.set_cookie('username', user.username, max_age=14*24*3600)
            # response.set_cookie('avatar', avatar_url, max_age=14*24*3600)
        # 7.返回响应
        return response


class LogoutView(View):

    def get(self, request):
        """
        1.清除session
        2.部分清楚cookie
        3.跳转首页
        """
        # 1.清除session
        logout(request)
        # 2.部分清楚cookie
        response = redirect(reverse('home:index'))
        response.delete_cookie('is_login')
        # response.delete_cookie('username')
        # 3.跳转首页
        return response


class ForgetPasswordView(View):

    def get(self, request):

        return render(request, 'users_forget_password.html')

    def post(self, request):
        """
        1.接收数据
        2.数据验证
            2.1 判断参数是否齐全
            2.2 判断手机号是否符合规则
            2.3 判断密码是否符合规则
            2.4 判断确认密码和密码是否一致
            2.5 判断短信验证码是否正确
        3.根据手机号查询用户信息
        4.如果查询出手机号信息-->密码修改
        5.如果没有手机号信息-->创建新用户
        6.跳转到登陆页面
        7.返回响应
        """
        # 1.接收数据
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        emailcode = request.POST.get('email_code')
        # 2.数据验证
        #     2.1 判断参数是否齐全
        if not all([mobile, email, password, password2, emailcode]):
            return HttpResponseBadRequest('参数不全')
        #     2.2 判断手机号是否符合规则
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号不符合规则')
        #     2.3 验证邮箱格式是否正确
        if not re.match(r'^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$', email):
            return HttpResponseBadRequest('邮箱不符合规则')
        #     2.3 判断密码是否符合规则
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return HttpResponseBadRequest('密码不符合规则')
        #     2.4 判断确认密码和密码是否一致
        if password != password2:
            return HttpResponseBadRequest('两次密码不一致')
        #     2.5 判断短信验证码是否正确
        redis_conn = get_redis_connection('default')
        redis_email_code = redis_conn.get('emailcode:%s'%mobile)
        if redis_email_code is None:
            return HttpResponseBadRequest('邮件验证码已过期')
        if emailcode != redis_email_code.decode():
            return HttpResponseBadRequest('邮件验证码错误')
        # 3.根据手机号查询用户信息
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 5.如果没有手机号信息-->创建新用户
            try:
                User.objects.create_user(username=mobile,
                                         mobile=mobile,
                                         email=email,
                                         password=password)
            except Exception:
                return HttpResponseBadRequest('修改失败，请稍后再试')
        else:
            # 4.如果查询出手机号信息-->密码修改
                user.set_password(password)
                # 保存用户信息
                user.save()

        # 6.跳转到登陆页面
        response = redirect(reverse('users:login'))
        # 7.返回响应
        return response
# class ForgetPasswordView(View):
#
#     def get(self, request):
#
#         return render(request, 'users_forget_password.html')
#
#     def post(self, request):
#         """
#         1.接收数据
#         2.数据验证
#             2.1 判断参数是否齐全
#             2.2 判断手机号是否符合规则
#             2.3 判断密码是否符合规则
#             2.4 判断确认密码和密码是否一致
#             2.5 判断短信验证码是否正确
#         3.根据手机号查询用户信息
#         4.如果查询出手机号信息-->密码修改
#         5.如果没有手机号信息-->创建新用户
#         6.跳转到登陆页面
#         7.返回响应
#         """
#         # 1.接收数据
#         mobile = request.POST.get('mobile')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
#         smscode = request.POST.get('sms_code')
#         # 2.数据验证
#         #     2.1 判断参数是否齐全
#         if not all([mobile, password, password2, smscode]):
#             return HttpResponseBadRequest('参数不全')
#         #     2.2 判断手机号是否符合规则
#         if not re.match(r'^1[3-9]\d{9}$', mobile):
#             return HttpResponseBadRequest('手机号不符合规则')
#         #     2.3 判断密码是否符合规则
#         if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
#             return HttpResponseBadRequest('密码不符合规则')
#         #     2.4 判断确认密码和密码是否一致
#         if password != password2:
#             return HttpResponseBadRequest('两次密码不一致')
#         #     2.5 判断短信验证码是否正确
#         redis_conn = get_redis_connection('default')
#         redis_sms_code = redis_conn.get('smscode:%s'%mobile)
#         if redis_sms_code is None:
#             return HttpResponseBadRequest('短信验证码已过期')
#         if smscode != redis_sms_code.decode():
#             return HttpResponseBadRequest('短信验证码错误')
#         # 3.根据手机号查询用户信息
#         try:
#             user = User.objects.get(mobile=mobile)
#         except User.DoesNotExist:
#             # 5.如果没有手机号信息-->创建新用户
#             try:
#                 User.objects.create_user(username=mobile,
#                                          mobile=mobile,
#                                          password=password)
#             except Exception:
#                 return HttpResponseBadRequest('修改失败，请稍后再试')
#         else:
#             # 4.如果查询出手机号信息-->密码修改
#                 user.set_password(password)
#                 # 保存用户信息
#                 user.save()
#
#         # 6.跳转到登陆页面
#         response = redirect(reverse('users:login'))
#         # 7.返回响应
#         return response


# LoginRequiredMixin
# 如果用户未登录，则会进行默认跳转
class UserCenterView(LoginRequiredMixin, View):

    def get(self, request):
        # 获取登陆用户的信息
        user = request.user

        context = {
            'username': user.username,
            'mobile': user.mobile,
            'avatar': user.avatar.url if user.avatar else None,
            'user_desc': user.user_desc
        }
        return render(request, 'users_center.html', context=context)

    def post(self, request):
        """
        1.接收数据
        2.保存参数
        3.更新cookie
        4.刷新当前页面（重定向操作）
        5.返回响应
        """
        user = request.user
        # 1.接收数据
        username = request.POST.get('username', user.username)
        user_desc = request.POST.get('desc', user.user_desc)
        avatar = request.FILES.get('avatar')
        # 2.保存参数
        try:
            user.username = username
            user.user_desc = user_desc
            if avatar:
                user.avatar = avatar
            user.save()
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest('修改失败，请稍后再试')
        # 3.更新cookie
        response = redirect(reverse('users:center'))
        response.set_cookie('username', user.username, max_age=14*24*3600)
        # 4.刷新当前页面（重定向操作）
        # 5.返回响应
        return response


class WriteBlogView(View):

    def get(self, request):

        try:
            categories = ArticleCategory.objects.all()
        except ArticleCategory.DoesNotExist:
            return HttpResponseBadRequest('文章分类不存在')

        context = {
            'categories': categories
        }

        return render(request, 'articles_write_blog.html', context=context)

    def post(self, request):
        """
        1.接受数据
        2.验证数据
        3.数据入库
        4.跳转指定页面
        """
        # 1.接受数据
        avatar = request.FILES.get('avatar')
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        tags = request.POST.get('tags')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        user = request.user

        # 2.验证数据
        # 2.1 判断数据是否齐全
        if not all([avatar, title, category_id, summary, content]):
            return HttpResponseBadRequest('参数不全')
        # 2.2 判断分类id
        try:
            category = ArticleCategory.objects.get(id=category_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseBadRequest('没有此分类')

        # 3.数据入库
        try:
            article = Article.objects.create(
                author=user,
                avatar=avatar,
                title=title,
                category=category,
                tags=tags,
                summary=summary,
                content=content
            )
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest('发布失败，请稍后再试')

        # 4.跳转指定页面
        return redirect(reverse('articles:index'))


