from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from rest_framework import serializers
from api.models.user.user import User, UserInfoSerializer


class Praise(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['pk']
        constraints = [
            models.UniqueConstraint(fields=['object_id', 'content_type', 'owner'], name='one_praise_one_target')]
        indexes = [
            models.Index(fields=['object_id', 'content_type'])
        ]


class PraiseSerializer(serializers.ModelSerializer):
    owner_info = UserInfoSerializer(source='owner.info')

    class Meta:
        model = Praise
        fields = ['owner_info', 'create_time']
