# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-27 09:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0010_test_successdensity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalCount', models.IntegerField(default=0)),
                ('lastWeekCount', models.IntegerField(default=0)),
                ('projectName', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scripts.Projects')),
            ],
        ),
    ]
