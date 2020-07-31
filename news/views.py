from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from django.conf import settings
import random
import datetime
import json

HYPERNEWS = []

NEWS_IDS = []

with open(settings.NEWS_JSON_PATH, "r") as f:
    HYPERNEWS = json.load(f)
    for item in HYPERNEWS:
        NEWS_IDS.append(item["link"])

class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return redirect("news/")


class NewsPageView(View):
    def get(self, request, *args, **kwargs):
        if "news_id" in kwargs:
            news_id = kwargs["news_id"]
            news_item = filter(lambda el: el["link"] == news_id, HYPERNEWS)
            item = list(news_item)
            if not item:
                return HttpResponseForbidden("Can't look at anything here", content_type="text/plain")
            else:
                return render(request, "news/one_news.html", context=item[0])
        else:
            return HttpResponseForbidden("Can't look at anything here", content_type="text/plain")


class NewsMainView(View):
    def get(self, request, *args, **kwargs):
        if "q" in request.GET:
            title_data = str(request.GET.get('q')).strip()
            if len(title_data):
                news_items_iterator = filter(lambda el: el["title"].lower().find(title_data.lower()) != -1, HYPERNEWS)
                items = list(news_items_iterator)
                return render(request, "news/main.html", context={"news": items})

        return render(request, "news/main.html", context={"news": HYPERNEWS})


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/create_news.html")

    def post(self, request, *args, **kwargs):
        title = str(request.POST.get("title"))
        text = str(request.POST.get("text"))
        max_news_count = 10000000000
        link = random.randrange(max_news_count)
        while link in NEWS_IDS:
            link = random.randrange(max_news_count)
        NEWS_IDS.append(link)
        created = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        if text and title:
            HYPERNEWS.append({"title": title, "text": text, "link": link, "created": created})
        return redirect('/news/')