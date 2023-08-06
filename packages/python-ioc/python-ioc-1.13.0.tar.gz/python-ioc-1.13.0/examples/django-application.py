# pylint: skip-file
from django.conf import settings
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path

import ioc


@ioc.inject('value', 'DjangoDependency')
def request_handler(request, value):
    return HttpResponse(value)


urlpatterns = [
    path('', request_handler)
]


if __name__ == '__main__':
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=['ioc'],
        ROOT_URLCONF='__main__',
        SECRET_KEY='changeme'
    )

    application = get_wsgi_application()
    call_command('runserver',  '127.0.0.1:8000')
