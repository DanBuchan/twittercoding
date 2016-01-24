# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0011_auto_20160123_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='reply_to',
            field=models.CharField(null=True, max_length=200),
        ),
    ]
