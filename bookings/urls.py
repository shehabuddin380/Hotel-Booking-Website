from django.urls import path
from .views import payment_view, payment_success

urlpatterns = [
    path("payment/", payment_view),
    path("payment/success/", payment_success),
]