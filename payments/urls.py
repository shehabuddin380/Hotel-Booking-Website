from django.urls import path
from . import views

from .views import payment

urlpatterns = [
    # future payment endpoints
    path("payment/", payment),
    path("pay/", payment),

]
