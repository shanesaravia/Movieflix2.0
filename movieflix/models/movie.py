from django.db import models
from .genre import Genre
import datetime
# from django.contrib.auth.models import User


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True)
    actors = models.CharField(max_length=100, default=None, blank=True, null=True)
    genres = models.ManyToManyField(Genre)
    popcorn_score = models.IntegerField(default=None, blank=True, null=True)
    tomato_score = models.IntegerField(default=None, blank=True, null=True)
    _release_date = models.DateField(max_length=15, default=None, blank=True,
                                     null=True, db_column='release_date')
    runtime = models.CharField(max_length=20, default=None, blank=True, null=True)
    rating = models.CharField(max_length=10, default=None, blank=True, null=True)
    poster = models.CharField(max_length=300, default=None, blank=True, null=True)
    synopsis = models.TextField(default=None, blank=True, null=True)
    trailer = models.CharField(max_length=300, default=None, blank=True, null=True)
    imdb_id = models.CharField(max_length=10, default=None, blank=True, null=True)
    tmdb_id = models.CharField(max_length=10, default=None, blank=True, null=True)
    language = models.CharField(max_length=3, default=None, blank=True, null=True)
    likes = models.IntegerField(default=0, blank=True, null=True)
    dislikes = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def release_date(self):
        return self._release_date

    @release_date.getter
    def release_date(self):
        return self._release_date

    @release_date.setter
    def release_date(self, new_date):
        if isinstance(new_date, datetime.date):
            self._release_date = new_date
        else:
            raise Exception('New date is not a datetime.date object')

    def pretty_release_date(self):
        pretty_date = self.release_date.strftime('%b %d, %Y')
        return pretty_date

    # favorite = models.ForeignKey(User, related_name='favorites',
    #                              on_delete=models.CASCADE)


# class Favorite(models.Model):
#     name = models.CharField(max_length=100)
#     actors = models.CharField(max_length=100)
#     popcorn_score = models.IntegerField()
#     tomato_score = models.IntegerField()
#     release_date = models.CharField(max_length=10)
#     runtime = models.CharField(max_length=20)
#     rated = models.CharField(max_length=10)
