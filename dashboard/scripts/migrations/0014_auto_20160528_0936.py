# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-28 09:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0013_auto_20160528_0725'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contributors',
            unique_together=set([('projectName', 'contributorName')]),
        ),
    ]
