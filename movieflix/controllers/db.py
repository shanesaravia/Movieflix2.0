from movieflix.controllers.api import RT
from movieflix.models import Movie
import pandas as pd


class DB():

    @classmethod
    def update(cls, df):
        for index, row in df.iterrows():
            try:
                movie = row.to_dict()
                cls.saveMovie(movie)
            except Exception as e:
                print(e)
                continue
        return True

    @classmethod
    def saveMovie(cls, movieData):
        obj = Movie()
        for data in movieData:
            setattr(obj, data, movieData[data])
        obj.save()


def main():
    df = RT.get_data()
    # with pd.option_context('display.max_rows', 999):
    #     print(df['actors'])
    df = RT.format_df(df)
    print('\n\n')
    print(df)
    # with pd.option_context('display.max_rows', 999):
    # print(df['actors'])
    # DB.update(df)
    # print('\n\n\n')
    # print(df)


if __name__ == '__main__':
    main()
