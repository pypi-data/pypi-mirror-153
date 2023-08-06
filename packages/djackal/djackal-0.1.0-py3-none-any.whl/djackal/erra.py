from enum import Enum


class Erra(Enum):
    def __str__(self):
        return self.name

    @property
    def message(self):
        return self.value

    @property
    def code(self):
        return self.name

    def get_message(self, context=None):
        message = self.message
        if context and message:
            message = message.format(**context)
        return message

    def response_data(self, context=None):
        message = self.get_message(context=context)
        return {'code': self.code, 'message': message}
