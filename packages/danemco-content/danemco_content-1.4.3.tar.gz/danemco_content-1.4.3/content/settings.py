from django.conf import settings

PAGE_CACHE_TIMEOUT = getattr(settings, "PAGE_CACHE_TIMEOUT", 60 * 60 * 4)
