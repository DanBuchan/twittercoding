import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twittercoding.settings')

import django
django.setup()

from coding.models import Tweet, Code, Category, Feature

Tweet.objects.all().delete()
Code.objects.all().delete()
