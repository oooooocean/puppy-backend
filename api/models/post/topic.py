from django.db import models
from rest_framework import serializers
from ..user.user import User, UserRole
from ..base.audit_mixin import AuditMixin
from ..public.audit import AuditStatus


class PostTopic(AuditMixin):
    """
    话题
    """
    title = models.CharField('话题标题', max_length=50)
    description = models.CharField('话题描述', max_length=200)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')  # 创建者
    posts = models.ManyToManyField('Post', related_name='topics', blank=True)

    class Meta(object):
        verbose_name = '主题'

    def __str__(self):
        return self.title


class PostTopicSerializer(serializers.ModelSerializer):
    content_count = serializers.IntegerField(source='posts.count')

    class Meta:
        model = PostTopic
        fields = ['id', 'title', 'description', 'content_count']

    def run_validation(self, data):
        if isinstance(data, int):
            return data
        return super(PostTopicSerializer, self).run_validation(data)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        validated_data['audit_status'] = (
            AuditStatus.SUCCESS if user.role == UserRole.OFFICIAL else AuditStatus.BLOCK).value
        return super(PostTopicSerializer, self).create(validated_data)
