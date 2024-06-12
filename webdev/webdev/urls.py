"""
URL configuration for webdev project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from django.conf import settings

from post.sitemaps import PostSitemap
from post.views import page_not_found, access_is_denied
from .spectacular import urlpatterns as doc_urls
# from .yasg import urlpatterns as doc_urls


sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/',
         admin.site.urls),
    path('',
         include('post.urls')),
    path('account/',
         include('account.urls',
                 namespace='account')),
    path('summernote/',
         include('django_summernote.urls')),
    path('api-auth/',
         include('rest_framework.urls')),
    path('auth/',
         include('djoser.urls')),
    path('auth/',
         include('djoser.urls.authtoken')),
    path('api/v1/',
         include('api.urls',
                 namespace='api')),
    path('social-auth/',
         include('social_django.urls',
                 namespace='social')),
    path("__debug__/",
         include("debug_toolbar.urls")),
    path('sitemap.xml',
         cache_page(86400)(sitemap),
         {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

handler403 = access_is_denied
handler404 = page_not_found

urlpatterns += doc_urls

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Webdev.com"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
