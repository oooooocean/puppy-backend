from rest_framework import viewsets, mixins, generics
from ..base import BaseView
from api.common.authentication import PuppyAuthentication
from api.common.permissions import IsAuthenticatedPermission
from api.models.support.feedback import FeedbackSerializer


class FeedbackView(BaseView, generics.CreateAPIView):
    authentication_classes = [PuppyAuthentication]
    permission_classes = [IsAuthenticatedPermission]
    serializer_class = FeedbackSerializer

    def create(self, request, *args, **kwargs):
        res = super(FeedbackView, self).create(request, *args, **kwargs)
        res.data = True
        return res
