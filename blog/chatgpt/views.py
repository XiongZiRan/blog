import json

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from chatgpt.models import ChatCompletionWithoutContext
from django.shortcuts import redirect
from django.urls import reverse

from .secret_key import API_KEY
import openai
openai.api_key = API_KEY

import logging
logger = logging.getLogger('django')

import os
# os.environ['http_proxy'] = "http://proxy.127.0.0.1:7890"
# os.environ['https_proxy'] = "http://proxy.127.0.0.1:7890"
os.environ['ALL_PROXY'] = 'http://127.0.0.1:7890'


# Create your views here.
class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        # 获取登陆用户的信息
        user = request.user
        print(user.username)
        context = {
            'username': user.username,
            'mobile': user.mobile,
            'avatar': user.avatar.url if user.avatar else None,
            'user_desc': user.user_desc
        }
        return render(request, 'chatgpt_index.html', context=context)

    def get_result(self, messages):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        messages.append(completion.choices[0].message)
        return messages

    def post(self, request):
        """
        1.接收prompt
        2.生成completion
        3.写入数据库
        4.传回前端显示
        """
        try:
            # 1.接收prompt
            user = request.user
            prompt = request.POST.get('prompt')

            print(prompt)

            # 2.生成completion
            messages = [{"content": "你是个乐于助人的助手", "role": "system"}, {"content": prompt, "role": "user"}]
            print("$ Wait for GPT $")
            messages = self.get_result(messages)
            print("GPT回答：", messages[-1].content)
            completion = messages[-1].content

            # 3.写入数据库
            try:
                chat_completion = ChatCompletionWithoutContext.objects.create(
                    user=user,
                    role=messages[0]['content'],
                    prompt=prompt,
                    completion=completion
                )
            except Exception as e:
                logger.error(e)
                return HttpResponseBadRequest('对话生成失败，请稍后再试')
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest('请求openai失败')

        return JsonResponse({'completion': completion})

        # 4.传回前端显示
        # context = {
        #     'username': user.username,
        #     'mobile': user.mobile,
        #     'avatar': user.avatar.url if user.avatar else None,
        #     'user_desc': user.user_desc,
        #     'prompt': chat_completion.prompt,
        #     'completion': chat_completion.completion,
        #     'created': chat_completion.created
        # }
        # return render(request, 'chatgpt_index.html', context=context)

