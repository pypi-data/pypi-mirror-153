# pylint: skip-file
from django.apps import AppConfig
from django.conf import settings

from .pkg import setup


class DependencyInjectionConfig(AppConfig):
    name = 'ioc'
    verbose_name = 'Dependency injection'

    def ready(self):
        if 'unimatrix' in settings.INSTALLED_APPS:
            # Do nothing if the unimatrix module is installed, because it also
            # invoked the ioc.pkg.setup() method.
            return
        setup(getattr(settings, 'IOC_SEARCH_PATH', None))
