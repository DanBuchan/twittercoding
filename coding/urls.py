from django.conf.urls import patterns, url
from coding import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^index/$', views.index, name='index_form'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^tweet/(?P<tweet_id>[\w\-]+)/$', views.tweet, name='tweet'),
        url(r'^dump/$', views.dump, name='dump'),
        url(r'^upload/$', views.upload, name='upload'),
        url(r'^summary/$', views.summary, name='summary'),
        )
