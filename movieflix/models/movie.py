from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True)
    actors = models.CharField(max_length=100, default=None, blank=True, null=True)
    popcorn_score = models.IntegerField(default=None, blank=True, null=True)
    tomato_score = models.IntegerField(default=None, blank=True, null=True)
    release_date = models.CharField(max_length=15, default=None, blank=True, null=True)
    runtime = models.CharField(max_length=20, default=None, blank=True, null=True)
    rating = models.CharField(max_length=10, default=None, blank=True, null=True)
    synopsis = models.TextField(default=None, blank=True, null=True)
    poster = models.CharField(max_length=300, default=None, blank=True, null=True)
    trailer = models.CharField(max_length=300, default=None, blank=True, null=True)

    def __str__(self):
        return self.title


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