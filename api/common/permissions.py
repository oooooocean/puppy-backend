from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from api.models.user.user import UserStatus


class IsAuthenticatedPermission(IsAuthenticated):
    """
    登录用户: 1. 授权用户 2. 用户状态正常
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and request.user.status == UserStatus.NORMAL)


class OnlyOwnerEditPermission(BasePermission):
    """
    登录用户必须是owner才允许编辑
    """

    def has_permission(self, request, view):
        if request.method.upper() in SAFE_METHODS:
            return True
        if not request.user:
            return False
        user_id = view.kwargs.get('user_id')  # 获取路径参数中的user_id
        return user_id == request.user.pk if user_id else True

    def has_object_permission(self, request, view, obj):
        return self.check(request, view, obj)

    def check(self, request, view, obj=None):
        if request.method.upper() in SAFE_METHODS:
            return True

        if not request.user:
            return False

        current_is_owner = obj.owner.pk == request.user.pk  # 当前登录用户和owner一致

        if not current_is_owner:
            return False
        user_id = view.kwargs.get('user_id')
        return user_id == request.user.pk if user_id else True  # 确保前端的路径参数调用正确
