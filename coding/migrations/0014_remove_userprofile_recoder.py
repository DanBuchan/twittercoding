# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0013_auto_20160125_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='recoder',
        ),
    ]
