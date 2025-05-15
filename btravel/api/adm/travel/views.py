from django.shortcuts import render
from rest_framework import viewsets
from .models import Destination, Hotel, Rental, TourCategory, Tour, Car
from .serializers import (
    DestinationSerializer, HotelSerializer, 
    RentalSerializer, TourCategorySerializer, 
    TourSerializer, CarSerializer
)

# No views needed 

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

class TourCategoryViewSet(viewsets.ModelViewSet):
    queryset = TourCategory.objects.all()
    serializer_class = TourCategorySerializer

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer 