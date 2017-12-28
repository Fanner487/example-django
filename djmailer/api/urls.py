from django.conf.urls import url
from rest_framework.routers import SimpleRouter

# from .views import SubscriberView
from .views import SubscriberViewSet
from .views import login, register
# from .views import hello_world

router = SimpleRouter()
router.register("subscribers", SubscriberViewSet)



urlpatterns = [
    url(r'^login', login, name="login")
    # url(r'^register', register, name="register")
    # url(r'^hello', SubscriberView.as_view(), name="subsriber")
    # url(r'^hello', hello_world, name="hello_world")
]

urlpatterns += router.urls
