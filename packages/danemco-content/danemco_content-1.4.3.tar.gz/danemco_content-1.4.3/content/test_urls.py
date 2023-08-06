from django.conf.urls import url

from .views import page_detail

urlpatterns = [
    url(r'(.*)', page_detail)
]
