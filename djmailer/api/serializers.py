from rest_framework import serializers
from .models import Subscriber

class SubscriberSerializer(serializers.Serializer):
	# name = serializers.CharField(max_length=50)
	# age = serializers.IntegerField()
	# email = serializers.EmailField()

	class Meta:
		model = Subscriber
		fields = "__all__"