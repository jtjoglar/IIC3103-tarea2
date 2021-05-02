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

url_base = 'https://tarea2-jtjoglar.herokuapp.com/'

class ArtistaList(APIView):
    def get(self, request):
        artistas = Artista.objects.all()
        serializer = ArtistaSerializer(artistas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        #{"artist_id": "2", "name": "Michael Jackson", "age": 38}
        try :
            artist_data = request.data
            #Revisamos que el request sea correcto
            if 'name' in artist_data.keys() and 'age' in artist_data.keys():
                string = artist_data['name']
                name_encoded = b64encode(string.encode()).decode('utf-8')
                if len(name_encoded) > 22:
                    name_encoded = name_encoded[:22]
                #Busca si ya existe en la base
                if Artista.objects.filter(artist_id=name_encoded):
                    art_existente = Artista.objects.get(artist_id=name_encoded)
                    serializer = ArtistaSerializer(art_existente)
                    return Response(serializer.data, status=status.HTTP_409_CONFLICT)

                new_artist = Artista.objects.create(artist_id=name_encoded, name=artist_data['name'], age=artist_data['age'],
                    albums=f'{url_base}artists/{name_encoded}/albums', tracks=f'{url_base}artists/{name_encoded}/tracks')
                #, self=f'{url_base}artists/{name_encoded}'
                new_artist.self = f'{url_base}artists/{name_encoded}'
                new_artist.save()
                serializer = ArtistaSerializer(new_artist)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response('HTTP 400 BAD REQUEST', status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ArtistaSelf(APIView):
    def get(self, request, artist_name):
        if Artista.objects.filter(artist_id=artist_name):
            artista = Artista.objects.filter(artist_id=artist_name)
            serializer = ArtistaSerializer(artista[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, artist_name):
        if Artista.objects.filter(artist_id=artist_name):
            artista = Artista.objects.filter(artist_id=artist_name)
            artista.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ArtistaAlbum(APIView):
    def get(self, request, artist_name):
        if Artista.objects.filter(artist_id=artist_name):
            albums = Album.objects.filter(artist_id=artist_name)
            serializer = AlbumSerializer(albums, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, artist_name):
        try:
            #{"name": ,"genre": } Nose si es necesario el if de abajo
            if Artista.objects.filter(artist_id=artist_name):
                album_data = request.data
                #Revisamos que el request sea correcto
                if 'name' in album_data.keys() and 'genre' in album_data.keys():
                    #Verificamos el artista
                    #Se revisa si existe el artista
                    artista = Artista.objects.filter(artist_id=artist_name)
                    string_name = album_data['name']
                    string_name = string_name+':'+artist_name
                    name_encoded = b64encode(string_name.encode()).decode('utf-8')
                    if len(name_encoded) > 22:
                        name_encoded = name_encoded[:22]
                    #Busca si ya existe en la base
                    if Album.objects.filter(album_id=name_encoded):
                        album_existente = Album.objects.get(album_id=name_encoded)
                        serializer = AlbumSerializer(album_existente)
                        return Response(serializer.data, status=status.HTTP_409_CONFLICT)

                    new_album = Album.objects.create(album_id=name_encoded, name=album_data['name'], genre=album_data['genre'],
                        artist_id=artista[0], artist=f'{url_base}artists/{artist_name}', tracks=f'{url_base}albums/{name_encoded}/tracks')
                    new_album.self = f'{url_base}albums/{name_encoded}'
                    new_album.save()
                    serializer = AlbumSerializer(new_album)

                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)


            else:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ArtistaTracks(APIView):
    def get(self, request, artist_name):
        if Artista.objects.filter(artist_id=artist_name):
            tracks = Track.objects.filter(artist_id=artist_name)
            serializer = TrackSerializer(tracks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ArtistPlay(APIView):
    def put(self, request, artist_name):
        if Artista.objects.filter(artist_id=artist_name):
            tracks = Track.objects.filter(artist_id=artist_name)
            for track in tracks:
                track.times_played += 1
                track.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class AlbumList(APIView):
    def get(self, request):
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

class AlbumSelf(APIView):
    def get(self, request, album_name):
        if Album.objects.filter(album_id=album_name):
            album = Album.objects.filter(album_id=album_name)
            serializer = AlbumSerializer(album[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, album_name):
        if Album.objects.filter(album_id=album_name):
            album = Album.objects.filter(album_id=album_name)
            album.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class AlbumTracks(APIView):
    def get(self, request, album_name):
        if Album.objects.filter(album_id=album_name):
            tracks = Track.objects.filter(album_id=album_name)
            serializer = TrackSerializer(tracks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, album_name):
        #{"name": "Confession", "duration": 3.5}
        try:
            if Album.objects.filter(album_id=album_name):
                track_data = request.data
                #Revisamos que el request sea correcto
                if 'name' in track_data.keys() and 'duration' in track_data.keys():
                    #Verificamos el album
                    album = Album.objects.filter(album_id=album_name)
                    artista = Artista.objects.filter(artist_id=album[0].artist_id.artist_id)
                    string_name = track_data['name']
                    string_name = string_name+':'+album_name
                    name_encoded = b64encode(string_name.encode()).decode('utf-8')
                    if len(name_encoded) > 22:
                        name_encoded = name_encoded[:22]
                    #Busca si ya existe en la base
                    if Track.objects.filter(track_id=name_encoded):
                        track_existente = Track.objects.get(track_id=name_encoded)
                        serializer = TrackSerializer(track_existente)
                        return Response(serializer.data, status=status.HTTP_409_CONFLICT)

                    new_track = Track.objects.create(track_id=name_encoded, name=track_data['name'], duration=track_data['duration'], times_played=0,
                        album_id=album[0], artist_id=artista[0], artist=f'{url_base}artists/{artista[0].artist_id}', album=f'{url_base}albums/{album_name}')
                    new_track.self = f'{url_base}tracks/{name_encoded}'
                    new_track.save()
                    serializer = TrackSerializer(new_track)

                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)


            else:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class AlbumPlay(APIView):
    def put(self, request, album_name):
        if Album.objects.filter(album_id=album_name):
            tracks = Track.objects.filter(album_id=album_name)
            for track in tracks:
                track.times_played += 1
                track.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class TrackList(APIView):
    def get(self, request):
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)

class TrackSelf(APIView):
    def get(self, request, track_name):
        if Track.objects.filter(track_id=track_name):
            track = Track.objects.filter(track_id=track_name)
            serializer = TrackSerializer(track[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, track_name):
        if Track.objects.filter(track_id=track_name):
            track = Track.objects.filter(track_id=track_name)
            track.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class TrackPlay(APIView):
    def put(self, request, track_name):
        if Track.objects.filter(track_id=track_name):
            track = Track.objects.get(track_id=track_name)
            track.times_played += 1
            track.save()
            serializer = TrackSerializer(track)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
