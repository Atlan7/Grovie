from django.views.generic import ListView, DetailView

from .models import Movie


class ViewMovies(ListView):
    model = Movie
    template_name = 'movies/view_movies.html'
    context_object_name = 'movies'


class ViewMovie(DetailView):
    model = Movie
    template_name = 'movies/view_movie.html'
    context_object_name = 'movie'
    slug_field = 'url'
    slug_url_kwarg = 'movie_slug'
