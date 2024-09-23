from django.urls import path, include
from rest_framework import routers

from airport.views import (
    PlaneViewSet,
    TripViewSet,
    FacilityViewSet,
    OrderViewSet,
)

app_name = "theatre"

router = routers.DefaultRouter()

router.register("planes", PlaneViewSet)
router.register("trips", TripViewSet)
router.register("facilities", FacilityViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
