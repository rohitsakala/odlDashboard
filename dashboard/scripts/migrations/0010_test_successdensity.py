# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-21 06:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0009_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='successDensity',
            field=models.FloatField(default=0),
        ),
    ]
