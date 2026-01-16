
from django.urls import path
from .views import RegisterView,ActivateAccount
from .views import LoginView, RegisterView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("logout/", LogoutView.as_view()),

]
