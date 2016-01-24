import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twittercoding.settings')

import django
django.setup()

from coding.models import Tweet, Code, Category, Feature


def populate():
    Tweet.objects.all().delete()
    Category.objects.all().delete()
    Feature.objects.all().delete()
    Code.objects.all().delete()

    add_tweet(596515623053750272, 1431048181, "_AlexSanderson", "LAB",
              "RT @peter_graham: Although @HFLabour take their lead from "
              "Hollande, a small step towards Sarkozy in @_AlexSanderson's "
              "loser's speech... htt…", "@peter_graham, @HFLabour")

    add_tweet(596393240946958336, 1431019003, "_AlexSanderson", "LAB",
              "RT @domjhales: Good luck @_AlexSanderson this evening in "
              "Chelsea and Fulham. @d_hasler and I voted for you and #labour "
              "this morning", "")

    add_tweet(594139875223437312, 1430481759, "_RachelGilmour", "LIBDEM",
              "@alexquantock bc I'm local. Raised in Welly. So I care about "
              "this area. My CV suits issues like farming+flooding.", "")

    c = add_category("Politics")
    add_feature(c, "internal")
    add_feature(c, "external")



def add_tweet(tweet_id, timestamp, user_name, label, tweet_text, reply_to):
    t = Tweet.objects.get_or_create(tweet_id=tweet_id, timestamp=timestamp)[0]
    t.timestamp = timestamp
    t.user_name = user_name
    t.label = label
    t.tweet_text = tweet_text
    t.reply_to = reply_to
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
