from django.urls import path

from movies.views import ViewMovies, ViewMovie


urlpatterns = [
    path('', ViewMovies.as_view(), name='view_movies'),
    path('view-movie/<slug:movie_slug>', ViewMovie.as_view(), name='view-movie'),
]
