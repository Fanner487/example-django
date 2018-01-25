from rest_framework import serializers
from .models import Subscriber, Event, Attempt
from django.contrib.auth.models import User
from datetime import datetime 
import pytz

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

		utc = pytz.UTC # using timezomes for time checking

		username= data.get('organiser').strip()
		start_time = data.get('start_time').replace(tzinfo=utc)
		finish_time = data.get('finish_time').replace(tzinfo=utc)
		attendees = data.get('attendees')
		time_now = datetime.now().replace(tzinfo=utc)

		print("Start time: " + str(start_time))
		print("End time: " + str(finish_time))
		print("Attending: " + str(data.get('attending')))

		# Checks if user exists
		if not user_exists(username.strip()):
			raise serializers.ValidationError("User does not exist")

		# Throw if start time after finish_time
		if start_time >= finish_time:
			raise serializers.ValidationError("Invalid time entry")

		if start_time < time_now or finish_time < time_now:
			raise serializers.ValidationError("Time must be in future")

		# Checks every username in attendee list
		for attendee in attendees:
			
			if not user_exists(attendee.strip()):
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

	# username = models.CharField("username", max_length=50)
	# event_id = models.IntegerField("event_id")
	# created = models.DateTimeField(auto_now_add=True)
	# time_on_screen = models.DateTimeField(null=True, blank=True)
	# date_on_screen = models.DateTimeField(null=True, blank=True)

	def validate(self, data):

		username = data.get('username').strip()
		event_id = data.get('event_id')
		time_on_screen = data.get('time_on_screen')
		date_on_screen = data.get('date_on_screen')

		# Checks if user exists
		if not user_exists(username.strip()):
			raise serializers.ValidationError("User does not exist")

		# Checks if event exists
		if not event_exists(event_id):
			raise serializers.ValidationError("Event does not exist")

		user_is_attendee(username, event_id)

		# Check if user exists in attendee list and not already in attending 

		return data

	class Meta:
		model = Attempt
		fields = "__all__"
		# exclude = ('created',)


# Checks if user exists with only one entry
def user_exists(username):
	user_count = User.objects.filter(username__iexact=username.strip()).count()

	if user_count == 1:
		return True
	else:
		return False


def event_exists(event_id):

	event_count = Event.objects.filter(id=event_id).count()
	
	event = Event.objects.filter(id=event_id)

	print(event)
	print(event_count)

	if event_count == 1:
		return True
	else:
		return False

def user_is_attendee(username, event_id):


	if user_exists(username):

		if event_exists(event_id):

			event = Event.objects.filter(id=event_id).filter(attendees__icontains=username.strip().lower())

			# if username.strip().lower() in event.attendees:
			if event.exists() and event.count() == 1:
				print(username + " exists in " + str(event_id))
			else:
				print(username + " does not exists in " + str(event_id))


		else:
			return False

	else:
		return False



# class UserSerializer(serializers.ModelSerializer)