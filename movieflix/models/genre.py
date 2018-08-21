from django.db import models
# from .movie import Movie


class Genre(models.Model):
    # movie_title = models.ForeignKey(Movie, to_field='title',
    #                                 db_column='movie_title',
    #                                 on_delete=models.CASCADE)
    genre = models.CharField(max_length=30)

    def __str__(self):
        return self.genre
