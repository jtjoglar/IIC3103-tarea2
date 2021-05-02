from django.db import models

class Artista(models.Model):
    artist_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    albums = models.URLField(max_length=200)
    tracks = models.URLField(max_length=200)
    self = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    album_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    artist_id = models.ForeignKey(Artista, on_delete=models.CASCADE)
    artist = models.URLField(max_length=200)
    tracks = models.URLField(max_length=200)
    self = models.URLField(max_length=200, blank=True)


    def __str__(self):
        return self.name

class Track(models.Model):
    track_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    duration = models.FloatField()
    times_played = models.IntegerField()
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    artist_id = models.ForeignKey(Artista, on_delete=models.CASCADE)
    artist = models.URLField(max_length=200)
    album = models.URLField(max_length=200)
    self = models.URLField(max_length=200, blank=True)


    def __str__(self):
        return self.name

    def play(self):
        self.times_played = self.times_played + 1
        return 0
