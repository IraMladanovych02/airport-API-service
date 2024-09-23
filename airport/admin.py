from django.contrib import admin

from airport.models import Plane, Facility, Order, Trip, Ticket


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(Plane)
admin.site.register(Facility)
admin.site.register(Trip)
admin.site.register(Ticket)
