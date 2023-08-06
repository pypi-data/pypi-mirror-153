from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.query_utils import Q
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class PageManager(models.Manager):

    def get_current(self, url):
        """ gets the current revision of this page at the given URL """
        try:
            page = Page.objects.get(url=url)
            page.title = mark_safe(page.title)
            page.content = mark_safe(page.content)

            return page
        except ObjectDoesNotExist:
            return None


class Page(models.Model):
    url = models.CharField(
        _('URL'),
        max_length=300,
        db_index=True,
        help_text='Be sure to include slashes at the beginning and at the end'
    )
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'), blank=True)
    enable_comments = models.BooleanField(_('enable comments'), default=False)
    template_name = models.CharField(
        _('template name'),
        max_length=200,
        blank=True,
        help_text=_(
            "Example: 'content/contact_page.html'. If this isn't provided, "
            "the system will use 'content/page.html'."
        ),
    )
    registration_required = models.BooleanField(
        _('registration required'),
        help_text=_("If this is checked, only logged-in users will be able to view the page."),
        default=False
    )
    sites = models.ManyToManyField(Site)
    keywords = models.TextField(blank=True)
    description = models.TextField(blank=True)

    objects = PageManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.url


class Section(models.Model):
    """
    The section of a web page that allows placing of snippets.
    """
    name = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class SnippetManager(models.Manager):

    def from_url(self, url):
        paths = ['/']
        for p in url.split('/'):
            if not p:
                continue
            paths.append("%s%s/" % (paths[-1], p))
        now = timezone.now()
        qs = self.get_queryset()
        qs = qs.filter(
            Q(exact_url=True, url=url) | Q(exact_url=False, url__in=paths),
            Q(publish__isnull=True) | Q(publish__lte=now),
            Q(expire__isnull=True) | Q(expire__gte=now)
        ).order_by("url", "expire", "-publish")
        if qs:

            # explicitly published or expiring pages take
            # precedence to pages that aren't
            # expire takes precedence over publish
            if any([a.expire is not None for a in qs]):
                qs = [a for a in qs if a.expire]
            elif any([a.publish is not None for a in qs]):
                qs = [a for a in qs if a.publish]
            return qs[0]
        return None


class Snippet(models.Model):
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="snippets",
    )
    url = models.CharField(
        _('URL'),
        max_length=200,
        blank=True,
        default="/",
        db_index=True,
    )
    exact_url = models.BooleanField(
        verbose_name="Exact URL", db_index=True, default=False,
        help_text="Check to only match this url (no sub-urls).")
    publish = models.DateTimeField(null=True, blank=True)
    expire = models.DateTimeField(null=True, blank=True)
    content = models.TextField(blank=True)
    # format = models.CharField(max_length=200, default="HTML",
    #     choices=(("html", "HTML"),))

    objects = SnippetManager()

    def __str__(self):
        return u"%s %s" % (self.section, self.url)

    def render(self, context=None):
        """
        Wrapper around the SnippetForm render to pass the context along.
        """
        return self.content
