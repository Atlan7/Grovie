import re
from datetime import datetime

from django.db import models
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField('Category name', max_length=150, unique=True)
    description = models.TextField('Category description')
    url = models.SlugField('Slug for category', max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Genre(models.Model):
    name = models.CharField('Genre name', max_length=150, unique=True)
    description = models.TextField('Genre description')
    url = models.SlugField('Slug for genre', max_length=300)

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    date_of_birth = models.DateField('Actor date of the birth')
    image = models.ImageField('Actor photo', upload_to='media/actors/image/')

    def clean(self):
        if datetime.now().year - self.date_of_birth.year <= 0:
            raise ValidationError("Wrong date of birth!")

    @property
    def get_age(self):
        return datetime.today().year - self.date_of_birth

    def __str__(self):
        return f'{self.first_name} {self.second_name}'


class Country(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def clean(self):
        if re.match(r'<+d>', self.name):
            raise ValidationError("Name of the country can't contain numbers!")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

class Movie(models.Model):

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
    title_image = models.ImageField('Title image for movie', upload_to='media/movies/image', blank=True, null=True)
    world_rating = models.PositiveSmallIntegerField('Movie world rating', default=0)
    country = models.ManyToManyField(Country, verbose_name='Movie country')
    world_fees = models.PositiveIntegerField('Fees in world')
    budget = models.PositiveIntegerField('Movie budget')
    world_premier = models.DateField('Movie world premier')
    is_published = models.BooleanField('is published', default=False)
    discription = models.TextField('Movie description')
    actors = models.ManyToManyField(Actor, verbose_name='Actors', related_name='movie_actors')
    directors = models.ManyToManyField(Actor, verbose_name='Directors', related_name='movie_directors')
    url = models.SlugField('Slug for movie', max_length=300)
    likes = models.PositiveIntegerField('Movie likes', default=0)
    dislikes = models.PositiveIntegerField('Movie dislikes', default=0)
    min_viewing_age = models.CharField(max_length=6, choices=AGE_CHOICES)

    def get_absloute_url(self):
        return reverse_lazy('movies:view-movie', kwargs={'movie_slug': self.url})

    def clean(self):
        if self.world_rating > 10 or self.world_rating < 0:
            raise ValidationError("Invalid world rating")

    def __str__(self):
        return self.name

class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='reviews_to_movie', on_delete=models.CASCADE)
    user = models.CharField(max_length=255)
    comment = models.TextField('Comment', max_length=5000)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField('Review likes', default=0)
    dislikes = models.PositiveIntegerField('Review dislikes', default=0)
    parent = models.ForeignKey('self', verbose_name='parent', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.movie.name} - {self.user}'
