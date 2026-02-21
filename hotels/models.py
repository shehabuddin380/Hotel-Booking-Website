from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Hotel(models.Model):

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_hotels"
    )

    def __str__(self):
        return self.name
    


class Room(models.Model):

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="rooms",
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    description = models.TextField()

    price = models.PositiveIntegerField()

    image = models.ImageField(
        upload_to="rooms/",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.hotel})"



class Booking(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    check_in = models.DateField()
    check_out = models.DateField()

    is_confirmed = models.BooleanField(
        default=False
    )

    booked_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user} booked {self.hotel}"



class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.hotel} ({self.rating})"



class Order(models.Model):

    name = models.CharField(max_length=100)

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField()

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    amount = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.room}"
