from __future__ import print_function

import json

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import redirect_to_login
from django.core.cache import cache
from django.forms.models import modelform_factory
from django.http import Http404, HttpResponse
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from . import settings as content_settings
from .models import Page


class PageDetailView(DetailView):
    """
    this view is not registered in the urls because it is called from
    the PageFallbackMiddleware.
    """

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.registration_required and \
                not request.user.is_authenticated:
            return redirect_to_login(request.path)
        return super(PageDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        url = self.kwargs.get("url", self.request.path)

        try:
            retval = cache.get(url)
            if not retval:
                retval = Page.objects.get(url=url)
                cache.set(url, retval, content_settings.PAGE_CACHE_TIMEOUT)
        except Page.DoesNotExist:
            opt_out = "nocreate" in self.request.GET
            if not getattr(settings, "CONTENT_CREATE_ON_404", False):
                opt_out = True
            is_media = settings.MEDIA_URL and settings.MEDIA_URL in self.request.path
            is_static = settings.STATIC_URL and settings.STATIC_URL in self.request.path
            if self.request.user.is_staff and not (opt_out or is_media or is_static):
                retval = Page(
                    title="Page",
                    content="Create a new page by editing this text",
                    url=url
                )
            else:
                raise Http404("Page not found")
        return retval

    def get_template_names(self):
        if self.object.template_name:
            return [self.object.template_name, "content/page.html"]
        return ["content/page.html"]

    def get_context_data(self, **kwargs):

        self.object.title = mark_safe(self.object.title)
        self.object.content = mark_safe(self.object.content)
        return super(PageDetailView, self).get_context_data(
            page=self.object,
            **kwargs
        )


page_detail = PageDetailView.as_view()


class PageUpdateView(UpdateView):
    model = Page
    form_class = modelform_factory(model=Page, fields=['content'])

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PageUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        if self.kwargs['pk'] == "new":
            return Page(
                title="Page",
                content="",
                url=self.request.POST['url']
            )
        else:
            return super(PageUpdateView, self).get_object()

    def form_valid(self, form):
        if self.request.is_ajax():
            page = form.save()
            return HttpResponse(json.dumps({
                "page_id": page.id,
                "status": "OK"
            }), content_type="x-application/json")

        return super(PageUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return HttpResponse(json.dumps({
                "status": "Error: {}".format(", ".join(form.errors))
            }), content_type="x-application/json")

        return super(PageUpdateView, self).form_valid(form)
