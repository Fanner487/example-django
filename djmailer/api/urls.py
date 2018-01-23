from django.conf.urls import url
from rest_framework.routers import SimpleRouter

# from .views import SubscriberView
from .views import SubscriberViewSet, EventViewSet
from .views import login, register, view_subscribers
# from .views import hello_world

router = SimpleRouter()
router.register("subscribers", SubscriberViewSet)
router.register("events", EventViewSet)



urlpatterns = [
    url(r'^login', login, name="login"),
    url(r'^register', register, name="register"),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', view_subscribers, name="view_subscribers"),
    # url(r'^register', register, name="register")
    # url(r'^hello', SubscriberView.as_view(), name="subsriber")
    # url(r'^hello', hello_world, name="hello_world")
]

urlpatterns += router.urls
