from rest_framework import permissions


class AdvertisementObjectPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # К конкретному объявлению со статусом "DRAFT" имеют доступ аутентифицированные автор и администратор.
        if obj.status == 'DRAFT':
            return bool(request.user == obj.creator or request.user.is_superuser)

        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user == obj.creator or request.user.is_superuser)


class AdvertisementModelPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return True




