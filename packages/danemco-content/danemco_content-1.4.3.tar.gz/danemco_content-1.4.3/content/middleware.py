from django.conf import settings
from django.http import Http404, HttpResponseRedirect

from .views import page_detail


class PageFallbackMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        return self.process_response(request, self.get_response(request))

    def process_response(self, request, response):
        if response.status_code != 404:
            # No need to check for a flatpage for non-404 responses.
            return response
        try:
            if request.method == "GET":
                response = page_detail(request, url=request.path_info)

                # if not isinstance(response, HttpResponseRedirect):
                #     response.render()

                return response
            else:
                return response
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except Exception:
            if settings.DEBUG:
                raise
            return response
