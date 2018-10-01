from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Musician, Sample, SamplePack

class MusicianSerializer(serializers.HyperLinkedModelSerializer):
	class Meta:
		model = Musician
		fields = ('url', 'name', 'minute_length', 'second_length', 'pack')

class SamplePackSerializer(serializers.HyperLinkedModelSerializer):
	class Meta:
		model = SamplePack
		fields = ('url', 'name', 'description', 'purchase_count', 
			'price', 'num_samples', 'buyers', 'current_seller')

class MusicianSerializer(serializers.HyperLinkedModelSerializer):
	class Meta:
		model = Musician
		fields = ('url', 'user', 'follower_count', 'balance', 'rating')