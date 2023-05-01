from django.db import models
from django.utils import timezone
from users.models import User


# Create your models here.
class ChatCompletionWithoutContext(models.Model):
    """
    不包含上下文关系的聊天生成模型
    """
    # 提问用户
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # 系统角色
    role = models.CharField(max_length=2048, blank=True)
    # prompt
    prompt = models.CharField(max_length=4096, blank=True)
    # completion
    completion = models.TextField()
    # 生成时间
    created = models.DateTimeField(default=timezone.now)

    # 修改表名，admin展示的配置信息
    class Meta:
        db_table = 'tb_chatcompletion_without_context'
        verbose_name = '聊天记录管理-无上下文关联'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
