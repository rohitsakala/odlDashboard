# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-09 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0018_performancegraphs_jenkinsjobname'),
    ]

    operations = [
        migrations.AddField(
            model_name='performancegraphs',
            name='wikiName',
            field=models.CharField(default='nothing', max_length=1000),
            preserve_default=False,
        ),
    ]