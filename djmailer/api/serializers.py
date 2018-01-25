from rest_framework import serializers
from .models import Subscriber, Event, Attempt
from django.contrib.auth.models import User
from datetime import datetime 

class SubscriberSerializer(serializers.ModelSerializer):
	# name = serializers.CharField(max_length=50)
	# age = serializers.IntegerField()
	# email = serializers.EmailField()

	def validate(self, data):

		if not data.get('name') == 'Eamon Tang':
			raise serializers.ValidationError("Wrong name nigguh")
		else:
			print("\n\nValue:" +  data['name'] + "\n\n")
		
		return data


	class Meta:
		model = Subscriber
		fields = "__all__"
		# exclude = ('created',)


class EventSerializer(serializers.ModelSerializer):

	def validate(self, data):

		username= data.get('organiser').strip()
		start_time = data.get('start_time')
		finish_time = data.get('finish_time')
		attendees = data.get('attendees')

		print("Start time: " + str(start_time))
		print("End time: " + str(finish_time))
		print("Attending: " + str(data.get('attending')))

		# ignores case
		users = User.objects.filter(username__iexact=username)

		# Checks if user exists
		if not users.exists():
			raise serializers.ValidationError("User does not exist")

		# Throw if start time after finish_time
		if start_time > finish_time:
			raise serializers.ValidationError("Invalid time entry")

		# Checks every username in attendee list
		for attendee in attendees:
			user = User.objects.filter(username__iexact=attendee.strip())
			
			if not user.exists():
				raise serializers.ValidationError(attendee + " does not exist")

		# Attending must be empty
		if data.get('attending'):
			raise serializers.ValidationError("Attending must be empty")
		
		return data


	class Meta:
		model = Event
		fields = "__all__"
		# exclude = ('created',)


class AttemptSerializer(serializers.ModelSerializer):
	# name = serializers.CharField(max_length=50)
	# age = serializers.IntegerField()
	# email = serializers.EmailField()

	# def validate(self, data):

	# 		if not data.get('name') == 'Eamon Tang':
	# 			raise serializers.ValidationError("Wrong name")
	# 		else:
	# 			print("\n\nValue:" +  data['name'] + "\n\n")
			
	# 		return data

	class Meta:
		model = Attempt
		fields = "__all__"
		# exclude = ('created',)

		


# class UserSerializer(serializers.ModelSerializer)