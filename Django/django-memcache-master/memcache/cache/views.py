from django.shortcuts import render, HttpResponse
from django.core.cache import cache
from .forms import *
from .models import *
import timeit

# Create your views here.
def index(request):
    if request.method == 'POST':
        # Gets form and sanitizes data
        qForm = QuestionForm(request.POST)
        if qForm.is_valid():
            qForm.save()

    qForm = QuestionForm()
    return render(request, 'index.html', {'questionForm': qForm})

def db_nocache(request):
    start = timeit.default_timer()
    questions = Question.objects.all()
    stop = timeit.default_timer()
    time_taken = str(stop - start)

    return render(request, 'db_dump.html', {'questions': questions, 'time_taken': time_taken})

def db_cache(request):

    cache_key = '123456789abcdefghij'
    cache_time = 600 # time to live (seconds)

    start = timeit.default_timer()
    questions = cache.get(cache_key)

    # If can't find cache
    if not questions:
        questions = Question.objects.all()
        cache.set(cache_key, questions, cache_time)

    stop = timeit.default_timer()
    time_taken = str(stop - start)

    questions = Question.objects.all()

    return render(request, 'db_dump.html', {'questions': questions, 'time_taken': time_taken})