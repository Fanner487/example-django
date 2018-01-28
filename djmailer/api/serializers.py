from rest_framework import serializers
from .models import Subscriber, Event, Attempt
from django.contrib.auth.models import User
from datetime import datetime 
from django.utils import timezone 
import pytz

class SubscriberSerializer(serializers.ModelSerializer):

	def validate(self, data):

		if not data.get('name') == 'Eamon Tang':
			raise serializers.ValidationError("Wrong name ")
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

	def validate(self, data):

		now = timezone.now()
		print("Time now: " + str(now))

		username = data.get('username').strip()
		event_id = data.get('event_id')
		time_on_screen = data.get('time_on_screen')
		date_on_screen = data.get('date_on_screen')

		# Setting time_created to now
		data['time_created'] = now 


		created = data.get('time_created')

		print("Created: " + str(created))

		# Checks if user exists
		if not user_exists(username.strip()):
			raise serializers.ValidationError("User does not exist")

		# Checks if event exists
		if not event_exists(event_id):
			raise serializers.ValidationError("Event does not exist")

	
		# Check if user exists in attendee list and not already in attending 
		if not user_is_attendee(username, event_id):
			raise serializers.ValidationError("User is not in attendees or already in list")

		# If user is attendee, add to list with verification
		# Doesn't need to raise Validation error, needs to check for duplicates
		verify_scan(data)

		return data

	class Meta:
		model = Attempt
		fields = "__all__"
		# fields = ('id', 'username', 'event_id', 'time_on_screen', 'date_on_screen', 'time_created')
		read_only_fields = ('time_created',)
		# exclude = ('created',)


def verify_scan(data):

	username = data.get('username')
	event_id = data.get('event_id')
	time_on_screen = data.get('time_on_screen')
	date_on_screen = data.get('date_on_screen')
	current_created = data.get('time_created')

	verified = True

	# Verifies current attempt
	if valid_attempt_in_event(username, event_id, time_on_screen, date_on_screen, current_created):
		print("Woooo")

		# Gets last attempt
		last_attempt = Attempt.objects.filter(username=username).filter(event_id=event_id).order_by("-time_created").first()
		
		if last_attempt:

			# Verifies second attempt for event
			if valid_attempt_in_event(last_attempt.username, last_attempt.event_id, last_attempt.time_on_screen, last_attempt.date_on_screen, last_attempt.time_created):

				# Check if time within 10 seconds of last
				seconds_difference = (current_created - last_attempt.time_created).total_seconds()
				delta = 10

				# Makes sure that the current time after alst attempt time and within delta
				if 0 < seconds_difference < delta :

					print("Two attempts within delta")
					add_to_attending(username, event_id)
				else:
					verified = False
					print("Two attempts not within delta")
			else:
				verified = False
		else:

			print("No last attempt")
			verified = False

	else:

		print("Current attempt not valid")
		verified = False

	return verified


def valid_attempt_in_event(username, event_id, time_on_screen, date_on_screen, timestamp):

	event = Event.objects.get(id=event_id)

	event_start_date = event.start_time.date()
	event_finish_date = event.finish_time.date()
	event_start_time = event.start_time.time()
	event_finish_time = event.finish_time.time()

	print("event_start_date: " + str(event_start_date))
	print("event_finish_date: " + str(event_finish_date))
	print("event_start_time: " + str(event_start_time))
	print("event_finish_time: " + str(event_finish_time))
	# print("new_date_on_screen: " + str(new_date_on_screen))
	# print("new_time_on_screen: " + str(new_time_on_screen))

	verified = True

	# Check dates from screen
	if event_start_date <= date_on_screen <= event_finish_date:
		print("Within date")
	else:
		verified = False

	# Check times from screen
	if event.sign_in_time.time() <= time_on_screen <= event_finish_time:
		print("Within time")
	else:
		verified = False


	# Check through timestamp
	if event.start_time <= timestamp <= event.finish_time:

		print("Within timezone")
	else:
		verified = False

	# Check screen time within timestamp delta
	print(time_on_screen)
	print(timestamp.time())
	time_difference = (timestamp.time() - time_on_screen).total_seconds()

	# (current_created - last_attempt.time_created).total_seconds()
	print("Time difference to delta: " + str(time_difference))


	return verified


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

		# Checks if user in attendee and not alreadt in attending
		event = Event.objects.filter(id=event_id) \
			.filter(attendees__icontains=username.strip().lower()) \
			.exclude(attending__icontains=username.strip().lower())

		# If there's only one entry of event and is exists
		if event.exists() and event.count() == 1:
			print(username + " exists in " + str(event_id))
			return True
		else:
			print(username + " does not exist in " + str(event_id) + " or is already in there")
			return False

	else:
		return False

def add_to_attending(username, event_id):

	event = Event.objects.get(id=event_id)

	if not username in event.attending:

		print("Appending user")
		event.attending.append(username.strip().lower())
		event.save()

		return True

	else:

		print("Not Appending user")
		return False
