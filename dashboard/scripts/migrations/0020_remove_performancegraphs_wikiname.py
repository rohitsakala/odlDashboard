# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-09 08:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0019_performancegraphs_wikiname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performancegraphs',
            name='wikiName',
        ),
    ]
