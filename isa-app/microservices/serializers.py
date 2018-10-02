from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Musician, Sample, SamplePack

class MusicianSerializer(serializers.Serializer):
	class Meta:
		model = Musician
		fields = ('url', 'user', 'follower_count', 'balance', 'rating')

class SamplePackSerializer(serializers.Serializer):
	class Meta:
		model = SamplePack
		fields = ('url', 'name', 'description', 'purchase_count', 
			'price', 'num_samples', 'buyers', 'current_seller')

class SampleSerializer(serializers.Serializer):
	class Meta:
		model = Sample
		fields = ('url', 'name', 'minute_length', 'second_length', 'pack')




