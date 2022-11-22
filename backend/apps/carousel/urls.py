from django.urls import path, include
from rest_framework import urlpatterns

from rest_framework.routers import DefaultRouter

from .views import CarouselViewSet


router = DefaultRouter()
router.register('carousel', CarouselViewSet, basename='carousel')

urlpatterns = [
    path('', include(router.urls)),
]