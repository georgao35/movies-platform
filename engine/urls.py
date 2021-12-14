from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='home'),
    path('actors', views.actor_lists, name='actors'),
    path('movie/<int:movie_id>', views.movie_detail, name='mov_detail'),
    path('actor/<int:actor_id>', views.actor_detail, name='act_detail'),
    path('results', views.results_view, name='result'),
    path('search', views.search, name='search')
]
