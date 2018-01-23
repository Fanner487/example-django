# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime 

# Create your models here.
class Subscriber(models.Model):
	name = models.CharField("Name", max_length=50)
	age = models.IntegerField("Age")
	email = models.EmailField("Email")
	created = models.DateTimeField(null=True, blank=True)
	# created = models.DateTimeField(null=True, blank=True, input_formats=["%d/%m/%Y %H:%M:%S"])



# class Event(models.Model):
# 	organiser = models.CharField("organiser", max_length=50)
# 	event_name = models.CharField("event_name", max_length=50)
# 	location = models.CharField("location", max_length=50)
# 	start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
# 	finish_time = models.DateTimeField(auto_now=False, auto_now_add=False,)
# 	attendees = ArrayField
# 	attending = ArrayField
# 	attendance_required = models 
