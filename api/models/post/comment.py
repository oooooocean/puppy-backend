from django.db import models
from api.models.user.user import User
from api.models.post.post import Post
from api.models.base.audit_mixin import AuditMixin, AuditStatus
from rest_framework import serializers, relations
from api.models.user.user import UserInfoSerializer


class PostComment(AuditMixin):
    description = models.CharField('内容', max_length=200)
    create_time = models.DateTimeField('创建', auto_now_add=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    class Meta(object):
        verbose_name = '评论'


class PostCommentSerializer(serializers.ModelSerializer):
    owner_info = UserInfoSerializer(source='owner.info', read_only=True)
    owner = relations.PrimaryKeyRelatedField(read_only=True)
    post = relations.PrimaryKeyRelatedField(write_only=True, queryset=Post.objects.all())

    class Meta:
        model = PostComment
        exclude = ['audit_status', 'audit_description']

    def is_valid(self, raise_exception=False):
        self.initial_data['post'] = self.context['view'].kwargs['post_id']
        return super(PostCommentSerializer, self).is_valid(raise_exception)

    def create(self, validated_data):
        validated_data['audit_status'] = AuditStatus.SUCCESS.value
        validated_data['owner'] = self.context['request'].user
        return super(PostCommentSerializer, self).create(validated_data)
