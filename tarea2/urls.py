"""tarea2 URL Configuration

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
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from apirest import views


urlpatterns = [
    path('admin/', admin.site.urls),
    #re_path(r'^artists$', views.ArtistaList.as_view()),
    path('artists', views.ArtistaList.as_view()),
    path('albums', views.AlbumList.as_view()),
    path('tracks', views.TrackList.as_view()),
    path('artists/<str:artist_name>', views.ArtistaSelf.as_view()),
    path('artists/<str:artist_name>/albums', views.ArtistaAlbum.as_view()),
    path('albums/<str:album_name>', views.AlbumSelf.as_view()),
    path('albums/<str:album_name>/tracks', views.AlbumTracks.as_view()),
    path('tracks/<str:track_name>', views.TrackSelf.as_view()),
    path('artists/<str:artist_name>/tracks', views.ArtistaTracks.as_view()),
    path('artists/<str:artist_name>/albums/play', views.ArtistPlay.as_view()),
    path('albums/<str:album_name>/tracks/play', views.AlbumPlay.as_view()),
    path('tracks/<str:track_name>/play', views.TrackPlay.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
