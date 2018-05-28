import requests
import pandas
import re
from pandas.io.json import json_normalize
from movieflix.models import Movie
from movieflix.views import views
from configs import Config

# Load configs
config = Config.load()


class Movieflix():

    @classmethod
    def retrieve_data(cls):
        qty = config['movie']['qty'] * config['movie']['pages']
        try:
            movies = Movie.objects.all().order_by('-id')[:qty]
            if not movies:
                views.updateDb(None)
                movies = Movie.objects.all().order_by('-id')[:qty]
        except Exception as e:
            print(e)
        return movies


def main():
    Movieflix.retrieve_data()

if __name__ == '__main__':
    main()