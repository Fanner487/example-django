# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import SubscriberSerializer
from .models import Subscriber

from django.shortcuts import render

# Create your views here.


class SubscriberView(APIView):
	# This method is overwritten
	def get(self, request):
		return Response({"message": "Hello world!"})

	def post(self, request):

		serializer = SubscriberSerializer(data=request.data)

		if serializer.is_valid():
			
			subscriber_instance = Subscriber.objects.create(**serializer.data)

			return Response({"message": "Created subscriber {}".format(subscriber_instance.id)})
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

