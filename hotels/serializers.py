from rest_framework import serializers
from .models import Hotel, Booking, Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = ['id', 'user', 'hotel', 'rating', 'comment', 'created_at']

class HotelDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'price', 'photo', 'reviews']

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    hotel_name = serializers.ReadOnlyField(source='hotel.name')

    class Meta:
        model = Booking
        fields = ['id', 'user', 'hotel', 'hotel_name', 'check_in', 'check_out', 'is_confirmed', 'booked_at']
