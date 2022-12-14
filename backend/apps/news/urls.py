from django.urls import path, include
from rest_framework import urlpatterns

from rest_framework.routers import DefaultRouter

from .views import NewsViewSet


router = DefaultRouter()
router.register('news', NewsViewSet, basename='news')

urlpatterns = [
    path('', include(router.urls)),
]