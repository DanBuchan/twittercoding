# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0002_auto_20160122_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='coded',
            field=models.BooleanField(default=False),
        ),
    ]
