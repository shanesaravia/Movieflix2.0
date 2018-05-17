from django.shortcuts import render

# from .movieData import S3
from ..controllers.movieData import RottonTomatoes
from ..controllers.movieApp import Movieflix


def home(request):
    movies = Movieflix.retrieve_data()
    return render(request, 'home.html', {'moviedata': movies})

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