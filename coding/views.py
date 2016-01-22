from django.shortcuts import render
from django.http import HttpResponse

from coding.models import Tweet, Code, Category, Feature


def index(request):
    tweet_list = Tweet.objects.order_by('-tweet_id')[:5]
    context_dict = {'tweets': tweet_list}

    return render(request, 'coding/index.html', context_dict)
# Create your views here.
