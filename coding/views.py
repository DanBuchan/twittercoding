import requests
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from coding.models import Tweet, Code, Category, Feature
from coding.forms import UserForm, UserProfileForm, TweetForm


def get_tweet(tweet):
    embedded_tweet = "<div></div>"
    try:
        twitter_embed_url = "https://api.twitter.com/1/statuses/oembed.json?hide_media=1&url=https://twitter.com/Interior/status/"
        r = requests.get(twitter_embed_url+str(tweet.tweet_id))
        embed_json = r.json()
        embedded_tweet = embed_json['html']
    except:
        #send to log in future
        print("Could not get tweet!")
    return(embedded_tweet)


def tweet(request, tweet_id):
    tweet = Tweet.objects.get(tweet_id=tweet_id)
    coding = Code.objects.filter(tweet=tweet, primary_coding=True).all()
    recoding = Code.objects.filter(tweet=tweet, recoding=True).all()
    categories = categories = Category.objects.all()

    context_dict = {'tweet': tweet,
                    'embedded_tweet': get_tweet(tweet),
                    'coding': coding,
                    'recoding': recoding,
                    'categories': categories,
                    }
    return render(request, 'coding/tweet.html', context_dict)

def get_db_info(current_user, form, error):
    coded = Tweet.objects.filter(label=current_user.userprofile.tweet_label, coded=True).count()
    uncoded = Tweet.objects.filter(label=current_user.userprofile.tweet_label, coded=False).count()
    tweet_list = Tweet.objects.filter(label=current_user.userprofile.tweet_label, coded=False).order_by('-tweet_id')[:1]
    coding_message = "You are currently coding for tweets marked "+current_user.userprofile.tweet_label
    progress_message = "You have coded "+str(coded)+" "+current_user.userprofile.tweet_label+" tweets. There are "+str(uncoded)+" to do."
    if current_user.userprofile.recoder == True:
        coded = Tweet.objects.filter(coded=True, recoded=True).count()
        uncoded = Tweet.objects.filter(coded=True, recoded=False).count()
        tweet_list = Tweet.objects.filter(coded=True, recoded=False).order_by('?')[:1]
        coding_message = "You are currently recoding randomised tweets"
        progress_message = "You have recoded "+str(coded)+" tweets. There are "+str(uncoded)+" to do."
    categories = Category.objects.all()
    # here we should get the tweet html as per the twitter API

    embedded_tweet = ''
    for tweet in tweet_list:
        embedded_tweet = get_tweet(tweet)

    context_dict = {'tweets': tweet_list,
                    'embedded_tweet': embedded_tweet,
                    'label': current_user.userprofile.tweet_label,
                    'todo': uncoded,
                    'done': coded,
                    'form': form,
                    'error': error,
                    'categories': categories,
                    'coding_message': coding_message,
                    'progress_message': progress_message,}
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
            #print(request.POST)
            tweet = Tweet.objects.get(tweet_id=request.POST['tweet_id'])
            # Save the new category to the database.

            #check we have recieved a selection for each radio button
            total_cats = Category.objects.all().count()
            cat_count = 0
            for key in request.POST:
                if key.startswith("category"):
                    cat_count+=1

            #if yes save each one to code
            if cat_count == total_cats:
                for key in request.POST:
                    if key.startswith("category"):
                        cat_key = key.lstrip("category_")
                        cat = Category.objects.get(pk=cat_key)
                        feat = Feature.objects.get(pk=request.POST[key])
                        if current_user.userprofile.recoder == True:
                            c = Code(recoding=True, tweet=tweet, category=cat, feature=feat)
                            c.save()
                        else:
                            c = Code(primary_coding=True, tweet=tweet, category=cat, feature=feat)
                            c.save()
            else:
                context_dict = get_db_info(current_user, form, 'Please make selections for all categories')
                return render(request, 'coding/index.html', context_dict)
            # Now call the index() view.
            # The user will be shown the homepage.

            tweet = Tweet.objects.get(tweet_id=request.POST['tweet_id'])
            if current_user.userprofile.recoder == True:
                tweet.recoded = True
            else:
                tweet.coded = True
            tweet.save()

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
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


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
