# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coding', '0012_tweet_reply_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code',
            name='primary_coding',
        ),
        migrations.RemoveField(
            model_name='code',
            name='recoding',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='coded',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='recoded',
        ),
        migrations.AddField(
            model_name='code',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feature',
            name='child_category',
            field=models.ForeignKey(to='coding.Category', related_name='child_category', null=True),
        ),
    ]
