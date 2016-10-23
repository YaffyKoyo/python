from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from queue.models import QueueItem
from django.core.context_processors import csrf
from django.template import loader
from mysite import test

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
    temp = test.MCClone('None',None)
    cache_key = "string"
    result = temp.get(cache_key)
    if result is None:
        data = "hello, found"
        temp.set(cache_key, data, 5)
        return HttpResponse(result)
    else:
        return HttpResponse(result)