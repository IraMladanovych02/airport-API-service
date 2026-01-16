from django.contrib import admin

from airport.models import Plane, Service, Order, Trip, Ticket


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


@admin.register(Plane)
class PlaneAdmin(admin.ModelAdmin):
    search_fields = ("info",)
    list_display = ("num_seats", "info")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ("name", )


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    search_fields = ("source", "destination",)
    list_display = ("source", "destination", "departure", "plane",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    search_fields = ("seat",)
    list_display = ("seat", "trip", "order")
