import warnings

from djackal.shortcuts import get_model


class Initializer:
    def __init__(self):
        self.init_methods = {}

    def wrapper(self, func, key, finish_message=None, skip_message=None, bind_self=False, **options):
        def inner():
            djadis_model = get_model('storage.Storage')
            if not djadis_model.get('{}_init'.format(key), False):
                result = func(self) if bind_self else func()
                djadis_model.set('{}_init'.format(key), True)
                print(finish_message or 'Finished {} initializing'.format(key))
                return result
            else:
                print(skip_message or 'Skip {} initializing'.format(key))

        return inner

    def add(self, key, **options):
        def decorator(func):
            if key in self.init_methods:
                warnings.warn('Duplicated init_method key: {}. It will overwritten by method that defined later.')
            self.init_methods[key] = self.wrapper(func, key, **options)
            return func

        return decorator

    def run(self):
        for key, method in self.init_methods.items():
            method()
