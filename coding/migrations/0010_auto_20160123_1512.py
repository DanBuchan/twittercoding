# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0009_userprofile_recoder'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='category',
            field=models.ForeignKey(null=True, to='coding.Category'),
        ),
        migrations.AddField(
            model_name='code',
            name='feature',
            field=models.ForeignKey(null=True, to='coding.Feature'),
        ),
        migrations.AddField(
            model_name='code',
            name='tweet',
            field=models.ForeignKey(null=True, to='coding.Tweet'),
        ),
    ]
