import os
from PIL import Image

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from movies.models import Movie


def profile_image_path_heandler(instance, filename):
    """Uploading profile image, if user set new one, deleting the old"""
    profile_img_name = f'users/user_{instance.pk}/profile.jpg'
    full_img_path = os.path.join(settings.MEDIA_ROOT, profile_img_name)

    # Deleting old image if exists
    if os.path.exists(full_img_path):
        os.remove(full_img_path)
    return profile_img_name


class Profile(AbstractUser):
    profile_image = models.ImageField('profile_image', upload_to=profile_image_path_heandler, default='user/default-img.jpg', null=True, blank=True)
    date_of_birth = models.DateField('Date of the birth', null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    movie_to_view = models.ForeignKey(Movie, related_name='movie_to_view', on_delete=models.CASCADE, blank=True, null=True)
    liked_movies = models.ForeignKey(Movie, related_name='liked_movies', on_delete=models.CASCADE, blank=True, null=True)
    disliked_movies = models.ForeignKey(Movie, related_name='disliked_movies', on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_image:
            SIZE = 300, 300
            picture = Image.open(self.profile_image.path)
            picture.thumbnail(SIZE, Image.LANCZOS)
            picture.save(self.profile_image.path)

    def __str__(self):
        return self.username
