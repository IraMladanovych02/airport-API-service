import pathlib
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from app import settings


class Facility(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "facilities"

    def __str__(self):
        return self.name


def image_path(instance, filename) -> pathlib.Path:
    filename = f"{slugify(instance.info)}--{uuid.uuid4()}" + pathlib.Path(filename).suffix
    return pathlib.Path("upload/planes/") / pathlib.Path(filename)


class Plane(models.Model):
    info = models.CharField(max_length=255, null=True)
    num_seats = models.IntegerField()
    facilities = models.ManyToManyField("Facility", related_name="plays")
    image = models.ImageField(null=True, upload_to=image_path)

    @property
    def is_small_or_big(self):
        return self.num_seats <= 50

    def __str__(self):
        return self.info



class Trip(models.Model):
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure = models.DateTimeField()
    plane = models.ForeignKey("Plane", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.source} - {self.destination} ({self.departure})"


class Ticket(models.Model):
    seat = models.IntegerField()
    trip = models.ForeignKey("Trip", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("trip", "seat")
        ordering = ("seat",)

    def __str__(self):
        return f"{self.trip} - (seat: {self.seat})"

    @staticmethod
    def validate_seat(seat: int, num_seats: int):
        if not (1 <= seat <= num_seats):
            raise ValidationError(
                {
                    "seat": f"Seat must be in the range [1, {num_seats}], not {seat}."
                }
            )

    def clean(self):
        Ticket.validate_seat(self.seat, self.trip.plane.num_seats)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Ticket, self).save(*args, **kwargs)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.created_at)
