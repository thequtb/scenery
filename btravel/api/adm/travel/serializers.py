from rest_framework import serializers
from .models import Bookable, BookableImage, Review
from django.db.models import Avg

class BookableImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookableImage
        fields = ['id', 'image', 'is_thumbnail']

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'bookable', 'user', 'username', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_username(self, obj):
        return obj.user.username

class BookableSerializer(serializers.ModelSerializer):
    images = BookableImageSerializer(source='bookableimage_set', many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Bookable
        fields = ['id', 'title', 'destination', 'type', 'options', 'images', 'avg_rating', 'review_count']
    
    def get_avg_rating(self, obj):
        avg = obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg, 1) if avg else 0
    
    def get_review_count(self, obj):
        return obj.reviews.count()

class BookableDetailSerializer(BookableSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta(BookableSerializer.Meta):
        fields = BookableSerializer.Meta.fields + ['reviews']

class SearchSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
