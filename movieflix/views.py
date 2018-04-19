from django.shortcuts import render
from django.shortcuts import redirect
# from .models import Movie

# import requests
from .movieApp import RottonTomatoes

#import test
from .movieData import S3
from .movieData import RottonTomatoes


# Create your views here.
def home(request):
    movies = RottonTomatoes()
    movies = movies.prepare_data()
    return render(request, 'home.html', {'moviedata': movies})
    # movies = Movie.objects.all()
    # return render(request, 'home.html', {'movies': movies})

def s3(request):
	rt = RottonTomatoes()
	rt.saveToDb()
	return redirect('http://www.movieflix.shanesaravia.com')

	# s3 = S3()
	# s3 = s3.test()
	# print(s3)
	# return render(request, 'test.html', {'data': s3.decode('utf-8')})