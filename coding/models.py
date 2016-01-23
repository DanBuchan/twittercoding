from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tweet(models.Model):
    tweet_id = models.IntegerField(unique=True)
    timestamp = models.IntegerField()
    user_name = models.CharField(max_length=128)
    label = models.CharField(max_length=20, null=True)
    tweet_text = models.CharField(max_length=200)

    coded = models.BooleanField(default=False, blank=False)
    recoded = models.BooleanField(default=False, blank=False)

    # user = link to

    def __str__(self):  # For Python 2, use __str__ on Python 3
        return str(self.tweet_id)


class Code(models.Model):
    primary_coding = models.BooleanField(default=False, blank=False)
    recoding = models.BooleanField(default=False, blank=False)
    # basically this table links tweets to features many-to-many table I guess


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):  # For Python 2, use __str__ on Python 3
        return self.name


class Feature(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=256)

    def __str__(self):  # For Python 2, use __str__ on Python 3
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    tweet_label = models.CharField(max_length=20, null=False)

    def __unicode__(self):
        return self.user.username
