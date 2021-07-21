from django.contrib import admin

from .models import Category, Genre, Actor, Country, Movie, Review

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Country)
admin.site.register(Movie)
admin.site.register(Review)
