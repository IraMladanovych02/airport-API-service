from django.db.models import Count, F
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from airport.models import Plane, Trip, Facility, Order
from airport.permissions import IsAdminOrIsAuthenticatedOrReadOnly
from airport.serializers import (
    PlaneSerializer,
    TripSerializer,
    TripListSerializer,
    PlaneListSerializer,
    FacilitySerializer,
    PlaneRetrieveSerializer,
    TripRetrieveSerializer,
    OrderSerializer, PlaneImageSerializer,
)


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminOrIsAuthenticatedOrReadOnly,)


class PlaneViewSet(viewsets.ModelViewSet):
    queryset = Plane.objects.all()
    serializer_class = PlaneListSerializer

    @staticmethod
    def _params_to_ints(query_string):
        return [int(str_id) for str_id in query_string.split(",")]

    def get_serializer_class(self):
        if self.action == "list":
            return PlaneListSerializer
        elif self.action == "retrieve":
            return PlaneRetrieveSerializer
        elif self.action == "upload-image":
            return PlaneImageSerializer
        return PlaneSerializer

    def get_queryset(self):
        queryset = self.queryset
        facilities = self.request.query_params.get("facilities")
        if facilities:
            facilities = self._params_to_ints(facilities)
            queryset = queryset.filter(facilities__id__in=facilities)
        if self.action in ("list", "retrieve"):
            return queryset.prefetch_related("facilities")
        return queryset.distinct()

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminUser,],
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        plane = self.get_object()
        serializer = self.get_serializer(plane, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all().select_related()
    serializer_class = TripSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer
        elif self.action == "retrieve":
            return TripRetrieveSerializer
        return TripSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in "list":
            queryset = (
                queryset
                .select_related()
                .annotate(tickets_available=F("plane__num_seats") - Count("tickets"))
            )
        elif self.action in "retrieve":
            queryset = queryset.select_related()

        return queryset.order_by("id")


class OrderSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderSetPagination

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        if self.action == "list":
            queryset = queryset.prefetch_related("tickets__trip__plane")
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "list":
            serializer = OrderSerializer

        return serializer
