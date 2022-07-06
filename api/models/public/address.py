from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from rest_framework import serializers


class Address(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    latitude = models.FloatField('维度')
    longitude = models.FloatField('精度')
    country = models.CharField('国家', max_length=10)
    province = models.CharField('省份', max_length=10)
    city = models.CharField('城市', max_length=20)
    district = models.CharField('区县', max_length=30, null=True, blank=True)
    street = models.CharField('街道', max_length=30, null=True, blank=True)
    town = models.CharField('乡镇', max_length=30, null=True, blank=True)
    address = models.CharField('地址', max_length=100, null=True, blank=True)
    ad_code = models.CharField('行政区划编码', max_length=10)
    city_code = models.CharField('城市编码', max_length=10)
    slang = models.CharField('语义化描述', max_length=50, null=True, blank=True)
    poi_name = models.CharField('poi名称', max_length=50, null=True, blank=True)
    poi_address = models.CharField('poi地址', max_length=100, null=True, blank=True)


class AddressSerializer(serializers.ModelSerializer):
    district = serializers.CharField(write_only=True)
    street = serializers.CharField(write_only=True)
    town = serializers.CharField(write_only=True)
    ad_code = serializers.CharField(write_only=True)
    city_code = serializers.CharField(write_only=True)
    slang = serializers.CharField(write_only=True)

    class Meta:
        model = Address
        exclude = ['content_type', 'object_id']

