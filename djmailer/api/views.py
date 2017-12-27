# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render

# Create your views here.


class HelloWorldView(APIView):
	# This method is overwritten
	def get(self, request):
		return Response({"message": "Hello world!"})

