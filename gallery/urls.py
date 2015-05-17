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
    url(r'^drawings/(?P<pk>\d+)/?$', views.DrawingDetailView.as_view(), name='drawing-detail'),
    url(r'^drawings/(?P<pk>\d+)/edit/?$', views.DrawingEditView.as_view(), name='drawing-edit'),
    # url(r'^drawings/create/?$', views.DrawingCreateView.as_view(), name='drawing-create'),
    url(r'^drawings/(?P<pk>\d+)/genres/?$', views.DrawingGenresListView.as_view(), name='drawing-genres'),
    url(r'^drawings/(?P<drawing_id>\d+)/genres/update/?$', views.update_drawing_genres_order, name='drawing-genres-update'),
    url(r'^exhibitions/(?P<pk>\d+)/?$', views.ExhibitionDetailView.as_view(), name='exhibition-detail'),
    url(r'^exhibitions/(?P<pk>\d+)/edit/?$', views.ExhibitionEditView.as_view(), name='exhibition-edit'),
    # url(r'^exhibitions/create/?$', views.ExhibitionCreateView.as_view(), name='exhibition-create'),
    url(r'^exhibitions/(?P<pk>\d+)/genres/?$', views.ExhibitionGenresListView.as_view(), name='exhibition-genres'),
    url(r'^exhibitions/(?P<exhibition_id>\d+)/genres/update/?$', views.update_exhibition_genres_order, name='exhibition-genres-update'),
    url(r'^genres/?$', views.GenresView.as_view(), name='genres')
)
