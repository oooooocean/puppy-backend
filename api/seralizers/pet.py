from rest_framework import serializers
from api.models.pet import Pet, PetIntrinsic
from api.models.pet_category import PetCategory
from api.seralizers.user_info import UserInfoSerializer


class PetIntrinsicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetIntrinsic
        exclude = ['owner']

    def validate(self, attrs):
        category = PetCategory(attrs['category'])
        subcategory = attrs['sub_category']
        if subcategory not in [i.id for i in category.sub_category()]:
            raise serializers.ValidationError('subcategory 不在范围')
        return attrs


class PetSerializer(serializers.ModelSerializer):
    owner_info = UserInfoSerializer(read_only=True)
    intrinsic = PetIntrinsicSerializer()
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

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
        if intrinsic_data:
            self.fields['intrinsic'].update(instance.intrinsic, intrinsic_data)

        query = Pet.objects.filter(pk=instance.pk)
        if validated_data:
            query.update(**validated_data)
        return query.first()
