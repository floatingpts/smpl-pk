from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Musician, Sample, SamplePack
from .serializers import SampleSerializer, SamplePackSerializer, MusicianSerializer

# Create your views here.

def musician_crud(request, pk):
	"""
	CRUD methods for Musician model
	"""
	if request.method == 'POST':
		data = JSONParser.parse(request)
		serializer = MusicianSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

	try:
		musician = Musician.objects.get(pk=pk)
	except Musician.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = MusicianSerializer(musician)
		return JsonResponse(musician.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = MusicianSerializer(musician, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		musician.delete()
		return HttpResponse(status=204)

def sample_crud(request, pk):
	"""
	CRUD methods for Musician model
	"""
	if request.method == 'POST':
		data = JSONParser.parse(request)
		serializer = SampleSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

	try:
		sample = Sample.objects.get(pk=pk)
	except Sample.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = SampleSerializer(sample)
		return JsonResponse(sample.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = SampleSerializer(sample, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		sample.delete()
		return HttpResponse(status=204)

def samplePack_crud(request, pk):
	"""
	CRUD methods for Musician model
	"""
	if request.method == 'POST':
		data = JSONParser.parse(request)
		serializer = SamplePackSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

	try:
		samplePack = SamplePack.objects.get(pk=pk)
	except SamplePack.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = SamplePackSerializer(samplePack)
		return JsonResponse(samplePack.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = SamplePackSerializer(samplePack, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		samplePack.delete()
		return HttpResponse(status=204)
