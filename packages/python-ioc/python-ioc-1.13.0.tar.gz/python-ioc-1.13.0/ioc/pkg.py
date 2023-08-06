"""Setup inversion-of-control through entrypoints."""
import pkg_resources
import os

from . import provider


IOC_ENTRYPOINT_NAME = 'ioc.providers'
IOC_SEARCH_PATH = list(
    filter(bool, str.split(os.getenv('IOC_SEARCH_PATH') or '', os.pathsep))
)
if not IOC_SEARCH_PATH:
    IOC_SEARCH_PATH = ['etc/ioc.conf', 'etc/ioc.conf.d/*']
IS_CONFIGURED = False


def get_providers():
    """Return the mapping of inversion-of-control providers and their
    entrypoints.
    """
    return [
        (entry_point.name, entry_point.load())
        for entry_point
        in pkg_resources.iter_entry_points('ioc.providers')
    ]


def setup(search_path: list = None):
    """Load all :term:`Dependency Providers` and start setting up the
    dependencies container.
    """
    global IS_CONFIGURED
    if IS_CONFIGURED:
        return

    import ioc
    for _, module in get_providers():
        if not hasattr(module, 'setup_ioc'):
            continue
        module.setup_ioc()

    search_path = search_path or IOC_SEARCH_PATH
    ioc.load_config(search_path, override=True)

    IS_CONFIGURED = True


def teardown():
    """Tear down the configured dependencies."""
    global IS_CONFIGURED
    provider.teardown()
    IS_CONFIGURED = False
