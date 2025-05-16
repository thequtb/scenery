from django.db import models
from pgvector.django import VectorField
from .utils import generate_bookable_embedding, generate_collection_embedding
import numpy as np
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Destination(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Bookable(models.Model):
    class BookableType(models.TextChoices):
        HOTEL = 'hotel'
        APARTMENT = 'apartment'
        ACTIVITY = 'activity'
        TOUR = 'tour'
        CAR = 'car'
        OTHER = 'other'

    title = models.CharField(max_length=255)
    destination = models.ForeignKey('Destination', on_delete=models.PROTECT)
    type = models.CharField(max_length=255, choices=BookableType.choices)
    options = models.JSONField(blank=True, null=True, default=dict)
    embedding = VectorField(dimensions=1536, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Generate embedding before saving
        destination_name = self.destination.name if self.destination_id else ""
        embedding_vector = generate_bookable_embedding(
            self.title,
            self.type,
            destination_name,
            self.options
        )
        self.embedding = embedding_vector
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BookableImage(models.Model):
    bookable = models.ForeignKey('Bookable', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/')
    is_thumbnail = models.BooleanField(default=False)

    def __str__(self):
        return self.image.url
    

class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    embedding = VectorField(dimensions=1536, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate embedding from description
        embedding_vector = generate_collection_embedding(self.description)
        self.embedding = embedding_vector
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CollectionItem(models.Model):
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)
    bookable = models.ForeignKey('Bookable', on_delete=models.CASCADE)


class Review(models.Model):
    bookable = models.ForeignKey('Bookable', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('bookable', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s review for {self.bookable.title}"

