# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-30 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
