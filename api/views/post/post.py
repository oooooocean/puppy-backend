from rest_framework import viewsets, decorators, response
from api.common.authentication import PuppyAuthentication
from api.common.permissions import OnlyOwnerEditPermission
from api.models.post.post import PostSerializer, Post
from api.views.base import BaseView
from api.models.public.complain import Complain
from api.models.public.audit import AuditStatus


class PostViewSet(BaseView, viewsets.ModelViewSet):
    authentication_classes = [PuppyAuthentication]
    permission_classes = [OnlyOwnerEditPermission]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(audit_status=AuditStatus.SUCCESS.value)

    @decorators.action(methods=['post'], detail=True)
    def complain(self, request, pk):
        post = self.queryset.get(pk=pk)
        Complain(description=request.data['description'], content_object=post).save()
        return response.Response(True)