from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#Se importan los modelos y serializers
from .models import Artista, Album, Track
from .serializers import ArtistaSerializer, AlbumSerializer, TrackSerializer
from base64 import b64encode

class ArtistaList(APIView):
    def get(self, request):
        artistas = Artista.objects.all()
        serializer = ArtistaSerializer(artistas, many=True)
        return Response(serializer.data)

    def post(self, request):
        #{"artist_id": "2", "name": "Michael Jackson", "age": 38}
        artist_data = request.data
        #if 'name' in artist_data.keys and 'age' in artist_data.keys:
        string = artist_data['name']
        if len(string) > 22:
            string = string[:22]
            print(string)
        name_encoded = b64encode(string.encode()).decode('utf-8')
        new_artist = Artista.objects.create(artist_id=name_encoded, name=artist_data['name'], age=artist_data['age'])
        new_artist.save()
        serializer = ArtistaSerializer(new_artist)

        return Response(serializer.data)


class AlbumList(APIView):
    def get(self, request):
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self):
        pass

class TrackList(APIView):
    def get(self, request):
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)

    def post(self):
        pass
