from django.db import models
from api.models.user.user import User
from api.models.base.audit_mixin import AuditMixin, AuditStatus
from rest_framework import serializers, relations
from api.models.user.user import UserInfoSerializer
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Comment(AuditMixin):
    description = models.CharField('内容', max_length=200)
    create_time = models.DateTimeField('创建', auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta(object):
        verbose_name = '评论'

    def __str__(self):
        return f'评论: {self.pk}'


class CommentSerializer(serializers.ModelSerializer):
    owner_info = UserInfoSerializer(source='owner.info', read_only=True)
    owner = relations.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        exclude = ['audit_status', 'audit_description', 'content_type', 'object_id']
