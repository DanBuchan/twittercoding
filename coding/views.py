from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from coding.models import Tweet, Code, Category, Feature
from coding.forms import UserForm, UserProfileForm, TweetForm


@login_required
def index(request):
    current_user = request.user
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
                        c = Code(primary_coding=True, tweet=tweet, category=cat, feature=feat)
                        c.save()
            else:
                coded = Tweet.objects.filter(label=current_user.userprofile.tweet_label, coded=True).count()
                uncoded = Tweet.objects.filter(label=current_user.userprofile.tweet_label, coded=False).count()
                tweet_list = Tweet.objects.filter(label=current_user.userprofile.tweet_label, coded=False).order_by('-tweet_id')[:1]
                categories = Category.objects.all()

                # here we should get the tweet html as per the twitter API
                context_dict = {'tweets': tweet_list,
                                'label': current_user.userprofile.tweet_label,
                                'todo': uncoded,
                                'done': coded,
                                'form': form,
                                'error': "YOU MUST MAKE A SELECTION FOR ALL CATEGORIES",
                                'categories': categories}
                return render(request, 'coding/index.html', context_dict)
            # Now call the index() view.
            # The user will be shown the homepage.

            tweet = Tweet.objects.get(tweet_id=request.POST['tweet_id'])
            tweet.coded = True
            tweet.save()

        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = TweetForm()

    coded = Tweet.objects.filter(label=current_user.userprofile.tweet_label, coded=True).count()
    uncoded = Tweet.objects.filter(label=current_user.userprofile.tweet_label, coded=False).count()
    tweet_list = Tweet.objects.filter(label=current_user.userprofile.tweet_label, coded=False).order_by('-tweet_id')[:1]
    categories = Category.objects.all()

    # here we should get the tweet html as per the twitter API
    context_dict = {'tweets': tweet_list,
                    'label': current_user.userprofile.tweet_label,
                    'todo': uncoded,
                    'done': coded,
                    'form': form,
                    'error': '',
                    'categories': categories}

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
