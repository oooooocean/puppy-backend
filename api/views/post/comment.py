from api.views.base import BaseView
from api.models.post.comment import PostCommentSerializer, PostComment
from api.models.public import complain, audit
from rest_framework import viewsets, mixins, decorators, response
from api.common.authentication import PuppyAuthentication
from api.common.permissions import IsAuthenticatedPermission


class PostCommentViewSet(BaseView, mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    authentication_classes = [PuppyAuthentication]
    permission_classes = [IsAuthenticatedPermission]
    serializer_class = PostCommentSerializer
    pagination_class = None

    def get_queryset(self):
        return PostComment.objects.filter(post=self.kwargs['post_id'], audit_status=audit.AuditStatus.SUCCESS)

    @decorators.action(methods=['post'], detail=True)
    def complain(self, request, post_id, pk):
        comment = PostComment.objects.get(pk=pk)
        complain.Complain(description=request.data['description'], content_object=comment).save()
        return response.Response(True)
