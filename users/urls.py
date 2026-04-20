from django.urls import path
from .views import RegisterView, ActivateAccount, login_view, logout_view, dashboard_view

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("activate/<uidb64>/<token>/", ActivateAccount.as_view()),
    path("login/", login_view),
    path("logout/", logout_view),
    path("dashboard/", dashboard_view),
]