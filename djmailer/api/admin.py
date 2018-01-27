# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Subscriber, Event, Attempt
# Register your models here.

class AttemptAdmin(admin.modelAdmin):
	readonly_fields = ('time_created',)

admin.site.register(Subscriber)
admin.site.register(Event)
admin.site.register(Attempt, AttemptAdmin)
