import requests
import pandas
import re
from pandas.io.json import json_normalize
from configs import Config
from movieflix.models import Movie
from django.urls import reverse


class API():
    pass


class TMDB(API):
    pass


class RottonTomatoes():

    def __init__(self):
        self.config = Config.load()
        urlRT = 'https://www.rottentomatoes.com/api/private/v2.0/browse\
        ?page=1\
        &limit=40\
        &type=cf-dvd-streaming-all\
        &minTomato=70'
        # urlRT = 'https://www.rottentomatoes.com/api/private/v2.0/browse\
        # ?page=1\
        # &limit=40\
        # &type=top-dvd-streaming\
        # &minTomato=70\
        # &genres=1;2;4;5;6;8;9;10;11;13;18;14\
        # &sortBy=popularity'
        data = requests.get(urlRT).json()['results']
        self.df = json_normalize(data)

    def prepare_data(self):
        self.df.drop(['synopsisType', 'tomatoIcon',
                      'mainTrailer.id', 'id', 'posters.thumborId',
                      'posters.primary', 'dvdReleaseDate', 'url',],
                      axis=1, inplace=True)
        self.df.rename(columns={'mainTrailer.sourceId': 'trailer',
                                'tomatoScore': 'tomato_score',
                                'theaterReleaseDate': 'release_date',
                                'mpaaRating': 'rating'},
                       inplace=True)
        self.df['title'] = self.df['title'].apply(
            lambda x: re.sub(r' \(.+\)', '', x))
        self.df['actors'] = self.df['actors'].apply(lambda x: ', '.join(x))
        self.df['poster'], self.df['synopsis'] = zip(
            *self.df['title'].apply(self.get_data))
        # Set NaNs
        self.df['runtime'] = self.df['runtime'].fillna('N/A')
        self.df['trailer'] = self.df['trailer'].fillna('')
        return self.df

    def get_data(self, title):
        title = title.replace(' ', '+').replace('#', '')
        api = 'https://api.themoviedb.org/3/search/movie' 
        searchUrl = '{}?api_key={}&query={}'.format(
            api, self.config['tmdb']['api_key'], title)
        resp = requests.get(searchUrl).json()
        try:
            poster = resp['results'][0]['poster_path']
            if poster is not None:
                posterUrl = 'http://image.tmdb.org/t/p/w300{}'.format(poster)
            else:
                posterUrl = '../static/images/error.png'
        except:
            posterUrl = 'static/images/error.png'
        try:
            overview = resp['results'][0]['overview']
        except:
            print('OVERVIEW NOT WORKING')
            overview = "Not Available"
        return posterUrl, overview

    def update(self):
        for index, row in self.df.iterrows():
            try:
                movie = row.to_dict()
                self.saveMovie(movie)
            except Exception as e:
                print(e)
                continue
        return True

    def saveMovie(self, movieData):
        obj = Movie()
        for data in movieData:
            setattr(obj, data, movieData[data])
        obj.save()


def main():
    movies = RottonTomatoes()
    movies.prepare_data()
    # movies.saveDb('movie')

if __name__ == '__main__':
    main()