from rest_framework.exceptions import APIException


class DjackalAPIException(APIException):
    default_message = ''
    default_status_code = 500

    def __init__(self, message=None, status_code=None):
        self.message = message
        self.status_code = status_code or self.default_status_code

    def __str__(self):
        return self.message

    def response_data(self):
        return {}

    def get_status_code(self):
        return getattr(self, 'status_code', self.default_status_code)


class ErraException(DjackalAPIException):
    default_status_code = 500

    def __init__(self, erra=None, code=None, message=None, context=None, status_code=None, **kwargs):
        self.erra = erra
        self.message = message
        self.code = code
        self.context = context
        self.kwargs = kwargs
        self.status_code = status_code or self.default_status_code

    def __str__(self):
        return self.get_message()

    def get_message(self):
        if self.message:
            return self.message
        elif self.erra:
            return self.erra.message
        return None

    def response_data(self):
        if self.erra:
            response = self.erra.response_data(context=self.context)
        else:
            response = {'code': self.code, 'message': self.message}
        response.update(self.kwargs)
        return response


class NotFound(DjackalAPIException):
    default_status_code = 404
    default_message = 'Data not found'

    def __init__(self, message=None, context=None, model=None, status_code=None, **kwargs):
        self.context = context
        self.kwargs = kwargs
        self.model = model
        self.message = message or self.default_message
        self.status_code = status_code or self.default_status_code

    def response_data(self):
        return {
            'code': 'NOT_FOUND',
            'message': self.message,
            **self.kwargs
        }


class BadRequest(ErraException):
    default_status_code = 400


class Unauthorized(ErraException):
    default_status_code = 401


class Forbidden(ErraException):
    default_status_code = 403


class NotAllowed(ErraException):
    default_status_code = 405


class InternalServer(ErraException):
    default_status_code = 500


class PermissionException(ErraException):
    default_status_code = 403

    def __init__(self, permission, erra=None, code=None, message=None, context=None, status_code=None, **kwargs):
        super().__init__(erra=erra, code=code, message=message, context=context, status_code=status_code, **kwargs)
        self.permission = permission
