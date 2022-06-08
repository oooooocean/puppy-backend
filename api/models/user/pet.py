from django.db import models
from api.models.user.user import User
from api.models.gender import Gender
from api.common.configuration import Configuration
from rest_framework import serializers, relations
from api.models.category.pet import PetCategory
from api.models.user.user import UserInfoSerializer
from django.contrib import admin


class Pet(models.Model):
    """
    宠物
    """
    nickname = models.CharField('昵称', max_length=50)
    avatar = models.CharField('照片', max_length=255)
    introduction = models.CharField('个性签名', max_length=int(Configuration.MAX_INTRODUCTION.evaluation), blank=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')  # 主人

    def __str__(self):
        return f'{self.owner.info.nickname}的{self.nickname}'


class PetIntrinsic(models.Model):
    """
    宠物的自然属性
    """
    owner = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name='intrinsic', primary_key=True)
    gender = models.IntegerField('性别', choices=[(i.value, str(i)) for i in Gender])
    category = models.IntegerField('类别', choices=[(i.value, str(i)) for i in PetCategory])
    sub_category = models.IntegerField('子类别')
    birthday = models.DateField('生日')
    neuter = models.BooleanField('是否绝育', null=True)


class PetIntrinsicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetIntrinsic
        exclude = ['owner']

    def validate(self, attrs):
        """
        验证sub_category是属于category的.
        """
        category = PetCategory(attrs['category'])
        subcategory = attrs['sub_category']
        if subcategory not in [i['id'] for i in category.sub_category()]:
            raise serializers.ValidationError('sub_category 不在范围')
        return attrs


class PetSerializer(serializers.ModelSerializer):
    owner_info = UserInfoSerializer(source='owner.info', read_only=True)
    owner = relations.PrimaryKeyRelatedField(read_only=True)
    intrinsic = PetIntrinsicSerializer()

    class Meta:
        model = Pet
        fields = '__all__'

    def create(self, validated_data):
        intrinsic = validated_data.pop('intrinsic')
        pet = Pet.objects.create(owner_id=self.context['view'].kwargs['user_id'], **validated_data)
        PetIntrinsic.objects.create(owner=pet, **intrinsic)
        return pet

    def update(self, instance, validated_data):
        intrinsic_data = validated_data.pop('intrinsic', None)
        if intrinsic_data:  # 更新自然属性
            self.fields['intrinsic'].update(instance.intrinsic, intrinsic_data)

        if validated_data:  # 更新社会属性
            query = Pet.objects.filter(pk=instance.pk)
            query.update(**validated_data)
            return query.first()
        return instance


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    pass