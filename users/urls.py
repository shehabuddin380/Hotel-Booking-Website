from django.urls import path
from .views import RegisterView,ActivateAccount

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    # path('profile/', ProfileView.as_view(), name='profile'), 

]
