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
		created = data.get('time_created')

		print("Created: " + str(data))

		# Checks if user exists
		if not user_exists(username.strip()):
			raise serializers.ValidationError("User does not exist")

		# Checks if event exists
		if not event_exists(event_id):
			raise serializers.ValidationError("Event does not exist")

		

		# Check if user exists in attendee list and not already in attending 
		user_is_attendee(username, event_id)
		# If user is attendee, add to list with verification
		verify_scan(data)
		return data

	class Meta:
		model = Attempt
		fields = "__all__"
		read_only_fields = ('time_created',)
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


	if event_count == 1:
		return True
	else:
		return False

def user_is_attendee(username, event_id):

	if user_exists(username) and event_exists(event_id):

		event = Event.objects.filter(id=event_id) \
			.filter(attendees__icontains=username.strip().lower()) \
			.exclude(attending__icontains=username.strip().lower())

		# If there's only one entry of event and is exists
		if event.exists() and event.count() == 1:
			print(username + " exists in " + str(event_id))
			# Add to attending
			add_to_attending(username, event_id)

			return True
		else:
			print(username + " does not exist in " + str(event_id) + " or is already in there")
			return False

	else:
		return False

def verify_scan(data):
	print("bleh")

	event = Event.objects.get(id=data.get('event_id'))

	print(data.get('id'))



	event_start_date = event.start_time.date()
	event_finish_date = event.finish_time.date()
	event_start_time = event.start_time.time()
	event_finish_time = event.finish_time.time()

	new_date_on_screen = data.get('date_on_screen').date()
	new_time_on_screen = data.get('time_on_screen').time()

	print("event_start_date: " + str(event_start_date))
	print("event_finish_date: " + str(event_finish_date))
	print("event_start_time: " + str(event_start_time))
	print("event_finish_time: " + str(event_finish_time))
	print("new_date_on_screen: " + str(new_date_on_screen))
	print("new_time_on_screen: " + str(new_time_on_screen))

	verified = True

	# Check dates
	if event_start_date <= new_date_on_screen <= event_finish_date:
		print("Within date")
	else:
		verified = False

	# Check times
	if event_start_time <= new_time_on_screen <= event_finish_time:
		print("Within time")
	else:
		verified = False

	# Check if there's past entry around same time
	# past_attempts = Attempt.objects.filter
	print(str(data.get('time_created')))
	# time_interval = data.get('created').time() - 10
	# print(time_interval)
	# print(data.get('created').time())

	# Check times
	return verified



def add_to_attending(username, event_id):

	event = Event.objects.get(id=event_id)

	if not username in event.attending:
		print("Appending user")
		event.attending.append(username.strip().lower())

		return True
	else:
		return False

	event.save()

# class UserSerializer(serializers.ModelSerializer)