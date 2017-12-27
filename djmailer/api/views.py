# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import HelloWorldSerializer

from django.shortcuts import render

# Create your views here.


class HelloWorldView(APIView):
	# This method is overwritten
	def get(self, request):
		return Response({"message": "Hello world!"})

	def post(self, request):

		serializer = HelloWorldSerializer(data=request.data)

		if serializer.is_valid():
			
			valid_data = serializer.data

			name = valid_data.get("name")
			age = valid_data.get("age")

			return Response({"message": "Hello {}, you're {} years old".format(name, age)})
		else:
			return Response({"errors": serializer.errors})

		# name = request.data.get("name")

		# if not name:
		# 	return Response({"error": "No name passed"})
		# return Response({"message": "Hello {}!".format(name)})

# @api_view(["GET", "POST"])
# def hello_world(request):
# 	if request.method == "GET":
# 		return Response({"message": "Hello World!"})

# 	else:
# 		name = request.data.get("name")

# 		if not name:
# 			return Response({"error": "No name passed"})
# 		else:
# 			return Response({"message": "Hello {}!".format(name)})

