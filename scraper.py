# This Python file uses the following encoding: utf-8
# coding=utf-8
import re
import os
import sys
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests
import json
import random
import time

os.makedirs('./src/movies/pic', exist_ok=True)
os.makedirs('./src/movies/json', exist_ok=True)
os.makedirs('./src/movies/html', exist_ok=True)

os.makedirs('./src/actors/pic', exist_ok=True)
os.makedirs('./src/actors/json', exist_ok=True)
os.makedirs('./src/actors/html', exist_ok=True)



USER_AGENTS = [
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12 "
]
#IP地址列表，用于设置IP代理
IP_AGENTS = [
    '182.39.6.245:38634',
    '115.210.181.31:34301',
    '123.161.152.38:23201',
    '222.85.5.187:26675',
    '123.161.152.31:23127',
]

#设置IP代理
proxy = random.choice(IP_AGENTS)
proxies = {
    'http': "http://"+proxy,
    'https': "https://"+proxy,
}

headers = {
    'User-agent': random.choice(USER_AGENTS),
}

# page_index = 28 日本
page_index = 53
params = {
    'type': 'movie',
    'sort': 'recommend',
    'page_limit': 50,
    'page_start': 0
}

base = "https://movie.douban.com"
baseurl = "https://movie.douban.com/j/search_subjects?type=movie&amp;tag=欧美&amp;sort=recommend&amp;page_limit=500&amp;page_start="
baseMovieDir = './src/movies/json'
baseActorDir = './src/actors/json'
actors_all_urls = set()

for i in range(2):
    url = baseurl + str(page_index)
    reqs = requests.get(url, data=params, headers=headers)
    print(reqs)
    results = json.loads(reqs.content)
    results = results['subjects']
    for result in results:
        moviesAll = os.listdir(baseMovieDir)
        req = Request(result['url'], headers=headers)
        # time.sleep(5)
        html = urlopen(req).read().decode('utf-8')
        bs = BeautifulSoup(html, features='lxml')
        if bs.h1 is None:
            continue
        title = bs.h1.span.getText()
        title = (':').join(title.split('.'))
        title = ('').join(title.split('/'))
        if title+'.json' in moviesAll:
            continue
        with open('./src/movies/html/%s.html' % title, 'w', encoding='utf-8') as f:
            f.write(html)
        #print(title)
        actors_raw = bs.find_all(
            'a', {'rel': 'v:starring'})
        actors = []
        count = 0
        for actor in actors_raw:
            if count == 10:
                break
            if actor['href'] in actors_all_urls:
                actors.append(actor.getText())
                count += 1
                continue
            actorReq = Request(base + actor['href'], headers=headers)
            # time.sleep(5)
            actorHtml = urlopen(actorReq).read().decode('utf-8')
            actorbs = BeautifulSoup(actorHtml, features='lxml')
            if actorbs.h1 is None:
                continue
            name = actorbs.h1.getText()
            if name+'.json' in os.listdir(baseActorDir):
                actors.append(actor.getText())
                count += 1
                continue
            with open('./src/actors/html/%s.html' % name, 'w', encoding='utf-8') as f:
                f.write(actorHtml)
            actorbs.find('div', {'class': 'pic'}).find('a').img['src']
            if actorbs.find('div', {'class': 'pic'}).find('a').img['src'] is not None:
                # time.sleep(5)
                pic = requests.get(actorbs.find(
                    'div', {'class': 'pic'}).find('a').img['src'])
                with open('./src/actors/pic/%s.jpg' % name, "wb") as f:
                    f.write(pic.content)
            info = actorbs.find('div', {'class': 'info'}).getText()
            if actorbs.find('span', {'class': 'all hidden'}):
                brief = actorbs.find('span', {'class': 'all hidden'}).getText()
            else:
                brief = actorbs.find('div', {'id': 'intro'}).find(
                    'div', {'class': 'bd'}).getText()
            actorDic = {'name': name, 'info': info, 'brief': brief}
            with open('./src/actors/json/%s.json' % name, 'w', encoding='utf-8') as f:
                json.dump(actorDic, f, ensure_ascii=False, indent=4)
            actors.append(actor.getText())
            actors_all_urls.add(actor['href'])
            count += 1
        if bs.find('span', {'class': 'all hidden'}) is None:
            brief = bs.find('span', {'property': 'v:summary'}).getText()
        else:
            brief = bs.find('span', {'class': 'all hidden'}).getText()
        #print(brief)
        other_info = bs.find('div', {'id': 'info'}).getText()
        #print(other_info.getText())
        # time.sleep(4)
        r = requests.get(bs.find('img')['src'])
        with open('./src/movies/pic/%s.jpg' % title, "wb") as f:
            f.write(r.content)
        
        raw_comments = bs.select('div[class="comment"]')
        comments = []
        for raw_comment in raw_comments:
            if raw_comment.select('span[class="hide-item full"]'):
                comment = raw_comment.find('span',{'class': "hide-item full"}).getText()
            else:
                comment = raw_comment.find('span',{'class': 'short'}).getText()
            comments.append(comment)
        
        print(title)
        dic = {'title': title, 'actors': actors, 'brief': brief,
               'other': other_info, 'comment': comments}
        with open('./src/movies/json/%s.json' % title, 'w', encoding='utf-8') as f:
            json.dump(dic, f, ensure_ascii=False, indent=4)
    params['page_start'] += 500
    page_index += 500
