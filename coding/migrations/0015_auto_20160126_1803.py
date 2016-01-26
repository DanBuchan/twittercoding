# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0014_remove_userprofile_recoder'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='constituency',
            field=models.CharField(null=True, max_length=256),
        ),
        migrations.AddField(
            model_name='tweet',
            name='full_name',
            field=models.CharField(null=True, max_length=256),
        ),
        migrations.AddField(
            model_name='tweet',
            name='gender',
            field=models.CharField(null=True, max_length=100),
        ),
        migrations.AddField(
            model_name='tweet',
            name='party_name',
            field=models.CharField(null=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='code',
            name='tweet',
            field=models.ForeignKey(related_name='coding', to='coding.Tweet', null=True),
        ),
        migrations.AlterField(
            model_name='feature',
            name='child_category',
            field=models.ForeignKey(blank=True, related_name='child_category', to='coding.Category', null=True),
        ),
    ]
