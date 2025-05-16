from django.contrib import admin
from .models import Destination, Bookable, BookableImage, Collection, CollectionItem, Review
from django_svelte_jsoneditor.widgets import SvelteJSONEditorWidget
from django.db.models import JSONField

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class BookableImageInline(admin.TabularInline):
    model = BookableImage
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Bookable)
class BookableAdmin(admin.ModelAdmin):
    list_display = ['title', 'destination', 'type']
    list_filter = ['type', 'destination']
    search_fields = ['title']
    inlines = [BookableImageInline, ReviewInline]
    formfield_overrides = {
        JSONField: {'widget': SvelteJSONEditorWidget},
    }

@admin.register(BookableImage)
class BookableImageAdmin(admin.ModelAdmin):
    list_display = ['bookable', 'image', 'is_thumbnail']
    list_filter = ['is_thumbnail', 'bookable']

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']

@admin.register(CollectionItem)
class CollectionItemAdmin(admin.ModelAdmin):
    list_display = ['collection', 'bookable']
    list_filter = ['collection']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['bookable', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['bookable__title', 'user__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
