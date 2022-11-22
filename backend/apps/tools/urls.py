from django.urls import path, include
from rest_framework import urlpatterns

from rest_framework.routers import DefaultRouter

from .views import ToolViewSet

router = DefaultRouter()
router.register('tools', ToolViewSet, basename='tools')

urlpatterns = [
    path('', include(router.urls)),
]