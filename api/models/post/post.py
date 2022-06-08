from django.db import models, transaction
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericRelation
from api.models.base.audit_mixin import AuditMixin
from api.models.user.user import User
from api.models.user.pet import Pet
from api.models.public.media import Media
from enum import IntEnum
from rest_framework import serializers, relations
from ..user.user import UserInfoSerializer
from ..public.audit import AuditStatus
from api.models.public.media import MediaSerializer, MediaInline


class PostType(IntEnum):
    """
    帖子类型
    """
    PHOTO = 0
    VIDEO = 1

    def __str__(self):
        return ['图文', '视频'][self.value]


class Post(AuditMixin):
    """
    medias: 图片or视频
    topics: 话题
    """
    description = models.TextField('帖子文案')
    type = models.IntegerField('类型', choices=[(i.value, str(i)) for i in PostType])
    create_time = models.DateTimeField('更新时间', auto_now_add=True)
    update_time = models.DateTimeField('创建时间', auto_now=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    pets = models.ManyToManyField(Pet, related_name='posts')
    collectors = models.ManyToManyField(User, related_name='collections')
    medias = GenericRelation(Media)

    class Meta(object):
        verbose_name = '帖子'


class PostSerializer(serializers.ModelSerializer):
    owner_info = UserInfoSerializer(source='owner.info', read_only=True)
    owner = relations.PrimaryKeyRelatedField(read_only=True)
    medias = MediaSerializer(many=True)

    class Meta:
        model = Post
        exclude = ['update_time', 'audit_status', 'audit_description', 'collectors']

    def create(self, validated_data):
        medias_json = validated_data.pop('medias')
        pet_json = validated_data.pop('pets')
        validated_data['owner'] = self.context['request'].user

        with transaction.atomic():
            post = Post(**validated_data)
            post.audit_status = AuditStatus.SUCCESS
            post.save()
            post.pets.set(pet_json)
            medias = [Media(type=media['type'], key=media['key'], content_object=post) for media in medias_json]
            Media.objects.bulk_create(medias)
            return post

    def update(self, instance, validated_data):
        medias_json = validated_data.pop('medias', None)
        pet_json = validated_data.pop('pets', None)

        with transaction.atomic():
            query = Post.objects.filter(pk=instance.pk)
            query.update(**validated_data)
            if medias_json:
                instance.medias.all().delete()
                medias = [Media(type=media['type'], key=media['key'], owner=instance) for media in medias_json]
                instance.medias.bulk_create(medias)
            if pet_json:
                instance.pets.set(pet_json)  # 直接重置, 不需要删除
            return query.first()

    def to_representation(self, instance):
        json = super(PostSerializer, self).to_representation(instance)
        pets = Pet.objects.filter(pk__in=json['pets'])
        json['pets'] = [{'id': pet.pk, 'name': pet.nickname, 'avatar': pet.avatar} for pet in pets]
        return json


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [MediaInline]
    readonly_fields = ('create_time', 'update_time')
    filter_horizontal = ('pets', )
    list_display = ('pk', 'owner', 'description')
    list_filter = ('audit_status', )
    sortable_by = []  # 禁用排序
