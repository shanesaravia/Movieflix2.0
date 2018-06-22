import requests
import numpy as np
import re
from pandas.io.json import json_normalize
from configs import Config
# from movieflix.models import Movie
import datetime
import time
import math

# Load configs
config = Config.load()
rt_config = Config.load('rt.yml')


class API():
    @classmethod
    def format_query(cls, base_url, **kwargs):
        initial = True
        for k, v in kwargs.items():
            v = v.replace(' ', '+').replace('#', '')
            if initial is True:
                base_url += '?{}={}'.format(str(k), str(v))
                initial = False
            else:
                base_url += '&{}={}'.format(str(k), str(v))
        return base_url


class TMDB(API):

    @classmethod
    def api_cooldown(cls, headers):
        """
        Checks api request limit and runs cooldown
        """
        limit_remaining = int(headers['X-RateLimit-Remaining'])
        if limit_remaining <= 1:
            limit_reset = int(headers['X-RateLimit-Reset'])
            limit_reset_time = datetime.datetime.fromtimestamp(limit_reset)
            now = datetime.datetime.now()
            cooldown = limit_reset_time - now
            cooldown = math.ceil(cooldown.total_seconds()) + 1
            time.sleep(cooldown)

    @classmethod
    def get_id(cls, title):
        """
        Makes 1 API call
        """
        search_url = config['tmdb']['search_url']
        query = cls.format_query(search_url,
                                 api_key=config['tmdb']['api_key'],
                                 query=title)
        resp = requests.get(query)
        cls.api_cooldown(resp.headers)
        json_data = resp.json()
        data = cls.search_newest_match(title, json_data)

        tmdb_id = data['id']

        return tmdb_id

    @classmethod
    def get_data(cls, movie_id):
        """
        Makes 1 API call
        """
        movie_url = config['tmdb']['movie_url'] + str(movie_id)
        query = cls.format_query(movie_url,
                                 api_key=config['tmdb']['api_key'])
        resp = requests.get(query)
        cls.api_cooldown(resp.headers)
        data = resp.json()

        poster = cls.format_poster_url(data['poster_path'])
        synopsis = data['overview']
        release_date = cls.convert_to_datetime(data['release_date'])
        language = data['original_language']
        genres = cls.format_genres(data['genres'])
        imdb_id = data['imdb_id']
        runtime = data['runtime']

        return poster, synopsis, release_date, \
            language, genres, imdb_id, runtime

    @classmethod
    def format_poster_url(cls, poster_url):
        try:
            poster = config['tmdb']['img_url'] + poster_url
        except TypeError:
            poster = None
        return poster

    @classmethod
    def convert_to_datetime(cls, release_date):
        date = datetime.datetime.strptime(release_date, '%Y-%m-%d').date()
        return date

    @classmethod
    def format_genres(cls, genre_data):
        genres = []
        for genre in genre_data:
            genres.append(genre['name'])
        return genres

    @classmethod
    def search_newest_match(cls, title, resp):
        """
        Parse the top 3 search results and return the newest match
        Only use those which match title
        If none found, return first
        """
        newest = None
        newest_date = None
        for movie_data in resp['results'][:config['tmdb']['search_limit']]:
            if movie_data['title'].lower() == title.lower():
                try:
                    date = datetime.datetime.strptime(movie_data['release_date'],
                                                      '%Y-%m-%d').date()
                    if not newest:
                        newest = movie_data
                        newest_date = date
                    elif newest_date > date:
                        continue
                    else:
                        newest = movie_data
                        newest_date = date
                except ValueError:
                    continue

        if newest is None:
            return resp['results'][0]
        else:
            return newest


class RT(API):

    @classmethod
    def get_data(cls):
        """
        Returns a pandas dataframe
        """
        url = rt_config['fresh']['base']
        data = requests.get(url).json()['results']
        df = json_normalize(data)
        return df

    @classmethod
    def format_df(cls, df):
        # Drop unwanted columns
        df.drop(rt_config['columns_to_drop'],
                axis=1, inplace=True)
        # Rename columns
        df.rename(columns=rt_config['columns_to_rename'],
                  inplace=True)
        df['title'] = df['title'].apply(
            lambda x: re.sub(r' \(.+\)', '', x))
        df['actors'] = df['actors'].apply(lambda x: ', '.join(x)
                                          if x else np.NaN)
        # Get TMDB ID
        df['tmdb_id'] = df['title'].apply(TMDB.get_id)
        # Get TMDB movie data
        df['poster'], df['synopsis'], df['release_date'], df['language'], \
            df['genres'], df['imdb_id'], df['runtime'] = zip(
            *df['tmdb_id'].apply(TMDB.get_data))
        # Set NaNs
        df.update(df[['actors', 'runtime', 'trailer']].fillna('N/A'))
        # df['actors'] = df['actors'].fillna('N/A')
        # df['runtime'] = df['runtime'].fillna('N/A')
        # df['trailer'] = df['trailer'].fillna('')
        # Reorder columns
        df = df[rt_config['order_columns']]
        return df


def main():
    df = RT.get_data()
    df = RT.format_df(df)
    # print(df)
    # RT.update(df)


if __name__ == '__main__':
    main()
