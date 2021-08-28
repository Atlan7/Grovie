import os
import re
from PIL import Image
from datetime import date, datetime

from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField('Category name', max_length=150, unique=True)
    description = models.TextField('Category description')
    url = models.SlugField('Slug for category', blank=True, max_length=300)

    def save(self,*args, **kwargs):
        if not self.url:
            url = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Genre(models.Model):
    name = models.CharField('Genre name', max_length=150, unique=True)
    description = models.TextField('Genre description')
    url = models.SlugField('Slug for genre', blank=True, max_length=300)

    def save(self,*args, **kwargs):
        if not self.url:
            url = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name




class Actor(models.Model):
    def actor_image_path_heandler(instance, filename):
        """Uploading actor image, if user set new one, deleting the old"""
        actor_img_name = f'actors/actor_{instance.pk}/actor_img.jpg'
        full_img_path = os.path.join(settings.MEDIA_ROOT, actor_img_name)

        # Deleting old image if exists
        if os.path.exists(full_img_path):
            os.remove(full_img_path)
        return actor_img_name

    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    date_of_birth = models.DateField('Actor date of the birth')
    biography = models.CharField('Actor biography', max_length=5000, blank=True, null=True)
    actor_image = models.ImageField('Actor photo', blank=True, upload_to=actor_image_path_heandler, default='user/default-img.jpg')

    def clean(self):
        if self.date_of_birth > date.today():
            raise ValidationError("Wrong date of birth!")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.actor_image:
            SIZE = 300, 300
            picture = Image.open(self.actor_image.path)
            picture.thumbnail(SIZE, Image.LANCZOS)
            picture.save(self.actor_image.path)

    def get_age(self):
        return datetime.today().year - self.date_of_birth.year

    def __str__(self):
        return f'{self.first_name} {self.second_name},'


class Country(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def clean(self):
        if re.match(r'[0-9]+', self.name):
            raise ValidationError("Name of the country can't contain numbers!")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'



class Movie(models.Model):

    def movie_title_image_path_headler(instance, filename):
        """Uploading movie title image, if user set new one, deleting the old"""
        movie_title_img_name = f'movies/movie_{instance.pk}/movie_title_img.jpg'
        full_img_path = os.path.join(settings.MEDIA_ROOT, movie_title_img_name)

        # Deleting old image if exists
        if os.path.exists(full_img_path):
            os.remove(full_img_path)
        return movie_title_img_name

    AGE_CHOICES = (
        ('0+', '0+'),
        ('6+', '6+'),
        ('12+', '12+'),
        ('16+', '16+'),
        ('18+', '18+'),
    )

    name = models.CharField('Movie name', max_length=150, unique=True)
    category = models.ManyToManyField(Category, verbose_name='Category')
    genres = models.ManyToManyField(Genre, verbose_name='Movie genres')
    title_image = models.ImageField('Title image for movie', upload_to=movie_title_image_path_headler)
    world_rating = models.PositiveSmallIntegerField('Movie world rating', default=0)
    country = models.ManyToManyField(Country, verbose_name='Movie country')
    world_fees = models.PositiveIntegerField('Fees in world')
    budget = models.PositiveIntegerField('Movie budget')
    world_premier = models.DateField('Movie world premier')
    is_published = models.BooleanField('is published', default=False)
    discription = models.TextField('Movie description')
    actors = models.ManyToManyField(Actor, verbose_name='Actors', related_name='movie_actors')
    directors = models.ManyToManyField(Actor, verbose_name='Directors', related_name='movie_directors')
    url = models.SlugField('Slug for movie', max_length=300, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='movie_likes')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='movie_dislikes')
    min_viewing_age = models.CharField(max_length=6, choices=AGE_CHOICES)

    def save(self, *args, **kwargs):
        if not self.url:
            url = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absloute_url(self):
        return reverse_lazy('movies:view-movie', kwargs={'movie_slug': self.url})

    def clean(self):
        if self.world_rating > 10 or self.world_rating < 0:
            raise ValidationError("Invalid world rating")

    def __str__(self):
        return self.name

    @property
    def get_total_likes(self):
        return self.likes.count()


class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='reviews_to_movie', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField('Comment', max_length=5000)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='review_likes')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='review_dislikes')
    parent = models.ForeignKey('self', verbose_name='parent', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.movie.name} - {self.user}'
