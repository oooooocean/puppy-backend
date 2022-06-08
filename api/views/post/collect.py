from rest_framework import viewsets, response, mixins
from ..base import BaseView
from api.common.permissions import IsAuthenticatedPermission
from api.common.authentication import PuppyAuthentication
from api.models.post.post import Post, PostSerializer


class PostCollectViewSet(BaseView, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = [PuppyAuthentication]
    permission_classes = [IsAuthenticatedPermission]

    def list(self, request, *args, **kwargs):
        user = request.user
        json = PostSerializer(user.collections, many=True).data
        return response.Response(json)

    def create(self, request, *args, **kwargs):
        is_collect = request.data.get('is_collect', True)
        post_id = request.data.get('post_id', None)
        post = Post.objects.get(pk=post_id)
        if is_collect:
            request.user.collections.add(post)
        else:
            request.user.collections.remove(post)
        return response.Response(True)
