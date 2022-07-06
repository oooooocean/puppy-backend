from enum import IntEnum
from rest_framework import serializers, relations, fields
from django.db import models, transaction
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericRelation
from ..base.audit_mixin import AuditMixin
from ..user.user import User, UserInfoSerializer, UserSimpleSerializer
from ..user.pet import Pet
from ..public.media import Media, MediaSerializer, MediaInline
from ..public.audit import AuditStatus
from ..public.praise import Praise
from ..public.comment import Comment
from ..public.address import Address, AddressSerializer
from .topic import PostTopicSerializer, PostTopic


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
    praises = GenericRelation(Praise)
    comments = GenericRelation(Comment)
    addresses = GenericRelation(Address)

    class Meta(object):
        verbose_name = '帖子'
        ordering = ('-pk',)  # 主键倒序排列

    def social(self, user: int):
        return {
            'praiseCount': self.praises.count(),
            'commentCount': self.comments.count(),
            'hasPraise': self.praises.filter(owner=user).exists(),
            'hasFollow': self.owner.fans.filter(pk=user).exists()
        }

    @property
    def address(self):
        return self.addresses.get()

    def __str__(self):
        return f'帖子: {self.pk}'


class PostSerializer(serializers.ModelSerializer):
    medias = MediaSerializer(many=True)
    owner_info = UserInfoSerializer(source='owner.info', read_only=True)
    owner = relations.PrimaryKeyRelatedField(read_only=True)
    topics = PostTopicSerializer(many=True, required=False)
    pets = relations.PrimaryKeyRelatedField(many=True, required=False, queryset=Pet.objects.all())
    notice_users = UserSimpleSerializer(many=True, required=False)
    address = AddressSerializer(required=False)

    class Meta:
        model = Post
        exclude = ['update_time', 'audit_status', 'audit_description', 'collectors']

    def create(self, validated_data):
        medias_json = validated_data.pop('medias')
        pet_json = validated_data.pop('pets', None)
        address_json = validated_data.pop('address', None)
        topic_json = validated_data.pop('topics', None)
        notice_json = validated_data.pop('notice_users', None)
        validated_data['owner'] = self.context['request'].user

        with transaction.atomic():
            post = Post(**validated_data)
            post.audit_status = AuditStatus.SUCCESS
            post.save()

            if pet_json:
                post.pets.set(pet_json)
            if address_json:
                post.addresses.add(Address(**address_json), bulk=False)
            if topic_json:
                topics = PostTopic.objects.filter(pk__in=topic_json).all()
                post.topics.set(topics)
            if notice_json:
                notices = post.owner.idols.filter(pk__in=notice_json).all()
                post.notice_users.set(notices)

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

    def to_representation(self, instance: Post):
        json = super(PostSerializer, self).to_representation(instance)
        pets = Pet.objects.filter(pk__in=json['pets'])
        json['pets'] = [{'id': pet.pk, 'nickname': pet.nickname, 'avatar': pet.avatar} for pet in pets]
        json['social'] = instance.social(self.context['request'].user.pk)
        return json


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [MediaInline]
    readonly_fields = ('create_time', 'update_time')
    filter_horizontal = ('pets', )
    list_display = ('pk', 'owner', 'description')
    list_filter = ('audit_status', )
    sortable_by = []  # 禁用排序
