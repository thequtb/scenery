from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Bookable, Review
from .serializers import (
    BookableSerializer, 
    BookableDetailSerializer, 
    ReviewSerializer,
    SearchSerializer
)
from .utils import get_embedding
from django.contrib.postgres.search import SearchVector, SearchQuery
from pgvector.django import L2Distance
import numpy as np

class BookableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bookable.objects.all()
    serializer_class = BookableSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookableDetailSerializer
        return BookableSerializer
    
    def get_queryset(self):
        queryset = Bookable.objects.all()
        
        # Filter by type if provided
        bookable_type = self.request.query_params.get('type', None)
        if bookable_type:
            queryset = queryset.filter(type=bookable_type)
            
        # Filter by destination if provided
        destination = self.request.query_params.get('destination', None)
        if destination:
            queryset = queryset.filter(destination_id=destination)
            
        return queryset
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """
        Search bookables using semantic search with vector embeddings.
        
        Args:
            message (str): The text query to find semantically similar bookables
            
        Returns:
            Paginated list of bookables ordered by semantic similarity
        """
        # Validate input using dedicated SearchSerializer
        search_serializer = SearchSerializer(data=request.data)
        if not search_serializer.is_valid():
            return Response(search_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated message
        message = search_serializer.validated_data['message']
        
        # Generate embedding for the search query
        query_embedding = get_embedding(message)
        
        # Set up pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        
        # Search for similar bookables using vector distance
        # Lower distance means higher similarity
        bookables = Bookable.objects.annotate(
            distance=L2Distance('embedding', query_embedding)
        ).order_by('distance')
        
        # Apply pagination
        paginated_bookables = paginator.paginate_queryset(bookables, request)
        serializer = self.get_serializer(paginated_bookables, many=True)
        
        return paginator.get_paginated_response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Review.objects.all()
        
        # Filter by bookable if provided
        bookable_id = self.request.query_params.get('bookable', None)
        if bookable_id:
            queryset = queryset.filter(bookable_id=bookable_id)
            
        # Filter by user if provided
        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
            
        return queryset
    
    def perform_create(self, serializer):
        # Link the review to the current user
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Endpoint to retrieve the current user's reviews."""
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
            
        reviews = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)