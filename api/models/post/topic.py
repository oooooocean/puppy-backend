from django.db import models
from api.models.post.post import Post
from api.models.user.user import User
from api.models.base.audit_mixin import AuditMixin
from rest_framework import serializers
from api.models.user.user import UserRole
from api.models.public.audit import AuditStatus


class PostTopic(AuditMixin):
    """
    话题
    auditRecords: 审核记录
    """
    title = models.CharField('话题标题', max_length=50)
    description = models.CharField('话题描述', max_length=200)
    create_time = models.DateTimeField('更新时间', auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')  # 创建者
    posts = models.ManyToManyField(Post, related_name='topics', blank=True)

    class Meta(object):
        verbose_name = '主题'

    def __str__(self):
        return self.title


class PostTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTopic
        fields = ['id', 'title', 'description']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        validated_data['audit_status'] = (
            AuditStatus.SUCCESS if user.role == UserRole.OFFICIAL else AuditStatus.BLOCK).value
        return super(PostTopicSerializer, self).create(validated_data)
