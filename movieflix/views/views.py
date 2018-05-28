from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.db.models import Q

# from .movieData import S3
from ..controllers.movieData import RottonTomatoes
from ..controllers.movieApp import Movieflix

from movieflix.models import Movie

from configs import Config

# Load configs
config = Config.load()


def home(request):
    movie_list = Movieflix.retrieve_data()
    page = request.GET.get('page', 1)
    paginator = Paginator(movie_list, config['movie']['qty'])

    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except (InvalidPage, EmptyPage):
        movies = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'moviedata': movies})

def updateDb(request):
    rt = RottonTomatoes()
    rt.prepare_data()
    rt.update()
    print('update complete')
    return render(request, 'updateDb.html')

def search(request):
    query=request.GET.get('q')

    if query:
        results = Movie.objects.order_by('-id').filter(Q(title__icontains=query) |
                                                       Q(actors__icontains=query) |
                                                       Q(synopsis__icontains=query))
    else:
        results = None

    page = request.GET.get('page', 1)
    paginator = Paginator(results, config['movie']['qty'])

    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except (InvalidPage, EmptyPage):
        movies = paginator.page(paginator.num_pages)
    except:
        movies = None

    return render(request, 'search-results.html', {'moviedata': movies,
                                                   'query': query})

# def s3(request):
#   rt = RottonTomatoes()
#   rt.prepare_data()
#   rt.test()
#   return render(request, 'test.html')

    # s3 = S3()
    # s3 = s3.test()
    # print(s3)
    # return render(request, 'test.html', {'data': s3.decode('utf-8')})