from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Count, Sum
from datetime import timedelta
from .models import Booking, Hotel
from django.contrib.auth.models import User

@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    
    today = now().date()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)

    bookings_last_week = Booking.objects.filter(created_at__gte=last_week).count()
    bookings_last_month = Booking.objects.filter(created_at__gte=last_month).count()

    top_hotels = (
        Hotel.objects.annotate(total_bookings=Count('booking'))
        .order_by('-total_bookings')[:5]
        .values('name', 'total_bookings')
    )

    top_users = (
        User.objects.annotate(total_bookings=Count('booking'))
        .order_by('-total_bookings')[:5]
        .values('username', 'total_bookings')
    )
    sales_current_month = (
        Booking.objects.filter(created_at__month=today.month)
        .aggregate(total=Sum('hotel__price'))['total'] or 0
    )
    sales_prev_month = (
        Booking.objects.filter(created_at__month=(today.month - 1))
        .aggregate(total=Sum('hotel__price'))['total'] or 0
    )
    sales_current_year = (
        Booking.objects.filter(created_at__year=today.year)
        .aggregate(total=Sum('hotel__price'))['total'] or 0
    )

    return Response({
        "bookings_last_week": bookings_last_week,
        "bookings_last_month": bookings_last_month,
        "top_hotels": list(top_hotels),
        "top_users": list(top_users),
        "sales_current_month": sales_current_month,
        "sales_prev_month": sales_prev_month,
        "sales_current_year": sales_current_year,
    })
