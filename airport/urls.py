from django.urls import path, include
from rest_framework import routers

from airport.views import (
    PlaneViewSet,
    TripViewSet,
    ServiceViewSet,
    OrderViewSet,
)

app_name = "airport"

router = routers.DefaultRouter()

router.register("planes", PlaneViewSet)
router.register("trips", TripViewSet)
router.register("services", ServiceViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
