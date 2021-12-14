from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Movie, Actor, Comment
from django.db.models import Q
from datetime import datetime


# Create your views here.
def main_view(request):
    movieList = list(Movie.objects.all())
    pages = Paginator(movieList, 20)
    current_page = int(request.GET.get('page', default=1))
    display_list = pages.get_page(current_page)
    if current_page > pages.num_pages:
        current_page = pages.num_pages
    # get page range
    page_range = range(max(1, current_page - 2), min(pages.num_pages, current_page + 2) + 1)
    path_dict = dict()
    base = '../static/pic/'
    return render(request, 'main.html', {
        'display_list': display_list,
        'current_page': current_page,
        'total': pages.num_pages,
        'movie_total': len(movieList),
        'end': pages.num_pages - 3,
        'page_range': page_range,
    })


def actor_lists(request):
    actorList = Actor.objects.all()
    pages = Paginator(actorList, 20)
    current_page = int(request.GET.get('page', default=1))
    display_list = pages.get_page(current_page)
    if current_page > pages.num_pages:
        current_page = pages.num_pages
    # get page range
    page_range = range(max(1, current_page - 2), min(pages.num_pages, current_page + 2) + 1)
    path_dict = dict()
    base = '../static/pic/'
    for actor in display_list:
        path_dict[actor] = base + actor.name + '.jpg'
    return render(request, 'actorlist.html', {
        'display_list': display_list,
        'current_page': current_page,
        'total': pages.num_pages,
        'movie_total': len(actorList),
        'end': pages.num_pages - 3,
        'page_range': page_range,
        'img_path': None,
        'paths': path_dict
    })


def movie_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    a = movie.comment_set.filter()
    base = '../static/pic/'
    if len(a) > 5:
        a = a[1:6]
    return render(request, 'moviewdetail.html', {
        'movie_id': movie_id,
        'title': movie.title,
        'brief': movie.brief,
        'other_info': movie.other_info,
        'comments': a,
        'path': base + movie.title + '.jpg',
        'actors': movie.actors.all(),
    })


def actor_detail(request, actor_id):
    actor = Actor.objects.filter(pk=actor_id)
    actor = list(actor)[0]
    dic = dict()
    for other_actor in actor.collaborate.all():
        dic[other_actor] = getCommon(actor, other_actor)
    actors = sorted(dic.items(), key=lambda d: d[1], reverse=True)
    actors = actors[0:10]
    return render(request, 'actordetail.html', {
        'actor': actor,
        'collaboration': actors,
    })


def results_view(request):
    return render(request, 'results.html')


def search(request):
    start_ = datetime.utcnow()
    typeSelected = request.GET['types']
    keyword = request.GET['keyword']
    if typeSelected == 'movies':
        if keyword == '':
            return HttpResponseRedirect(reverse('home'))
        query = Q(title__contains=keyword) | Q(actors__name__contains=keyword)
        movie_list = Movie.objects.filter(query).all().distinct()
        result = list(movie_list)
    elif typeSelected == 'actors':
        if keyword == '':
            return HttpResponseRedirect(reverse('actors'))
        query = Q(name__contains=keyword) | Q(movie__title__contains=keyword)
        actor_list = Actor.objects.filter(query).all().distinct()
        result = list(actor_list)
    else:
        comments = list(Comment.objects.filter(content__contains=keyword).all())
        result = comments
    end_ = datetime.utcnow()
    c = (end_ - start_)
    pages = Paginator(result, 20)
    current_page = int(request.GET.get('page', default=1))
    if current_page > pages.num_pages:
        current_page = pages.num_pages
    display_list = pages.get_page(current_page)
    page_range = range(max(1, current_page - 2), min(pages.num_pages, current_page + 2) + 1)

    #    return redirect()
    return render(request, 'results.html', {
        'time': c,
        'results': display_list,
        'type': typeSelected,
        'size': len(list(result)),
        'end': pages.num_pages - 3,
        'page_range': page_range,
        'current_page': current_page,
        'total': pages.num_pages,
        'keyword': keyword
    })


def getCommon(actor1, actor2):
    mov_set1 = set(actor1.movie_set.all())
    mov_set2 = set(actor2.movie_set.all())
    return len(mov_set1 & mov_set2)
