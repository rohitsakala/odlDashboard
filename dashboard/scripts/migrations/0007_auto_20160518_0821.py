# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-18 08:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0006_auto_20160518_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bugs',
            name='projectName',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scripts.Projects'),
        ),
    ]