from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^db_cache/?$', views.db_cache, name='db_cache'),
    url(r'^db_nocache/?$', views.db_nocache, name='db_nocache'),
]