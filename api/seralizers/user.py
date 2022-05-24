from rest_framework import serializers
from rest_framework.fields import IntegerField
from api.seralizers.user_info import UserInfoSerializer
from api.models.user import User


class UserSerializer(serializers.ModelSerializer):
    info = UserInfoSerializer(read_only=True)
    pet_count = IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone', 'info', 'pet_count')