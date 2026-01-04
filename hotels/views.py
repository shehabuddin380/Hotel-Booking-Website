from rest_framework import viewsets, permissions, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.core.mail import send_mail
from django.db import transaction
from .models import Hotel, Booking, Review
from .serializers import HotelSerializer, BookingSerializer, ReviewSerializer, HotelDetailSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from .models import Order
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Hotel ViewSet
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.AllowAny]  # সবাই দেখতে পারবে


# Booking ViewSet (balance check + confirmation email + atomic + overlap check)
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        hotel = serializer.validated_data["hotel"]
        check_in = serializer.validated_data["check_in"]
        check_out = serializer.validated_data["check_out"]

        if check_in >= check_out:
            raise ValidationError("Check-out date must be after check-in date.")

        # Overlap check
        overlap = Booking.objects.filter(
            hotel=hotel,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists()
        if overlap:
            raise ValidationError("This hotel is already booked for the selected dates.")

        price = hotel.price

        with transaction.atomic():
            user.refresh_from_db()
            if user.balance < price:
                raise ValidationError("Insufficient balance to book this hotel.")

            # Deduct balance
            user.balance -= price
            user.save()

            # Save booking
            booking = serializer.save(user=user)

            # Send confirmation email
            send_mail(
                subject="Booking Confirmation",
                message=f"Dear {user.first_name}, your booking for {booking.hotel.name} is confirmed!",
                from_email="no-reply@hotelbooking.com",
                recipient_list=[user.email],
            )


# Review ViewSet
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        hotel = serializer.validated_data["hotel"]

        # Check if user has booking for this hotel
        if not Booking.objects.filter(user=user, hotel=hotel).exists():
            raise ValidationError("You can only review hotels you have booked.")

        serializer.save(user=user)

    def get_queryset(self):
        hotel_id = self.request.query_params.get("hotel")
        if hotel_id:
            return Review.objects.filter(hotel_id=hotel_id)
        return Review.objects.all()


# Hotel Detail View (with reviews, photos)
class HotelDetailView(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['POST'])
def create_order(request):
    data = request.data
    order = Order.objects.create(
        name=data['name'],
        phone=data['phone'],
        address=data['address'],
        room_id=data['room_id'],
        amount=3500
    )
    return Response({"order_id": order.id})

@csrf_exempt
def ssl_payment(request):
    data = {
        "store_id": "your_store_id",
        "store_passwd": "your_pass",
        "total_amount": 3500,
        "currency": "BDT",
        "success_url": "http://localhost:5173/success",
        "fail_url": "http://localhost:5173/fail",
    }

    return JsonResponse(data)