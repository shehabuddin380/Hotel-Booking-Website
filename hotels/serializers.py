from rest_framework import serializers
from .models import Hotel, Booking, Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = ['id', 'user', 'hotel', 'rating', 'comment']


class HotelDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Hotel
        fields = [
            'id',
            'name',
            'location',
            'description',
            'address',
            'owner',
            'reviews'
        ]


class HotelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Hotel
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    hotel_name = serializers.ReadOnlyField(source='hotel.name')

    class Meta:
        model = Booking
        fields = [
            'id',
            'user',
            'hotel',
            'hotel_name',
            'check_in',
            'check_out',
            'is_confirmed',
            'booked_at'
        ]