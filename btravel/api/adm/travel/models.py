from django.db import models

class Destination(models.Model):
    city = models.CharField(max_length=100)
    properties = models.CharField(max_length=20, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    hover_text = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    travellers = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    number_of_properties = models.CharField(max_length=20, blank=True, null=True)
    col_class = models.CharField(max_length=50, blank=True, null=True)
    delay_animation = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.city or self.title or self.name or ""

class Hotel(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    tag = models.CharField(max_length=50, blank=True, null=True)
    img = models.CharField(max_length=255)
    slide_img = models.JSONField(default=list)
    ratings = models.CharField(max_length=10)
    number_of_reviews = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    city = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    delay_animation = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.title

class Rental(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    tag = models.CharField(max_length=50, blank=True, null=True)
    slide_img = models.JSONField(default=list)
    ratings = models.CharField(max_length=10)
    number_of_reviews = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    guest = models.CharField(max_length=10)
    bedroom = models.CharField(max_length=10)
    bed = models.CharField(max_length=10)
    delay_animation = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.title

class TourCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    tour_number = models.CharField(max_length=10)
    price = models.CharField(max_length=20)
    delay_animation = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Tour Categories"
    
    def __str__(self):
        return self.name

class Tour(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    tag = models.CharField(max_length=50, blank=True, null=True)
    slide_img = models.JSONField(default=list)
    duration = models.CharField(max_length=10)
    number_of_reviews = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    tour_type = models.CharField(max_length=50)
    delay_animation = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.title

class Car(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    tag = models.CharField(max_length=50, blank=True, null=True)
    slide_img = models.JSONField(default=list)
    type = models.CharField(max_length=50)
    ratings = models.CharField(max_length=10)
    number_of_reviews = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    seat = models.CharField(max_length=10)
    luggage = models.CharField(max_length=10)
    transmission = models.CharField(max_length=20)
    speed = models.CharField(max_length=50)
    delay_animation = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.title 