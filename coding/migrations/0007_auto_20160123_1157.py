# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0006_auto_20160123_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='primary_coding',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='code',
            name='recoding',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tweet',
            name='recoded',
            field=models.BooleanField(default=False),
        ),
    ]
