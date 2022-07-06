from django.db import models
from django.contrib import admin
from rest_framework import serializers
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from api.models.user.user import User


class Complain(models.Model):
    description = models.CharField(max_length=200)
    done = models.BooleanField('是否已处理', default=False)
    create_time = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '投诉'

    def __str__(self):
        return str(self.content_object)


class ComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = '__all__'


@admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    readonly_fields = ('description', 'content_object', 'content_type', 'object_id', 'owner')
    list_filter = ('done', )
