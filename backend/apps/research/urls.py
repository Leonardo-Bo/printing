from django.urls import path, include
from rest_framework import urlpatterns

from rest_framework.routers import DefaultRouter

from .views import ResearchFieldViewSet

router = DefaultRouter()
router.register('research', ResearchFieldViewSet, basename='research')

urlpatterns = [
    path('', include(router.urls)),
]