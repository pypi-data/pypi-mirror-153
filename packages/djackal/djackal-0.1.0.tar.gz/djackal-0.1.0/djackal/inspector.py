from djackal.settings import djackal_settings
from djackal.utils import isiter


class skip:
    """
    When null is this class, that will removed in value dict.
    """
    pass


class InspectorException(Exception):
    def __init__(self, message):
        self.message = message


class InspectActionException(Exception):
    def __init__(self, key, value, action=None, param=None, message=None):
        self.action = action
        self.key = key
        self.value = value
        self.param = param
        self.message = message


class Inspector:
    """
    example of inspector map

    {
        key: {
            'required': True or False,
            'type': ['int', 'float', 'number', 'str', 'list', 'dict', 'bool'],
            'default': {DEFAULT_VALUE},
            'convert': [int, float, str, list, convert_function, ...],
            'valid': {Validation Function}
        },
        another_key: {
            ...actions
        }
    }
    """
    none_values = None
    type_maps = {
        'int': int,
        'float': float,
        'number': (int, float),
        'str': str,
        'bool': bool,
        'list': (tuple, list, set),
        'dict': dict,
    }
    allow_actions = ['required', 'default', 'convert', 'type', 'valid', 'unknown']

    def __init__(self, _map):
        self.inspect_map = _map

    def get_none_values(self):
        return self.none_values if self.none_values is not None else djackal_settings.DEFAULT_NONE_VALUES

    def action_unknown(self, key, value, param=None):
        """
        When data not exists in inspect_map
        """
        return skip

    def action_required(self, key, value, param):
        """
        When field has required.
        """
        required = param
        if required and value is None:
            raise InspectActionException(
                key, value, action='required', param=param,
                message='required field {} is not exists'.format(key)
            )
        return value

    def action_convert(self, key, value, param):
        """
        When field has convert, convert value
        """
        if not callable(param):
            raise InspectorException(
                message='{} convert param is not callable'.format(key)
            )
        return param(value)

    def action_type(self, key, value, param):
        """
        When field has type, check type.
        """
        if param not in self.type_maps:
            raise InspectActionException(
                key, value, action='type', param=param,
                message='type: {} is not allowed'.format(param)
            )
        if value is None:
            return value

        standard = self.type_maps[param]
        value_type = type(value)

        if (isiter(standard) and value_type in standard) or value_type is standard:
            return value
        raise InspectActionException(
            key, value, action='type', param=param,
            message='value type: {} is not {}'.format(value_type, param)
        )

    def action_default(self, key, value, param):
        """
        When field has default and value in none_values, return default
        """
        default = param
        if value is None:
            if param is skip:
                return skip
            elif callable(default):
                return default()
            return default
        return value

    def action_valid(self, key, value, param):
        if not callable(param):
            raise InspectActionException(
                key, value, action='valid', param=param,
                message='valid function: {} is not callable'.format(param)
            )

        if param(value):
            return value
        else:
            raise InspectActionException(
                key, value, action='valid', param=param,
                message='validation error: {} is invalid value {}'.format(key, value)
            )

    def sort_field(self, field):
        if 'required' in field and 'default' in field:
            raise InspectorException(
                'Inspect failed: required action cannot be used with default.'
            )
        elif 'convert' in field and 'type' in field:
            raise InspectorException(
                'Inspect failed: convert action cannot be used with type.'
            )

        result = {}
        for action in self.allow_actions:
            if action in field:
                result[action] = field[action]
        return result

    def inspect(self, data):
        result = {}

        # fields in inspect_map
        for key, field in self.inspect_map.items():
            raw_value = data.get(key)
            result[key] = raw_value if raw_value not in self.get_none_values() else None
            field = self.sort_field(field)
            for action, param in field.items():
                value = self.action(action, key, result[key], param)
                if value is skip:
                    result.pop(key, None)
                    break
                result[key] = value

        # data not in inspect_map
        unknown_data = {key: value for key, value in data.items() if key not in self.inspect_map}
        for key, value in unknown_data.items():
            value = self.action('unknown', key, value, None)
            if value is skip:
                continue
            result[key] = value
        return result

    def action(self, action, key, value, param):
        if action not in self.allow_actions:
            raise InspectorException('invalid action: {}'.format(action))
        method = getattr(self, 'action_{}'.format(action))
        return method(key, value, param)
