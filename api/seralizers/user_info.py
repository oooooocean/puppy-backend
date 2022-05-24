from rest_framework import serializers
from api.models.user import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        exclude = ['owner', 'update_time', 'create_time']

    def create(self, validated_data):
        validated_data['owner_id'] = self.context['view'].kwargs['user_id']
        return super(UserInfoSerializer, self).create(validated_data)
