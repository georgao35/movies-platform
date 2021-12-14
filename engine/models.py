from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=20)
    brief = models.CharField(max_length=150)
    info = models.CharField(max_length=150)
    collaborate = models.ManyToManyField(to='self')

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=20)
    brief = models.CharField(max_length=150)
    other_info = models.CharField(max_length=100)
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
# Create your models here.
