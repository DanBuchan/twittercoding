import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twittercoding.settings')

import django
django.setup()

from coding.models import Tweet, Code, Category, Feature


def populate():
    Tweet.objects.all().delete()
    add_tweet(596515623053750272, 1431048181, "_AlexSanderson", "LAB",
              "RT @peter_graham: Although @HFLabour take their lead from "
              "Hollande, a small step towards Sarkozy in @_AlexSanderson's "
              "loser's speech... htt…")

    c = add_category("Politics")

    add_feature(c, "internal")
    add_feature(c, "external")



def add_tweet(tweet_id, timestamp, user_name, party_code, tweet_text):
    t = Tweet.objects.get_or_create(tweet_id=tweet_id, timestamp=timestamp)[0]
    t.timestamp = timestamp
    t.user_name = user_name
    t.party_code = party_code
    t.tweet_text = tweet_text
    t.save()
    return(t)


def add_category(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return(c)


def add_feature(cat, name):
    f = Feature.objects.get_or_create(category=cat, name=name)[0]
    f.save()
    return(f)

# Start execution here!
if __name__ == '__main__':
    print("Starting population script...")
    populate()
