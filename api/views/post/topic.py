from rest_framework import viewsets, mixins
from api.models.post.topic import PostTopic
from api.models.public.audit import AuditStatus
from api.common.authentication import PuppyAuthentication
from api.common.permissions import IsAuthenticatedPermission
from api.models.post.topic import PostTopicSerializer
from api.views.base import BaseView


class PostTopicViewSet(BaseView,
                       mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    authentication_classes = [PuppyAuthentication]
    permission_classes = [IsAuthenticatedPermission]
    serializer_class = PostTopicSerializer
    pagination_class = None
    queryset = PostTopic.objects.filter(audit_status=AuditStatus.SUCCESS.value)


