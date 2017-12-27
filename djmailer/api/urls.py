from django.conf.urls import url

from .views import SubscriberView
# from .views import hello_world

urlpatterns = [
    # url(r'^hello', hello_world, name="hello_world")
    url(r'^hello', SubscriberView.as_view(), name="subsriber")
    # url(r'^hello', hello_world, name="hello_world")
]