from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import os
import hmac
import settings
from .models import *
from .serializers import *


@csrf_exempt
def musician_list(request):
	if request.method == 'GET':
		musicians = Musician.objects.all()
		serializer = MusicianSerializer(musicians, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = MusicianSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def musician_detail(request, pk):
	"""
	CRUD methods for Musician model
	"""
	try:
		musician = Musician.objects.get(pk=pk)
	except Musician.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = MusicianSerializer(musician)
		return JsonResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = MusicianSerializer(musician, data=data)
		authenticator = hmac.new(
		        key = settings.SECRET_KEY.encode('utf-8'),
      			msg = os.urandom(32),
        		digestmod = 'sha256',
    		    ).hexdigest()
		if serializer.is_valid():
			serializer.save()
			try:
				auth = Authenticator.objects.get(pk=pk)
				return HttpResponse("<h1>Authenticator already exists</h1>")
			except Authenticator.DoesNotExist:
				//SAVE AUTHENTICATOR
				return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		musician.delete()
		return HttpResponse(status=204)

@csrf_exempt
def sample_list(request):
	if request.method == 'GET':
		samples = Sample.objects.all()
		serializer = SampleSerializer(samples, many=True)
		return JsonResponse(serializer.data, safe=False)

	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = SampleSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def sample_detail(request, pk):
	"""
	CRUD methods for Musician model
	"""
	try:
		sample = Sample.objects.get(pk=pk)
	except Sample.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = SampleSerializer(sample)
		return JsonResponse(serializer.data)

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

@csrf_exempt
def sample_pack_list(request):
	if request.method == 'GET':
		samplePacks = SamplePack.objects.all()
		serializer = SamplePackSerializer(samplePacks, many=True)
		return JsonResponse(serializer.data, safe=False)

	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = SamplePackSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def sample_pack_detail(request, pk):
	"""
	CRUD methods for SamplePack model
	"""
	try:
		samplePack = SamplePack.objects.get(pk=pk)
	except SamplePack.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = SamplePackSerializer(samplePack)
		return JsonResponse(serializer.data)

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

@csrf_exempt
def samples_in_pack(request, pk):
    try:
        sample_pack = SamplePack.objects.get(pk=pk)
    except Sample.DoesNotExist:
        return HttpResponse(status=404)
    samples = Sample.objects.filter(pack=pk)

    serializer = SampleSerializer(samples, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def top5_sample_packs(request):
    samplePacks = SamplePack.objects.order_by('-purchase_count')[:5]
    serializer = SamplePackSerializer(samplePacks, many=True)
    return JsonResponse(serializer.data, safe=False)


