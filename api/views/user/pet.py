from rest_framework import viewsets
from api.models.user.pet import Pet
from api.models.user.pet import PetSerializer
from api.common.authentication import PuppyAuthentication
from api.common.permissions import IsAuthenticatedPermission, OnlyOwnerEditPermission
from ..base import BaseView


class PetViewSet(BaseView, viewsets.ModelViewSet):
    """
    user/user_id/pets/
    user/user_id/pets/pet_id/ 查询指定用户下的指定宠物
    """
    authentication_classes = [PuppyAuthentication]
    permission_classes = [IsAuthenticatedPermission, OnlyOwnerEditPermission]
    serializer_class = PetSerializer
    pagination_class = None

    def get_queryset(self):
        if self.action == 'list':
            return Pet.objects.filter(owner=self.kwargs['user_id'])
        return Pet.objects.all()

