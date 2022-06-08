from django.db import models
from django.contrib import admin
from rest_framework import serializers
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Complain(models.Model):
    description = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = '投诉'

    def __str__(self):
        return str(self.content_type)


class ComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = '__all__'


@admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    readonly_fields = ('description', 'content_object', 'content_type', 'object_id')
