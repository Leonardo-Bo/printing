from django.urls import path, include
from rest_framework import urlpatterns

from rest_framework.routers import DefaultRouter

from .views import (ImageResearchFieldViewSet, CoverResearchFieldViewSet, 
                    ImagePersonViewSet, CoverPersonViewSet, PicProfilePersonViewSet,
                    ImageNewsViewSet, CoverNewsViewSet,
                    CoverCarouselViewSet, 
                    CoverToolViewSet)


router = DefaultRouter()
router.register('research-images', ImageResearchFieldViewSet, basename='research_images')
router.register('research-cover', CoverResearchFieldViewSet, basename='research_cover')
router.register('person-images', ImagePersonViewSet, basename='person_images')
router.register('person-cover', CoverPersonViewSet, basename='person_cover')
router.register('person-pic', PicProfilePersonViewSet, basename='person_pic')
router.register('news-images', ImageNewsViewSet, basename='news_images')
router.register('news-cover', CoverNewsViewSet, basename='news_cover')
router.register('carousel-cover', CoverCarouselViewSet, basename='carousel_cover')
router.register('tool-cover', CoverToolViewSet, basename='tool_cover')


urlpatterns = [
    path('', include(router.urls)),
]