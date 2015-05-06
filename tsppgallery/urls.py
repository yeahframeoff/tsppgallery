from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = (
    url(r'^', include('gallery.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT
    }),
)
