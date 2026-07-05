from django.contrib.auth import get_user_model, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer
from hotels.models import Room, Order

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(self.request).domain
        activation_link = f"http://{domain}/api/users/activate/{uid}/{token}/"
        send_mail(
            "Activate your HotelLux Account",
            f"Hello {user.email}, Click here to activate your account:\n{activation_link}",
            "no-reply@hotellux.com",
            [user.email],
            fail_silently=True,
        )

class ActivateAccount(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            return Response({"error": "Invalid activation link"}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully!"})

        return Response({"error": "Activation failed"}, status=400)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=401)

    if not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=401)

    if not user.is_active:
        return Response({"error": "Account not activated. Please check your email."}, status=403)

    refresh = RefreshToken.for_user(user)
    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "email": user.email
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"message": "Logout successful"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    total_rooms = Room.objects.count()
    booked_room_ids = Order.objects.values_list('room_id', flat=True).distinct()
    booked_rooms = booked_room_ids.count()
    available_rooms = total_rooms - booked_rooms

    my_orders = Order.objects.filter(name=request.user.email).select_related('room')
    bookings_data = [
        {
            "room_name": order.room.name,
            "amount": order.amount,
            "room_id": order.room.id,
        }
        for order in my_orders
    ]

    available_rooms_data = list(
        Room.objects.exclude(id__in=booked_room_ids).values('id', 'name', 'price', 'description')
    )

    return Response({
        "total_rooms": total_rooms,
        "booked_rooms": booked_rooms,
        "available_rooms": available_rooms,
        "my_bookings": bookings_data,
        "available_rooms_list": available_rooms_data,
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    return Response({
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_admin": user.is_admin,
        "phone_number": user.phone_number,
        "address": user.address,
        "balance": user.balance,
    })