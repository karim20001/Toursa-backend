from rest_framework import serializers
from .models import Tour

class TourSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'origin_city', 'origin_country',
            'destination_city', 'destination_country', 'start_date',
            'end_date', 'days_of_tour', 'capacity', 'remaining_capacity',
            'transportation_type', 'price', 'price_off', 'discounted_price',
            'description', 'is_available', 'image'
        ]

    def get_discounted_price(self, obj):
        """Calculate the discounted price based on the percentage discount."""
        if obj.price_off and obj.price_off > 0:  # If a discount is set
            discount = (obj.price * obj.price_off) / 100  # Calculate discount amount
            return obj.price - discount  # Subtract discount from the original price
        return obj.price  # Return original price if no discount

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.cover_photo:
            return request.build_absolute_uri(obj.cover_photo.url) if request else obj.cover_photo.url
        return None