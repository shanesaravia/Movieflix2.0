import requests
import pandas
import re
from pandas.io.json import json_normalize
import yaml
import os
import boto3
import base64
import io
from movieflix.models import Movie

class Config(object):

    def load():
        with open('config.yml', 'r') as config:
            return yaml.load(config)


class RottonTomatoes(Config):

    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
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
        self.df.drop(['synopsisType', 'popcornIcon', 'tomatoIcon',
                      'mainTrailer.id', 'id', 'posters.thumborId',
                      'posters.primary', 'dvdReleaseDate', 'url',
                      'synopsis'], axis=1, inplace=True)
        self.df.rename(columns={'mainTrailer.sourceId': 'mainTrailer'},
                       inplace=True)
        self.df['title'] = self.df['title'].apply(
            lambda x: re.sub(r' \(.+\)', '', x))
        self.df['actors'] = self.df['actors'].apply(lambda x: ', '.join(x))
        self.df['poster'], self.df['synopsis'] = zip(
            *self.df['title'].apply(self.get_data))
        return self.df

    def get_data(self, title):
        title = title.replace(' ', '+').replace('#', '')
        api = 'https://api.themoviedb.org/3/search/movie'
        searchUrl = '{}?api_key={}&query={}'.format(
            api, self.config['apikey'], title)
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

    def saveToDb(self):
        m = Movie(title='test')
        m.save()


class S3(Config):

    def __init__(self):
        pass

    def test(self):
        # Get image
        image = 'http://image.tmdb.org/t/p/w300/kOVEVeg59E0wsnXmF9nrh6OmWII.jpg'
        res = requests.get(image, stream=True)

        # Create bucket
        s3 = boto3.resource('s3')
        bucket = s3.create_bucket(Bucket='movieflix-s3')

        # Upload image
        bucket.put_object(Key='test-image', Body=res.content)

        # Download image

        obj = s3.Object('movieflix-test', 'test-image')
        obj = obj.get()['Body'].read()

        image = io.BytesIO(obj)
        image = base64.b64encode(image.getvalue())

        return image
        # return s3.buckets.all()

def main():
    movies = RottonTomatoes()
    movies.saveToDb()

if __name__ == '__main__':
    main()