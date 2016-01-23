# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0003_tweet_coded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='party_code',
        ),
        migrations.AddField(
            model_name='tweet',
            name='label',
            field=models.CharField(null=True, max_length=20),
        ),
    ]
