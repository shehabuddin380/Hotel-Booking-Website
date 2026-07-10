from rest_framework import serializers
from .models import Hotel, Booking, Review, Room


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


class RoomSerializer(serializers.ModelSerializer):
    hotel_name = serializers.ReadOnlyField(source='hotel.name')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id',
            'hotel',
            'hotel_name',
            'name',
            'description',
            'price',
            'image',
        ]

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None