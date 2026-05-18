from django.urls import path
from .views import payment

urlpatterns = [
    # future payment endpoints
    path("payment/", payment),
    path("pay/", payment),
    
]
