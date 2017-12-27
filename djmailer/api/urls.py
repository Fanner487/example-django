from django.conf.urls import url
from rest_framework.routers import SimpleRouter

# from .views import SubscriberView
from .views import SubscriberViewSet
# from .views import hello_world

router = SimpleRouter()
router.register("subscribers", SubscriberViewSet)

urlpatterns = router.urls

# urlpatterns = [
#     # url(r'^hello', hello_world, name="hello_world")
#     url(r'^hello', SubscriberView.as_view(), name="subsriber")
#     # url(r'^hello', hello_world, name="hello_world")
# ]