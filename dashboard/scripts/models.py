from __future__ import unicode_literals

from django.db import models

class Projects(models.Model):
	name = models.CharField(max_length=255)