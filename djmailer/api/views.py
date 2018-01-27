# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.viewsets import ModelViewSet
from .serializers import SubscriberSerializer, EventSerializer, AttemptSerializer
from .models import Subscriber, Event, Attempt
from rest_framework.generics import ListCreateAPIView

from django.contrib.auth import authenticate

from django.shortcuts import render

from django.contrib.auth.models import User

# Create your views here.

class EventViewSet(ModelViewSet):

	serializer_class = EventSerializer
	queryset = Event.objects.all()



class AttemptViewSet(ModelViewSet):

	serializer_class = AttemptSerializer
	queryset = Attempt.objects.all()


class SubscriberViewSet(ModelViewSet):

	serializer_class = SubscriberSerializer
	queryset = Subscriber.objects.all()


# class AttemptView(ListCreateAPIView):
# 	serializer_class = AttemptSerializer
# 	queryset = Attempt.objects.all()

# 	def post(self, request):

# 		print("\n\nIn post\n\n")

# 		serializer = AttemptSerializer(data=request.data)

# 		if serializer.is_valid():

# 			attempt_instance = Attempt.objects.create(**serializer.data)

# 			print(serializer.data["username"])
# 			print(serializer.data["event_id"])

# 			# Checks go here

# 			event_id = serializer.data["event_id"]
# 			username = serializer.data["username"]
# 			event = Event.objects.get(id=event_id)

# 			event.attending.append(username)

# 			event.save()


# 			return Response({"message": "Created attempt {}".format(attempt_instance.id)})
# 		else:
# 			return Response({"errors": serializer.errors})

# class SubscriberView(ListCreateAPIView):


# 	serializer_class = SubscriberSerializer
# 	queryset = Subscriber.objects.all()


	# # This method is overwritten
	# def get(self, request):
	# 	all_subscribers = Subscriber.objects.all()
	# 	serialized_subscribers = SubscriberSerializer(all_subscribers, many=True)
	# 	return Response(serialized_subscribers.data)

	# def post(self, request):

	# 	serializer = SubscriberSerializer(data=request.data)

	# 	if serializer.is_valid():
			
	# 		subscriber_instance = Subscriber.objects.create(**serializer.data)

	# 		return Response({"message": "Created subscriber {}".format(subscriber_instance.id)})
	# 	else:
	# 		return Response({"errors": serializer.errors})


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


@api_view(["GET"])
def get_events(request, username, event_type):

	# past, present, upcoming

	username = username.strip().lower()
	event_type = event_type.strip().lower()

	if event_type == "organising":

		organised_events = Event.objects.filter(organiser__iexact=username).order_by('-start_time')
		serialized = EventSerializer(organised_events, many=True)

		return Response(serialized.data)

	elif event_type == "attending":

		attending_events = Event.objects.filter(attendees__icontains=username).order_by('-start_time')

		for event in attending_events:
			print(event.attendees)

		serialized = EventSerializer(attending_events, many=True)

		return Response(serialized.data)

	else: 

		return Response(status=status.HTTP_400_BAD_REQUEST)
	


@api_view(["POST"])
def login(request):
	username = request.data.get("username")
	password = request.data.get("password")

	user = authenticate(username=username, password=password)

	if not user:
		return Response(status=status.HTTP_401_UNAUTHORIZED)
	else: 
		return Response({"message": "Login successful"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def register(request):
	username = request.data.get("username")
	password = request.data.get("password")
	email = request.data.get("email")
	first_name = request.data.get("firstname")
	surname = request.data.get("surname")

	unique, invalid_field = verify_unique_username_email(username, email)


	if unique:
		print("\n\nEmail is unique\n\n")

		new_user = User.objects.create_user(username, email, password)

		new_user.is_active = True
		new_user.first_name = first_name
		new_user.last_name = surname
		new_user.save()

		return Response({"message": "Created account"})
	else:
		return Response({"message": invalid_field + " already exists"})
	


def verify_unique_username_email(username, email):

	usernames = User.objects.filter(username=username)
	emails = User.objects.filter(email=email)

	if not emails.exists() and not usernames.exists():
		return True, "null"
	else:
		if emails.exists():
			return False, "Email"

		elif usernames.exists():
			return False, "Username"
		else:
			return False, "null"

