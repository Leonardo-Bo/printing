from django.urls import path, include
from rest_framework import urlpatterns

from rest_framework.routers import DefaultRouter

from .views import PublicationPDFViewSet, PersonCVPDFViewSet


router = DefaultRouter()
router.register('publication-files', PublicationPDFViewSet, basename='publication_files')
router.register('people-files', PersonCVPDFViewSet, basename='person_files')


urlpatterns = [
    path('', include(router.urls)),
]