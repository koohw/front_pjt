from django.db import models
from django.conf import settings

# Create your models here.
class Movie(models.Model):
    tmdb_id = models.IntegerField(primary_key=True)
    original_language = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    poster_path = models.CharField(max_length=500, null=True)
    backdrop_path = models.CharField(max_length=500, null=True)
    genre_ids = models.JSONField()
    genres = models.ManyToManyField('Genre', related_name='movies')
    adult = models.BooleanField()
    popularity = models.DecimalField(default=None, max_digits=20, decimal_places=3)
    vote_average = models.DecimalField(max_digits=20, decimal_places=1)
    vote_count = models.IntegerField()
    video = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_movies",
        blank=True
    )

    def __str__(self):
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=100)  # 장르 이름
    
    
    def __str__(self):
        return self.title