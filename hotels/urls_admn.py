from django.urls import path
from .views_admin import dashboard_stats

urlpatterns = [
    path('admin/dashboard/', dashboard_stats, name='admin-dashboard'),
]
