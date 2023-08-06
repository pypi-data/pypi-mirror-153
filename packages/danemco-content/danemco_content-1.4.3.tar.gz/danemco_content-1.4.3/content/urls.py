from django.conf.urls import include, url

from .views import PageUpdateView


defaultpatterns = [('^', include('content.urls'))]


urlpatterns = [
    url(
        r'^(?P<pk>\d+|new)/save/',
        PageUpdateView.as_view(),
        name="content-save"
    )
]
