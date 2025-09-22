from django.contrib.auth import get_user_model
User =get_user_model()
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout

from .serializers import UserRegisterSerializer

# ---------------- Registration ----------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)  # inactive until email confirm
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(self.request).domain
        activation_link = f"http://{domain}/api/users/activate/{uid}/{token}/"

        try:
            send_mail(
                subject="Activate your account",
                message=f"Hi {user.username}, please click the link to activate your account: {activation_link}",
                from_email="no-reply@hotelbooking.com",
                recipient_list=[user.email],
                fail_silently=False,
            )
        except BadHeaderError:
            return Response({"error": "Invalid header found."}, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Activation ----------------
class ActivateAccount(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Login ----------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                return Response({"error": "Account is not activated yet."}, status=status.HTTP_403_FORBIDDEN)

            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Logout ----------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()  # remove token
        except Exception:
            pass
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
