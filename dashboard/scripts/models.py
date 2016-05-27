from __future__ import unicode_literals

from django.db import models

class Projects(models.Model):
	name = models.CharField(max_length=255,unique=True)

	def __str__(self):
    		return self.name

class Bugs(models.Model):
	projectName =  models.OneToOneField('Projects',on_delete=models.CASCADE)
	unconfirmed = models.IntegerField(default=0)
	confirmed = models.IntegerField(default=0)
	inProgress = models.IntegerField(default=0)
	waitingForReview = models.IntegerField(default=0)
	blocker = models.IntegerField(default=0)
	critical = models.IntegerField(default=0)
	major = models.IntegerField(default=0)
	normal = models.IntegerField(default=0)
	minor = models.IntegerField(default=0)
	trivial = models.IntegerField(default=0)
	enhancement = models.IntegerField(default=0)
	highest = models.IntegerField(default=0)
	high = models.IntegerField(default=0)
	normal = models.IntegerField(default=0)
	low = models.IntegerField(default=0)
	lowest = models.IntegerField(default=0)

class Test(models.Model):
	projectName =  models.OneToOneField('Projects',on_delete=models.CASCADE)
	coverage = models.FloatField(default=0)
	successDensity = models.FloatField(default=0)

class Commit(models.Model):
	projectName =  models.OneToOneField('Projects',on_delete=models.CASCADE)
	totalCount = models.IntegerField(default=0)
	lastWeekCount = models.IntegerField(default=0)