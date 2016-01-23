from django import forms
from django.contrib.auth.models import User

from coding.models import Tweet, Code, Category, Feature, UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['tweet_label'].choices = Tweet.objects.all().values_list("label","label").distinct()

    tweet_label = forms.ChoiceField(choices=[])
    recoder = forms.BooleanField(initial=False)

    class Meta:
        model = UserProfile
        fields = ('tweet_label', 'recoder')


class TweetForm(forms.ModelForm):
    coded = forms.BooleanField(widget=forms.HiddenInput(), initial=True)

    class Meta:
        model = Tweet
        fields = ('coded', )
