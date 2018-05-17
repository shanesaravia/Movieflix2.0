import requests
import pandas
import re
from pandas.io.json import json_normalize
from movieflix.models import Movie
from movieflix.views import views


class Movieflix():

    def __init__(self):
        pass

    @classmethod
    def retrieve_data(cls):
        try:
            movies = Movie.objects.all()[:29]
            if not movies:
                views.updateDb(None)
                movies = Movie.objects.all()[:29]
        except Exception as e:
            print(e)
        return movies


def main():
    Movieflix.retrieve_data()

if __name__ == '__main__':
    main()