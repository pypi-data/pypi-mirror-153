from django.core.management import BaseCommand

from djackal.loaders import initializer_loader


class Command(BaseCommand):
    def handle(self, *args, **options):
        initializer = initializer_loader()
        if not initializer:
            print('No initializers')

        print('Start initializing')
        initializer.run()
        print('Initialing done.')
