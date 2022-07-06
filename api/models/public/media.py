from django.db import models
from enum import IntEnum
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.admin import GenericTabularInline


class MediaType(IntEnum):
    PICTURE = 0
    VIDEO = 1

    def __str__(self):
        return ['图片', '视频'][self.value]


class Media(models.Model):
    key = models.CharField('七牛云Key', max_length=500)
    type = models.IntegerField('类型', choices=[(i.value, str(i)) for i in MediaType])
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    def __str__(self):
        return f'{MediaType(self.type)}: {self.key}'

    class Meta:
        verbose_name = '图片/视频'
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = ['content_type', 'object_id']


class MediaInline(GenericTabularInline):
    """
    图片, 视频编辑
    """
    model = Media
    extra = 0
