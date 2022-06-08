from django.db import models
from enum import IntEnum, IntFlag
from rest_framework import serializers
from rest_framework.fields import IntegerField
from .user_info import UserInfoSerializer


class UserRole(IntEnum):
    NORMAL = 0
    OFFICIAL = 1


class UserPermission(IntFlag):
    pass


class User(models.Model):
    """
    用户
    """
    is_active = True
    is_authenticated = True

    phone = models.CharField('手机号', max_length=11)
    role = models.IntegerField('角色', choices=[(i.value, str(i)) for i in UserRole], default=UserRole.NORMAL.value)

    def __str__(self):
        return self.phone

    @property
    def pet_count(self):
        return self.pets.count()


class UserSerializer(serializers.ModelSerializer):
    info = UserInfoSerializer(read_only=True)
    pet_count = IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone', 'info', 'pet_count')
