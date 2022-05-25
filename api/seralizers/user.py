from rest_framework import serializers
from rest_framework.fields import IntegerField
from api.models.user import User, UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        exclude = ['owner', 'update_time', 'create_time']

    def create(self, validated_data):
        validated_data['owner_id'] = self.context['view'].kwargs['user_id']
        return super(UserInfoSerializer, self).create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    info = UserInfoSerializer(read_only=True)
    pet_count = IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone', 'info', 'pet_count')
