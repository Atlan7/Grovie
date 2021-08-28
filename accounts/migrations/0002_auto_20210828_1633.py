# Generated by Django 3.2.5 on 2021-08-28 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='disliked_movies',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disliked_movies', to='movies.movie'),
        ),
        migrations.AddField(
            model_name='profile',
            name='liked_movies',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liked_movies', to='movies.movie'),
        ),
        migrations.AddField(
            model_name='profile',
            name='movie_to_view',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie_to_view', to='movies.movie'),
        ),
    ]