# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response

from django.shortcuts import render

# Create your views here.


def hello_world(request):
	return JsonResponse({"message": "Hello world!"})
