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
	attendees = ArrayField(models.CharField(max_length=50), blank=True, null=True)
	# created = models.DateTimeField(null=True, blank=True, input_formats=["%d/%m/%Y %H:%M:%S"])



class Event(models.Model):
	organiser = models.CharField("organiser", max_length=50)
	event_name = models.CharField("event_name", max_length=50)
	location = models.CharField("location", max_length=50)
	start_time = models.DateTimeField(null=True, blank=True)
	finish_time = models.DateTimeField(null=True, blank=True)
	attendees = ArrayField(models.CharField(max_length=50), blank=True, null=True)
	attending = ArrayField(models.CharField(max_length=50), blank=True, null=True)
	attendance_required = models.BooleanField(default=False)



class Attempt(models.Model):
	username = models.CharField("username", max_length=50)
	event_id = models.IntegerField("event_id")
	created = models.DateTimeField(auto_add_now=True)
	time_on_screen = models.DateTimeField(null=True, blank=True)
	date_on_screen = models.DateTimeField(null=True, blank=True)
