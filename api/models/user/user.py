from django.db import models
from enum import IntEnum, IntFlag
from rest_framework import serializers
from .user_info import UserInfoSerializer
from ..public.audit import AuditStatus


class UserRole(IntEnum):
    NORMAL = 0
    OFFICIAL = 1


class UserPermission(IntFlag):
    pass


class UserStatus(IntEnum):
    NORMAL = 0
    BLOCKING = 1


class User(models.Model):
    """
    用户
    """
    is_active = True
    is_authenticated = True

    phone = models.CharField('手机号', max_length=11)
    status = models.IntegerField('状态', choices=[(i.value, str(i)) for i in UserStatus], default=UserStatus.NORMAL.value)
    role = models.IntegerField('角色', choices=[(i.value, str(i)) for i in UserRole], default=UserRole.NORMAL.value)
    password = models.CharField('密码', max_length=100, null=True, blank=False)
    create_time = models.DateTimeField('账户创建时间', auto_now_add=True)
    last_login = models.DateTimeField('最近登录时间', auto_now_add=True)

    fans = models.ManyToManyField('User', related_name='idols')
    post_notices = models.ManyToManyField('Post', related_name='notice_users')

    def __str__(self):
        return self.phone

    @property
    def pet_count(self):
        return self.pets.count()

    @property
    def is_blocking(self):
        return self.status == UserStatus.BLOCKING.value

    @property
    def social(self):
        """
        社交属性: 点赞数, 粉丝数, 关注数
        """
        praise_count = sum([post.praises.count() for post in
                            self.posts.filter(audit_status=AuditStatus.SUCCESS).prefetch_related('praises').all()])
        return {
            'praiseCount': praise_count,
            'fansCount': self.fans.count(),
            'idolCount': self.idols.count()
        }

    @property
    def has_password(self):
        return self.password is not None


class UserSerializer(serializers.ModelSerializer):
    info = UserInfoSerializer(read_only=True)
    social = serializers.DictField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'info', 'pet_count', 'social')


class LoginUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'info', 'pet_count', 'social', 'has_password')


class UserSimpleSerializer(serializers.ModelSerializer):
    info = UserInfoSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'info')

    def run_validation(self, data):
        if isinstance(data, int):
            return data
        return super(UserSimpleSerializer, self).run_validation(data)
