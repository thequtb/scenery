from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DestinationViewSet, HotelViewSet, RentalViewSet,
    TourCategoryViewSet, TourViewSet, CarViewSet
)

app_name = 'travel'

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'rentals', RentalViewSet)
router.register(r'tour-categories', TourCategoryViewSet)
router.register(r'tours', TourViewSet)
router.register(r'cars', CarViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
] 