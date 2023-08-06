VERSION = (1, 4, 3)


def get_version():
    return '.'.join([str(i) for i in VERSION])


__version__ = get_version()


def load_snippets():
    """
    search for a snippets module in each app and try to import it.
    the snippets module should register forms to use as snippets.
    """
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            import_module('%s.snippets' % app)
        except Exception:
            if module_has_submodule(mod, 'snippets'):
                raise
