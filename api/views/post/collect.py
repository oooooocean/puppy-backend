from rest_framework import viewsets, response, mixins
from ..base import BaseView
from api.common.permissions import IsAuthenticatedPermission
from api.common.authentication import PuppyAuthentication
from api.models.post.post import Post, PostSerializer


class PostCollectViewSet(BaseView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    authentication_classes = [PuppyAuthentication]
    permission_classes = [IsAuthenticatedPermission]

    def list(self, request, *args, **kwargs):
        """
        获取收藏列表
        """
        page = self.paginate_queryset(request.user.collections.all())
        serializer = PostSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        收藏
        """
        post_id = request.data.get('post_id', None)
        post = Post.objects.get(pk=post_id)
        request.user.collections.add(post)  # manyToMany 此时 post 已经存在
        return response.Response(True)

    def destroy(self, request, *args, **kwargs):
        post_id = request.data.get('post_id', None)
        post = Post.objects.get(pk=post_id)
        request.user.collections.remove(post)
        return response.Response(True)
