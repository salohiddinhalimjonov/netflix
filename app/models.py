from django.db import models
from django.contrib.auth.models import User


class Actor(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    birth_date = models.DateField()
    gender = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    year = models.DateField()
    imdb = models.FileField(null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    actor = models.ManyToManyField(Actor, related_name='actor')
    watched = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name

class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.movie

