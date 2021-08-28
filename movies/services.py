from .models import Movie


def add_like_to_the_movie(request, movie):
        if movie.dislikes.filter(id=request.user.id).exists():
            movie.dislikes.remove(request.user)
            movie.likes.add(request.user)

        elif movie.likes.filter(id=request.user.id).exists():
            movie.likes.remove(request.user)

        else:
            movie.likes.add(request.user)


def add_dislike_to_the_movie(request, movie):
        if movie.likes.filter(id=request.user.id).exists():
            movie.likes.remove(request.user)
            movie.dislikes.add(request.user)

        elif movie.dislikes.filter(id=request.user.id).exists():
            movie.dislikes.remove(request.user)

        else:
            movie.dislikes.add(request.user)
