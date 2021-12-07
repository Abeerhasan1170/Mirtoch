"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import allauth
from djangoTwitter.sitemap import StaticSitemap, PublicationSitemap #,ProfileSitemap
from django.contrib.sitemaps.views import sitemap
import notifications.urls
from django.conf import settings
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)



sitemaps = {
    'pages': StaticSitemap,
    'publication': PublicationSitemap,
    # 'profiles': ProfileSitemap
}


admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # new
    path('', include(('djangoTwitter.urls'), namespace='mirtoch')),  # new
    path('inbox/notifications/',
         include(notifications.urls, namespace='notifications')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('timelines/', include(('timeline.urls'), namespace='timeline-urls')),

]


handler400 = 'djangoTwitter.views.bad_request'
handler403 = 'djangoTwitter.views.permission_denied'
handler404 = 'djangoTwitter.views.page_not_found'
handler500 = 'djangoTwitter.views.server_error'
