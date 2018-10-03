from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Musician, Sample, SamplePack

class MusicianSerializer(serializers.ModelSerializer):
	class Meta:
		model = Musician
		fields = ('id', 'user', 'follower_count', 'balance', 'rating')

class SamplePackSerializer(serializers.ModelSerializer):
	class Meta:
		model = SamplePack
		fields = ('id', 'name', 'description', 'purchase_count', 
			'price', 'num_samples', 'buyers', 'current_seller')

class SampleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Sample
		fields = ('id', 'name', 'minute_length', 'second_length', 'pack')




