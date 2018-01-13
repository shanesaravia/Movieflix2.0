from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=100)
    actors = models.CharField(max_length=100)
    popcorn_score = models.IntegerField()
    tomato_score = models.IntegerField()
    release_date = models.CharField(max_length=10)
    runtime = models.CharField(max_length=20)
    rating = models.CharField(max_length=10)

    def __str__(self):
        return self.name
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