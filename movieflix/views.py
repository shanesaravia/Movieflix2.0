from django.shortcuts import render
# from .models import Movie

# import requests
from .movieApp import RottonTomatoes


# Create your views here.
def home(request):
    movies = RottonTomatoes()
    movies = movies.prepare_data()
    return render(request, 'home.html', {'moviedata': movies})
    # movies = Movie.objects.all()
    # return render(request, 'home.html', {'movies': movies})
