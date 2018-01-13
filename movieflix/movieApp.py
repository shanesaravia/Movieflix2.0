import requests
import pandas
import re
from pandas.io.json import json_normalize
import yaml
import os


class Config(object):

    def load():
        with open('config.yml', 'r') as config:
            return yaml.load(config)


class RottonTomatoes(object):

    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.config = Config.load()
        urlRT = 'https://www.rottentomatoes.com/api/private/v2.0/browse?page=1&limit=20&type=top-dvd-streaming&minTomato=0&maxTomato=100&minPopcorn=0&maxPopcorn=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=popularity'
        data = requests.get(urlRT).json()['results']
        self.df = json_normalize(data)
        # self.prepare_data()

    def prepare_data(self):
        self.df.drop(['synopsisType', 'popcornIcon', 'tomatoIcon', 'mainTrailer.id', 'id', 'posters.thumborId', 'posters.primary', 'dvdReleaseDate', 'url', 'synopsis'], axis=1, inplace=True)
        self.df.rename(columns={'mainTrailer.sourceId': 'mainTrailer'}, inplace=True)
        self.df['title'] = self.df['title'].apply(lambda x: re.sub(r' \(.+\)', '', x))
        self.df['actors'] = self.df['actors'].apply(lambda x: ', '.join(x))
        self.df['poster'], self.df['synopsis'] = zip(*self.df['title'].apply(self.get_data))
        return self.df

    def get_data(self, title):
        title = title.replace(' ', '+').replace('#', '')
        searchUrl = 'https://api.themoviedb.org/3/search/movie?api_key={}&query={}'.format(self.config['apikey'], title)
        resp = requests.get(searchUrl).json()
        poster = resp['results'][0]['poster_path']
        overview = resp['results'][0]['overview']
        posterUrl = 'http://image.tmdb.org/t/p/w300{}'.format(poster)
        return posterUrl, overview

    # def get_html(self, start=True):
    #     env = Environment(loader=FileSystemLoader('./templates'))
    #     template = env.get_template("indextemp.html")
    #     template_vars = {'moviedata': self.df}
    #     html_out = template.render(template_vars)
    #     with open('./templates/index.html', 'w') as f:
    #         f.write(html_out)
    #     if start == True:
    #         os.chdir('./templates')
    #         os.startfile('index.html')

# def main():
#     movies = RottonTomatoes()
#     movies.get_html()


# if __name__ == '__main__':
#     main()