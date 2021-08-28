from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .models import Movie

from .services import add_like_to_the_movie, add_dislike_to_the_movie


class ViewMovies(ListView):
    model = Movie
    template_name = 'movies/view_movies.html'
    context_object_name = 'movies'
    ordering = ['-world_rating']


class ViewMovie(DetailView):
    model = Movie
    template_name = 'movies/view_movie.html'
    context_object_name = 'movie'
    slug_field = 'url'
    slug_url_kwarg = 'movie_slug'


class AddLikeToMovie(LoginRequiredMixin, View):
    def post(self, request, movie_pk, *args, **kwargs):
        movie = get_object_or_404(Movie, pk=movie_pk)
        add_like_to_the_movie(request, movie)
        return HttpResponseRedirect(reverse_lazy('movies:view-movie', args=[str(movie.url)]))


class AddDislikeToMovie(LoginRequiredMixin, View):
    def post(self, request, movie_pk, *args, **kwags):
        movie = get_object_or_404(Movie, pk=movie_pk)
        add_dislike_to_the_movie(request, movie)
        return HttpResponseRedirect(reverse_lazy('movies:view-movie', args=[str(movie.url)]))
