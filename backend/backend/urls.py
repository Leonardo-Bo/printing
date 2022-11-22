"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path('signup/', TemplateView.as_view(template_name="index.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('account/', TemplateView.as_view(template_name="index.html")),
    path('reset-password/', TemplateView.as_view(template_name="index.html")),
    path('reset-password/confirm/<str:uid>/<str:token>/', TemplateView.as_view(template_name="index.html")),

    path('settings/', TemplateView.as_view(template_name="index.html")),

    path('settings/research-fields/', TemplateView.as_view(template_name="index.html")),
    path('settings/research-fields/add', TemplateView.as_view(template_name="index.html")),
    path('settings/research-fields/edit/<str:slug>', TemplateView.as_view(template_name="index.html")),

    path('settings/people/', TemplateView.as_view(template_name="index.html")),
    path('settings/people/add', TemplateView.as_view(template_name="index.html")),
    path('settings/people/edit/<str:slug>', TemplateView.as_view(template_name="index.html")),

    path('settings/publications/', TemplateView.as_view(template_name="index.html")),
    path('settings/publications/add', TemplateView.as_view(template_name="index.html")),
    path('settings/publications/edit/<int:id>', TemplateView.as_view(template_name="index.html")),

    path('settings/news/', TemplateView.as_view(template_name="index.html")),
    path('settings/news/add', TemplateView.as_view(template_name="index.html")),
    path('settings/news/edit/<str:slug>', TemplateView.as_view(template_name="index.html")),

    path('settings/carousel/', TemplateView.as_view(template_name="index.html")),
    path('settings/carousel/add', TemplateView.as_view(template_name="index.html")),
    path('settings/carousel/edit/<int:pk>', TemplateView.as_view(template_name="index.html")),

    path('settings/tools/', TemplateView.as_view(template_name="index.html")),
    path('settings/tools/add', TemplateView.as_view(template_name="index.html")),
    path('settings/tools/edit/<str:slug>', TemplateView.as_view(template_name="index.html")),


    path('research-fields/', TemplateView.as_view(template_name="index.html")),
    path('research-fields/<str:slug>', TemplateView.as_view(template_name="index.html")),

    path('people/', TemplateView.as_view(template_name="index.html")),
    path('people/<str:slug>', TemplateView.as_view(template_name="index.html")),

    path('publications/', TemplateView.as_view(template_name="index.html")),

    path('news/', TemplateView.as_view(template_name="index.html")),
    path('news/<str:slug>', TemplateView.as_view(template_name="index.html")),

    path('tools/', TemplateView.as_view(template_name="index.html")),
    path('contacts/', TemplateView.as_view(template_name="index.html")),


    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),

    path("api/v1/", include("apps.crossuser.urls")),
    path("api/v1/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.research.urls")),
    path("api/v1/", include("apps.publications.urls")),
    path("api/v1/", include("apps.news.urls")),
    path("api/v1/", include("apps.people.urls")),
    path("api/v1/", include("apps.carousel.urls")),
    path("api/v1/", include("apps.tools.urls")),

    path("api/v1/", include("apps.images.urls")),
    path("api/v1/", include("apps.files.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
