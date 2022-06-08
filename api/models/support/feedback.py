from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from ..public.media import Media, MediaInline
from rest_framework import serializers
from ..public.media import MediaSerializer
from django.contrib import admin


class Feedback(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)

    medias = GenericRelation(Media, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '反馈'


class FeedbackSerializer(serializers.ModelSerializer):
    medias = MediaSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Feedback
        fields = '__all__'

    def create(self, validated_data):
        medias_json = validated_data.pop('medias', None)
        feedback = super(FeedbackSerializer, self).create(validated_data)
        if medias_json:
            feedback.medias.bulk_create(
                [Media(type=media['type'], key=media['key'], content_object=feedback) for media in medias_json])
        return feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    inlines = [MediaInline]
    readonly_fields = ('create_time', 'title', 'description')