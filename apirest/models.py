from django.db import models

class Artista(models.Model):
    artist_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    #albums = models.URLField(max_length=200, blank=True)
    #tracks = models.URLField(max_length=200, blank=True)
    #self = models.URLField('HOLA')

    def __str__(self):
        return self.name

class Album(models.Model):
    album_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    artist = models.ForeignKey(Artista, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Track(models.Model):
    track_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    duration = models.FloatField()
    times_played = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
