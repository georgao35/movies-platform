from django.contrib import admin
from engine.models import Movie, Actor, Comment
# Register your models here.
admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Comment)
