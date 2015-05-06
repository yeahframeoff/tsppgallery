from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as authviews
from . import views

urlpatterns = (
    url(r'^$', views.main, name='mainpage'),
    url(r'^login/?$', authviews.login, {'template_name': 'login.html', 'current_app': 'gallery'}, name='login'),
    url(r'^logout/?$', authviews.logout, {'next_page': 'mainpage', 'current_app': 'gallery'}, name='logout'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^artist/(?P<pk>\d+)/?$', views.ArtistDetailView.as_view(), name='artist-detail'),
    url(r'^organizer/(?P<pk>\d+)/?$', views.OrganizerDetailView.as_view(), name='organizer-detail'),
    url(r'^drawings/(?P<pk>\d+)/?$', views.DrawingDetailView.as_view(), name='drawing-view'),
)
