from django.conf.urls import url

from .views import HelloWorldView

urlpatterns = [
    # url(r'^hello', hello_world, name="hello_world")
    url(r'^hello', HelloWorldView.as_view(), name="hello_world")
]