from rest_framework import serializers
from api.models.pet import Pet, PetIntrinsic
from api.models.category.pet import PetCategory
from api.seralizers.user import UserInfoSerializer


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
