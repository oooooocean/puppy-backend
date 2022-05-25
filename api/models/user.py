from django.db import models
from api.models.gender import Gender
from api.common.configuration import Configuration


class User(models.Model):
    """
    用户
    """
    is_active = True
    is_authenticated = True

    phone = models.CharField('手机号', max_length=11)

    def __str__(self):
        return self.phone

    @property
    def pet_count(self):
        return self.pets.count()


class UserInfo(models.Model):
    """
    用户属性
    """
    nickname = models.CharField('昵称', max_length=20)
    gender = models.IntegerField('性别', choices=[(i.value, str(i)) for i in Gender], null=True)
    introduction = models.CharField('宠物寄语', max_length=int(Configuration.MAX_INTRODUCTION.evaluation), blank=True)
    avatar = models.CharField('照片', max_length=500, blank=True)
    create_time = models.DateTimeField('更新时间', auto_now_add=True)
    update_time = models.DateTimeField('创建时间', auto_now=True)

    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info', primary_key=True)

    def __str__(self):
        return self.nickname
