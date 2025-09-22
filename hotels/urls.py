from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, BookingViewSet, ReviewViewSet, HotelDetailView
from .views_admin import dashboard_stats

router = DefaultRouter()
router.register('hotels', HotelViewSet)
router.register('bookings', BookingViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/dashboard/', dashboard_stats, name='dashboard-stats'),
    path('hotels/<int:pk>/detail/', HotelDetailView.as_view(), name='hotel-detail'),
]
