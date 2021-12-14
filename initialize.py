import json, os, sys
from engine.models import Actor, Movie, Comment

dirMovies = 'src/movies/json'
dirActor = 'src/actors/json'
dirTry = 'src/trial/json'


def main():
    actors()
    movie()
    finishActors()
    pass


def actors():
    files = os.listdir(dirActor)
    for file in files:
        path = os.path.join(dirActor, file)
        f = open(path).read()
        dic = json.loads(f)
        a = Actor(name=dic['name'], brief=dic['brief'], info=dic['info'])
        a.save()


def movie():
    files = os.listdir(dirMovies)
    for file in files:
        path = os.path.join(dirMovies, file)
        f = open(path).read()
        dic = json.loads(f)
        q = Movie(title=dic['title'], brief=dic['brief'], other_info=dic['other'])
        q.save()
        for actor_name in dic['actors']:
            actor = Actor.objects.filter(name__contains=actor_name)
            if list(actor).__len__():
                q.actors.add(list(actor)[0])
        for comment in dic['comment']:
            c = Comment(content=str(comment), movie=q)
            c.save()


def getActorsCollaboration(actor):
    movie_set = set(actor.movie_set.all())
    actor_all = set()
    for movie in movie_set:
        actors = set(movie.actors.all())
        for actor in actors:
            actor_all.add(actor)
    dic = dict()
    for other_actor in actor_all:
        if other_actor != actor:
            dic[other_actor] = getCommon(actor, other_actor)
    dic = sorted(dic.items(), key=lambda d: d[1], reverse=True)
    return dic[0:10]


def finishActors():
    for actor in Actor.objects.all():
        tmp = getActorsCollaboration(actor)
        count = 0
        for other_actor in tmp:
            if count == 10:
                continue
            if other_actor[0].name != actor.name:
                count += 1
                actor.collaborate.add(other_actor[0])


def getCommon(actor1, actor2):
    mov_set1 = set(actor1.movie_set.all())
    mov_set2 = set(actor2.movie_set.all())
    return len(mov_set1 & mov_set2)
