from django.conf.urls import patterns, url
from coding import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'))
