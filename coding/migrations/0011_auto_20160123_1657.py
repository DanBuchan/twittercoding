# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0010_auto_20160123_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tweet_id',
            field=models.IntegerField(db_index=True, unique=True),
        ),
    ]
