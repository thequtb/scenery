from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookableViewSet, ReviewViewSet


app_name = 'travel'

router = DefaultRouter()
router.register(r'bookables', BookableViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
] 