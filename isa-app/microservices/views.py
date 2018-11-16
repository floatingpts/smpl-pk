from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import datetime
from .models import *
from .serializers import *
import os
import hmac

# import django settings file
import microservices.settings

@csrf_exempt
def generate_auth(pk):
  auth = hmac.new(
       key = settings.SECRET_KEY.encode('utf-8'),
       msg = os.urandom(32),
       digestmod = 'sha256',).hexdigest()
  return auth

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
def musician_login(request, user):
  try:
    name = user["username"]
    hashed_pass = user["password"]
    musician = Musician.objects.get(username=name, password=hashed_pass)
    # Generate random auth string
    auth = generate_auth()
    # Check that this random string not already used
    while(Authenticator.objects.filter(authenticator=auth).exists()):
      auth = generate_auth()
    # We now know that string stored in auth is unique,
    # so create new authenticator object
    new_auth = Authenticator.objects.create(user_id=musician.pk, authenticator=auth, date_created=datetime.date.today())
    new_auth.save()
    serializer = AuthenticatorSerializer(new_auth)
    return JsonResponse(serializer.data)

  except Musician.DoesNotExist:
    return HttpResponse(status=404)

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
		if serializer.is_valid():
			serializer.save()
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

@csrf_exempt
def authenticator_list(request):
	if request.method == 'GET':
		authenticators = Authenticator.objects.all()
		serializer = AuthenticatorSerializer(authenticators, many=True)
		return JsonResponse(serializer.data, safe=False)

	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = AuthenticatorSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def authenticator_detail(request, pk):
	"""
	CRUD methods for Authenticator model
	"""
	try:
		authenticator = Authenticator.objects.get(pk=pk)
	except Authenticator.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = AuthenticatorSerializer(authenticator)
		return JsonResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = AuthenticatorSerializer(authenticator, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		authenticator.delete()
		return HttpResponse(status=204)


