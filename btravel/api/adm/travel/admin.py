from django.contrib import admin
from .models import Destination, Hotel, Rental, TourCategory, Tour, Car

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'title', 'name', 'region', 'location')
    search_fields = ('city', 'title', 'name', 'region', 'location')
    list_filter = ('region',)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'price', 'city', 'category', 'ratings')
    search_fields = ('title', 'location', 'city')
    list_filter = ('city', 'category')

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'price', 'bedroom', 'guest')
    search_fields = ('title', 'location')
    list_filter = ('bedroom', 'guest')

@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tour_number', 'price')
    search_fields = ('name',)

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'duration', 'price', 'tour_type')
    search_fields = ('title', 'location', 'tour_type')
    list_filter = ('tour_type',)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'type', 'price', 'transmission')
    search_fields = ('title', 'location', 'type')
    list_filter = ('type', 'transmission') 