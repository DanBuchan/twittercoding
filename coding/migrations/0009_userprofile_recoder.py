# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0008_auto_20160123_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='recoder',
            field=models.BooleanField(default=False),
        ),
    ]
