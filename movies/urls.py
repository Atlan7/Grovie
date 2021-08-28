from django.urls import path

from movies.views import ViewMovies, ViewMovie, AddLikeToMovie, AddDislikeToMovie


urlpatterns = [
    path('', ViewMovies.as_view(), name='view-movies'),
    path('view-movie/<slug:movie_slug>', ViewMovie.as_view(), name='view-movie'),
    path('like-movie/<int:movie_pk>', AddLikeToMovie.as_view(), name='like-movie'),
    path('dislike-movie/<int:movie_pk>', AddDislikeToMovie.as_view(), name='dislike-movie'),
]
