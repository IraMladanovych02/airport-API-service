from django.db import transaction
from rest_framework import serializers

from airport.models import Plane, Trip, Service, Ticket, Order


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("id", "name")


class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = ("id", "info", "num_seats", "services", "is_small_or_big")


class PlaneImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plane
        fields = ("id", "image")


class PlaneListSerializer(PlaneSerializer):
    services = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )


class PlaneRetrieveSerializer(PlaneSerializer):
    services = ServiceSerializer(many=True, read_only=True)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "seat", "trip")

    def validate(self, attrs):
        seat = attrs.get("seat")
        trip = attrs.get("trip")
        if not seat or not trip:
            raise serializers.ValidationError("Seat and trip are required.")
        Ticket.validate_seat(seat, trip.plane.num_seats)
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ("id", "source", "destination", "departure", "plane")


class TripListSerializer(serializers.ModelSerializer):
    plane_info = serializers.CharField(source="plane.info", read_only=True)
    plane_num_seats = serializers.IntegerField(source="plane.num_seats", read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Trip
        fields = (
            "id",
            "source",
            "destination",
            "departure",
            "plane_info",
            "plane_num_seats",
            "tickets_available",
        )


class TripRetrieveSerializer(TripSerializer):
    plane = PlaneRetrieveSerializer(many=False, read_only=True)
    taken_seats = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="seat", source="tickets"
    )
    fields = ("id", "source", "destination", "departure", "plane", "taken_seats")


class TicketListSerializer(TicketSerializer):
    trip = TripListSerializer(read_only=True)


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
