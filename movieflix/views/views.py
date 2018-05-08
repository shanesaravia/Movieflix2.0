from django.shortcuts import render
# from .models import Movie

# import requests
# from .movieApp import RottonTomatoes

#import test
# from .movieData import S3
from ..controllers.movieData import RottonTomatoes
from ..controllers.movieApp import Movieflix


def home(request):
    movies = Movieflix.retrieve_data()
    return render(request, 'home.html', {'moviedata': movies})

# Create your views here.
# def home(request):
#     movies = RottonTomatoes()
#     movies = movies.prepare_data()
#     return render(request, 'home.html', {'moviedata': movies})
    # movies = Movie.objects.all()
    # return render(request, 'home.html', {'movies': movies})

def updateDb(request):
	rt = RottonTomatoes()
	rt.prepare_data()
	rt.update()
	print('update complete')
	return render(request, 'updateDb.html')

# def s3(request):
# 	rt = RottonTomatoes()
# 	rt.prepare_data()
# 	rt.test()
# 	return render(request, 'test.html')

	# s3 = S3()
	# s3 = s3.test()
	# print(s3)
	# return render(request, 'test.html', {'data': s3.decode('utf-8')})