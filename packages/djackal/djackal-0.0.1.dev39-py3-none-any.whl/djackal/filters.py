class BaseFilterFunc:
    def action(self, name, value):
        func = getattr(self, name, None)
        if func is None:
            raise KeyError(f'QuanFunc not found by name: \'{name}\'')
        if not callable(func):
            raise ValueError(f'QuanFunc is not callable: \'{name}\'')

        return func(value)


class DefaultFilterFunc(BaseFilterFunc):
    def to_bool(self, value):
        if value.lower() in ['true', 't', 'yes', 'y', 'on', '1']:
            return True
        elif value.lower() in ['false', 'f', 'no', 'n', 'off', '0']:
            return False
        return None

    def to_int(self, value):
        return int(value)
