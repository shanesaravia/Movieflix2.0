import requests
import pandas
import re
from pandas.io.json import json_normalize
from movieflix.models import Movie


class Movieflix():

    def __init__(self):
        pass

    @classmethod
    def retrieve_data(cls):
        movies = Movie.objects.all()[:30]
        print(movies[0].trailer)
        return movies


def main():
    Movieflix.retrieve_data()

if __name__ == '__main__':
    main()