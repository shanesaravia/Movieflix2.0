from movieflix.controllers.api import RT
from django.db.models import Q
from movieflix.models import Movie
from movieflix.models import Genre
import pandas as pd
# from movieflix.controllers.utils import Helpers


class DB():

    @classmethod
    def update(cls, df):
        print('\n\n starting DB UPDATE')

        for index, row in df.iterrows():
            # movie_obj = None

            # Update movies
            movie = Prepare.movie(row)
            movie = movie.to_dict()
            movie_obj = cls.saveMovie(movie)

            # Update genres
            for genre in row['genres']:
                genre_obj = cls.saveGenre(dict(genre=genre))
                movie_obj[0].genres.add(genre_obj[0])

        return True

    @classmethod
    def saveMovie(cls, movie_data: dict):
        """
        Fields: title, actors, popcorn_score, tomato_score, release_date,
                runtime, rating, poster, synopsis, trailer, imdb_id, tmdb_id,
                language
        """
        movie_data['_release_date'] = movie_data.pop('release_date')
        movie_obj = Movie.objects.get_or_create(**movie_data)
        return movie_obj

    @classmethod
    def saveGenre(cls, genre_data: dict):
        """
        Fields: genre, movie_title
        """
        genre_obj = Genre.objects.get_or_create(**genre_data)
        return genre_obj


class Prepare(DB):

    @classmethod
    def movie(cls, series):
        series = series.drop('genres')
        return series

    @classmethod
    def genres(cls, genres_list):
        for genre in genres_list:
            genre_obj = cls.saveGenre(dict(genre=genre))

        return True

    # @classmethod
    # def genres(cls, fk_obj, series):
    #     df = pd.DataFrame(columns=['movie_title', 'genre'])
    #     for genre in series['genres']:
    #         df = df.append({'movie_title': fk_obj, 'genre': genre},
    #                        ignore_index=True)
    #     return df


def main():
    df = RT.get_data()
    df = RT.format_df(df)
    DB.update(df)


if __name__ == '__main__':
    main()
