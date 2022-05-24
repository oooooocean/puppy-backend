from rest_framework import viewsets, permissions
from api.models.pet import Pet
from api.seralizers.pet import PetSerializer
from api.common.authentication import PuppyAuthentication
from api.common.permissions import IsAuthenticatedPermission, OnlyOwnerEditPermission
from api.views.base import BaseView


class PetViewSet(BaseView, viewsets.ModelViewSet):
    authentication_classes = [PuppyAuthentication]
    permission_classes = [IsAuthenticatedPermission, OnlyOwnerEditPermission]
    serializer_class = PetSerializer
    pagination_class = None

    def get_queryset(self):
        if self.action == 'list':
            return Pet.objects.filter(owner=self.kwargs['user_id'])
        return Pet.objects.all()

