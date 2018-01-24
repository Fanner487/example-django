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
		end_time = data.get('end_time')

		print("Start time: " + str(start_time))
		print("End time: " + str(end_time))

		# ignores case
		users = User.objects.filter(username__iexact=username)

		# Checks if user exists
		if not users.exists():
			raise serializers.ValidationError("User does not exist")

		# Throw if start time after end_time
		if start_time > end_time:
			raise serializers.ValidationError("Invalid time entry")
		
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