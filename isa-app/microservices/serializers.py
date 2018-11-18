from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Musician, Sample, SamplePack, Authenticator

class MusicianSerializer(serializers.ModelSerializer):
	class Meta:
		model = Musician
		fields = ('username', 'email', 'password', 'follower_count', 'balance', 'rating')

class SamplePackSerializer(serializers.ModelSerializer):
	class Meta:
		model = SamplePack
		fields = ('id', 'name', 'description', 'purchase_count',
			'price', 'num_samples', 'buyers', 'current_seller')

class SampleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Sample
		fields = ('id', 'name', 'minute_length', 'second_length', 'pack')

class AuthenticatorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Authenticator
		fields = ('authenticator', 'user_id', 'date_created')
