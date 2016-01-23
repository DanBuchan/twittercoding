# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0007_auto_20160123_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='category',
            field=models.ForeignKey(to='coding.Category', related_name='features'),
        ),
    ]
