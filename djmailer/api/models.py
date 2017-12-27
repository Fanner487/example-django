# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Subscriber(models.Model):
	name = models.CharField("Name", max_length=50)
	age = models.IntegerField("Age")
	email = models.EmailField("Email")