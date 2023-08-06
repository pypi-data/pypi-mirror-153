from django import template
from django.conf import settings
from django.core.cache import cache
from django.template import TemplateSyntaxError
from django.utils.html import mark_safe
from six import text_type

from .. import settings as content_settings
from ..models import Page, Section

register = template.Library()


@register.simple_tag()
def concat(*args, **kwargs):
    return "".join([text_type(a) for a in args])


@register.simple_tag(takes_context=True)
def snippet(context, section="", default=""):
    section = section.strip()
    if section:
        try:
            section = Section.objects.get(name=section)
        except Section.DoesNotExist:
            if settings.TEMPLATES[0]['OPTIONS'].get('debug', settings.DEBUG):
                raise
            return default

        request = context.get('request', None)
        if request:
            path = request.path
        else:
            path = "/"

        my_snippet = section.snippets.from_url(path)
        if my_snippet:
            return mark_safe(my_snippet.render(context))
        return default
    else:
        if settings.TEMPLATES[0]['OPTIONS'].get('debug', settings.DEBUG):
            raise TemplateSyntaxError(
                "You must provide the name of the section"
            )
        return mark_safe(default)


@register.simple_tag()
def page(url):
    try:
        retval = cache.get(url, None)
        if retval is None:
            retval = Page.objects.get(url=url)
            cache.set(url, retval, content_settings.PAGE_CACHE_TIMEOUT)
        return retval
    except Page.DoesNotExist:
        cache.set(url, '', content_settings.PAGE_CACHE_TIMEOUT)
        return None
