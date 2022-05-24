from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS


class IsAuthenticatedPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated)


class OnlyOwnerEditPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user_id = view.kwargs.get('user_id', None)
        return user_id == request.user.pk if user_id else True

    def has_object_permission(self, request, view, obj):
        return self.check(request, view, obj)

    def check(self, request, view, obj=None):
        if request.method in SAFE_METHODS:
            return True
        current_is_owner = obj.owner.pk == request.user.pk  # 当前登录用户和owner一致

        if not current_is_owner:
            return False
        user_id = view.kwargs.get('user_id', None)
        return user_id == request.user.pk if user_id else True
