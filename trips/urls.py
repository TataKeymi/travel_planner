from django.urls import path, include
from rest_framework.routers import DefaultRouter
from trips.views import TravelProjectViewSet, ProjectPlaceViewSet

router = DefaultRouter()
router.register("projects", TravelProjectViewSet)
router.register("places", ProjectPlaceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
