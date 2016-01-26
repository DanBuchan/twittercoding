import requests
import json
import csv
import pprint
import oauth2 as oauth
import urllib.parse

from io import StringIO

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from coding.models import Tweet, Code, Category, Feature
from coding.forms import UserForm, UserProfileForm, TweetForm

@login_required
def summary(request):
    tweet_count = Tweet.objects.all().count()

    codings = Code.objects.values_list('tweet', flat=True).distinct()
    coded_tweets = Tweet.objects.filter(id__in=codings)

    coding_counts = {}
    users = User.objects.all()
    for user in users:
        codes = Code.objects.filter(user=user).all()
        user_counts = {}
        for code in codes:
            user_counts.setdefault(str(code.category), {})[str(code.feature)] = 0
        for code in codes:
            user_counts[str(code.category)][str(code.feature)]+=1

        coding_counts[str(user)]=user_counts


    context_dict = {'tweet_count': tweet_count,
                    'coded_count': len(coded_tweets),
                    'coding_counts': coding_counts,
                    }
    return render(request, 'coding/summary.html', context_dict)

@login_required
def upload(request):
    if request.method == 'POST':
        file = request.FILES['csv_file']
        f = StringIO(file.read().decode())
        data = [row for row in csv.reader(f.read().splitlines())]

        for row in data:
            if len(row[0]) < 1:
                continue
            reply_to = [word for word in row[6].split() if word.startswith('@')]
            reply_to = [s.rstrip(':') for s in reply_to]
            reply_to = ', '.join(reply_to)

            t = Tweet(tweet_id=int(row[1]), timestamp=int(row[2]),
                      user_name=row[3], label=row[7], tweet_text=row[6],
                      reply_to=reply_to)
            t.save()
        return HttpResponse("Tweets Uploaded.")
    else:
        return render(request, 'coding/upload.html', {})


def dump(request):
    pp = pprint.PrettyPrinter(indent=4)

    coded = Code.objects.values('tweet', ).distinct()
    coded_tweets = Tweet.objects.filter(id__in=coded)

    contents = "tweet_id,username,label,user"
    categories = Category.objects.all()
    for cat in categories:
        contents += ","+str(cat)
    contents += "\n"

    annotations = {}
    for tweet in coded_tweets:

        print(tweet)
        codings = Code.objects.filter(tweet=tweet).all()
        pp.pprint(codings)
        for code in codings:
            annotations.setdefault(str(code.user), {})[str(code.category)] = str(code.feature)

        for user in annotations:
            contents += str(tweet.tweet_id)+","+tweet.user_name+","+tweet.label+","+user
            codes = annotations[user]
            for cat in categories:
                if str(cat) in codes:
                    contents += ","+codes[str(cat)]
                else:
                    contents += ",NOT CODED"
            contents += "\n"
    #return HttpResponse(contents, content_type='text/plain')
    response = HttpResponse(contents, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=codings.csv'
    return response


def get_tweet(tweet):
    embedded_tweet = "<div></div>"
    # print(tweet.tweet_id)
    try:
        twitter_embed_url = "https://api.twitter.com/1/statuses/oembed.json?hide_media=1&id="+str(tweet.tweet_id)
        r = requests.get(twitter_embed_url)
        embed_json = r.json()
        #print(embed_json)
        embedded_tweet = embed_json['html']
    except:
        # send to log in future
        embedded_tweet = "<div class='col-sm-4 col-md-4' style='background:#d9d9d9;' ><h3>Tweet Could Not Be Retrieved</h3><h3>User: "+tweet.user_name+"</h3><h4>Stored Text: "+tweet.tweet_text+"</h4></div>"
    return(embedded_tweet)


def tweet(request, tweet_id):
    tweet = Tweet.objects.get(tweet_id=tweet_id)
    categories = Category.objects.all()
    codes = Code.objects.filter(tweet=tweet).all()

    context_dict = {'tweet': tweet,
                    'embedded_tweet': get_tweet(tweet),
                    'categories': categories,
                    'codes': codes,
                    }
    return render(request, 'coding/tweet.html', context_dict)


def get_db_info(current_user, form, error):

    codings = Code.objects.filter(user=current_user).values_list('tweet', flat=True).distinct()
    coded_tweets = Tweet.objects.filter(id__in=codings)
    total = Tweet.objects.filter(label=current_user.userprofile.tweet_label).count()
    coded = Tweet.objects.filter(id__in=codings).count()
    uncoded = total-coded
    tweet_list = Tweet.objects.filter(label=current_user.userprofile.tweet_label).exclude(id__in=codings).order_by('-tweet_id')[:1]
    coding_message = "You are currently coding for tweets marked "+current_user.userprofile.tweet_label
    progress_message = "You have coded "+str(coded)+" "+current_user.userprofile.tweet_label+" tweets. There are "+str(uncoded)+" to do."
    categories = Category.objects.all()
    # here we should get the tweet html as per the twitter API

    child_cats = {}
    for cat in categories:
        for feat in cat.features.all():
            if feat.child_category:
                child_cats[feat.child_category] = feat

    #revisit this for embedded bios
    embedded_tweet = ''
    replies = None
    for tweet in tweet_list:
        embedded_tweet = get_tweet(tweet)
        #embedded_bio = get_bio(tweet.user_name)
        #embedd_reply = ''
        if len(tweet.reply_to) > 0:
            replies = tweet.reply_to.split(", ")
            #embedded_reply = get_bio(replies[0])
            replies = ["https://twitter.com/intent/user/?screen_name="+s for s in replies]



    context_dict = {'tweets': tweet_list,
                    'embedded_tweet': embedded_tweet,
                    'label': current_user.userprofile.tweet_label,
                    'todo': uncoded,
                    'done': coded,
                    'form': form,
                    'error': error,
                    'categories': categories,
                    'coding_message': coding_message,
                    'progress_message': progress_message,
                    'replies': replies,
                    'child_cats': child_cats}
    return(context_dict)

@login_required
def index(request):
    current_user = request.user

    if current_user.username == "admin":
        return render(request, 'coding/login.html', {})
    # get a tweet's data

    # save or prepare the tweet coding form
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = Tweet.objects.get(tweet_id=request.POST['tweet_id'])
            child_count = int(request.POST['children_count'])

            # Save the new category to the database.

            # check we have recieved a selection for each radio button
            total_cats = Category.objects.all().count()
            cat_count = 0
            for key in request.POST:
                if key.startswith("category"):
                    cat_count += 1

            # if yes save each one to code
            if cat_count >= (total_cats-child_count):
                for key in request.POST:
                    if key.startswith("category"):
                        cat_key = key.lstrip("category_")
                        cat = Category.objects.get(pk=cat_key)
                        feat = Feature.objects.get(pk=request.POST[key])
                        c = Code(tweet=tweet, category=cat, feature=feat, user=current_user)
                        c.save()
            else:
                context_dict = get_db_info(current_user, form, 'Please make selections for all categories')
                return render(request, 'coding/index.html', context_dict)
            # Now call the index() view.
            # The user will be shown the homepage.
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = TweetForm()

    context_dict = get_db_info(current_user, form, '')
    return render(request, 'coding/index.html', context_dict)
# Create your views here.


def register(request):
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'coding/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/coding/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Coding account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'coding/login.html', {})

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/coding/')
