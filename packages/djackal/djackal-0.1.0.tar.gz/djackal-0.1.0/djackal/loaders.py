from djackal.settings import djackal_settings, perform_import


def initializer_loader():
    return perform_import(djackal_settings.INITIALIZER, 'INITIALIZER')
