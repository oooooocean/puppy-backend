from django.db import IntegrityError
from api.views.base import BaseView
from rest_framework import viewsets, decorators, response
from api.common.authentication import PuppyAuthentication
from api.common.permissions import OnlyOwnerEditPermission
from api.common.responses import fail_response
from api.common.exceptions import client_error, SaoException
from api.models.post.post import PostSerializer, Post
from api.models.public.comment import Comment, CommentSerializer
from api.models.public.complain import Complain
from api.models.public.audit import AuditStatus
from api.models.public.praise import Praise, PraiseSerializer


class PostViewSet(BaseView, viewsets.ModelViewSet):
    authentication_classes = [PuppyAuthentication]
    permission_classes = [OnlyOwnerEditPermission]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(audit_status=AuditStatus.SUCCESS.value) \
        .prefetch_related('pets', 'medias', 'praises', 'comments', 'topics', 'notice_users') \
        .select_related('owner')

    def get_queryset(self):
        queryset = self.queryset
        if user_id := self.request.query_params.get('user_id'):
            queryset = queryset.filter(owner=user_id)
        return queryset

    def list(self, request, *args, **kwargs):
        is_refresh = int(request.query_params.get('page', 1)) == 1
        if is_refresh:
            page = self.paginate_queryset(self.get_queryset())
        else:  # 加载更多
            start_id = request.query_params.get('start_id')
            if not start_id:
                raise client_error('参数缺失: start_id')
            page = self.paginate_queryset(self.get_queryset().filter(pk__lte=start_id))
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @decorators.action(methods=['post'], detail=True)
    def complain(self, request, pk):
        """
        举报帖子
        """
        post = self.queryset.get(pk=pk)
        Complain(description=request.data['description'], content_object=post, owner=request.user).save()
        return response.Response(True)

    @decorators.action(methods=['post', 'get', 'delete'], detail=True, permission_classes=[])
    def praise(self, request, _):
        """
        点赞
        """
        match request.method:
            case 'post':
                try:
                    post = self.get_object()
                    Praise(content_object=post, owner=request.user).save()
                except IntegrityError:
                    return fail_response(SaoException('请勿重复点赞', 1007))
                else:
                    return response.Response(True)
            case 'delete':
                self.get_object().praises.filter(owner=request.user).delete()
                return response.Response(True)
            case 'get':
                praises = self.get_object().praises.select_related('owner__info').all()
                page = self.paginate_queryset(praises)
                serializer = PraiseSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

    @decorators.action(methods=['post', 'delete'], detail=True)
    def collect(self, request, pk):
        """
        收藏
        """
        post = self.queryset.get(pk=pk)
        if request.method == 'post':
            request.user.collections.add(post)  # manyToMany 此时 post 已经存在
        else:
            request.user.collections.remove(post)
        return response.Response(True)

    @decorators.action(methods=['post', 'get'], detail=True, permission_classes=[])
    def comment(self, request, _):
        """
        评论
        """
        post = self.get_object()
        if request.method == 'post':
            comment = Comment(description=request.data.get('description'), content_object=post, owner=request.user)
            comment.save()
            return response.Response(CommentSerializer(comment).data)
        else:
            comments = self.get_object().comments.select_related('owner__info').all()
            page = self.paginate_queryset(comments)
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @decorators.action(methods=['post'], url_path='comment/complain', detail=True)
    def comment_complain(self, request, _):
        """
        举报评论
        """
        comment = self.get_object().comments.get(pk=request.data.get('comment_id'))
        Complain(description=request.data['description'], content_object=comment, owner=request.user).save()
        return response.Response(True)

    @decorators.action(methods=['post', 'delete'], url_path='comment/praise', detail=True)
    def comment_praise(self, request, _):
        """
        点赞评论
        """
        post = self.get_object()
        if request.method == 'post':
            try:
                comment = post.comments.get(pk=request.data.get('comment_id'))
                Praise(content_object=comment, owner=request.user).save()
            except IntegrityError:
                return fail_response(SaoException('请勿重复点赞', 1007))
        else:
            post.comments.filter(owner=request.user).delete()
        return response.Response(True)
