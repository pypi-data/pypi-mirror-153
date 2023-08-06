from rest_framework import permissions

from djackal.exceptions import PermissionException

REAL_SAFE_METHOD = ('OPTIONS', 'HEAD')
POST = 'POST'
GET = 'GET'
PATCH = 'PATCH'
PUT = 'PUT'
DELETE = 'DELETE'


class ErraPermission(permissions.BasePermission):
    hard = False
    erra = None
    status_code = 403
    code = None
    message = None

    def get_message(self, request, view, obj=None):
        return self.message

    def get_erra(self, request, view, obj=None):
        return self.erra

    def get_status_code(self, request, view, obj=None):
        return self.status_code

    def get_code(self, request, view, obj=None):
        return self.code

    def raise_error(self, request, view, obj=None):
        raise PermissionException(
            permission=self,
            erra=self.get_erra(request, view, obj),
            code=self.get_code(request, view, obj),
            message=self.get_message(request, view, obj),
            status_code=self.get_status_code(request, view, obj)
        )

    def handle(self, request, view):
        return True

    def handle_object(self, request, view, obj):
        return True

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if self.handle(request, view):
            return True

        if self.hard:
            self.raise_error(request, view)
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if self.handle_object(request, view, obj):
            return True

        if self.hard:
            self.raise_error(request, view, obj=obj)
        else:
            return False


class _MethodPermission(ErraPermission):
    allow_method = None

    def handle(self, request, view):
        if request.method in REAL_SAFE_METHOD:
            return True
        return request.method == self.allow_method

    def handle_object(self, request, view, obj):
        return self.handle(request, view)


class IsGet(_MethodPermission):
    """
    if request method is GET return True
    """
    allow_method = GET


class IsPost(_MethodPermission):
    """
    if request method is POST return True
    """
    allow_method = POST


class IsPut(_MethodPermission):
    """
    if request method is PUT return True
    """
    allow_method = PUT


class IsPatch(_MethodPermission):
    """
    if request method is PATCH return True
    """
    allow_method = PATCH


class IsDelete(_MethodPermission):
    """
    if request method is DELETE return True
    """
    allow_method = DELETE
