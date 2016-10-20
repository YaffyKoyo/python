from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from queue.models import QueueItem
from django.core.context_processors import csrf
from django.template import loader
from django.core.cache import cache

def index(request):
    t = loader.get_template("index.html")
    queue = QueueItem.objects.order_by("id")
    c = {'queue':queue}
    c.update(csrf(request))
    html = t.render(c)
    return HttpResponse(html)

def add(request):
    item = QueueItem(text=request.POST["text"])
    item.save()
    return HttpResponse("<li>%s</li>" % item.text)

def remove(request):
    items = QueueItem.objects.order_by("id")[:1]
    if len(items)!=0:
        items[0].delete()
    return redirect("/")

def memcached_test(request):
    cache_key = "string"
    result = cache.get(cache_key)
    if result is None:
        data = "hello, found"
        cache.set(cache_key, data, 60)
        return HttpResponse(result)
    else:
        return HttpResponse(result)