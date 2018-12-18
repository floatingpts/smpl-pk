from django.contrib.auth.hashers import check_password
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
import urllib.request
import urllib.parse

# import django settings file
from . import settings

@csrf_exempt
def generate_auth():
  auth = hmac.new(
          key = settings.SECRET_KEY.encode('utf-8'),
          msg = os.urandom(32),
          digestmod = 'sha256',
      ).hexdigest()
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
def musician_create_account(request):
    if request.method == 'POST':
        # Decode form-encoded user information from request key-value pairs.
        user_query = request.POST
        # Django gives us a QueryDict for the POST body.
        name = user_query.get('username')
        hashed_pass = user_query.get('password')
        mail = user_query.get('email')

        # Check that user doesn't already exist.
        try:
            musician = Musician.objects.get(username=name) # or Musician.objects.get(email=mail)
            # Return error, since user needs to pick a unique username.
            # >>> HTTP code 409: conflicting resource.
            return HttpResponse(status=409)

        except Musician.DoesNotExist:
            # New user, so add to database.
            new_user = Musician.objects.create(
                username=name,
                password=hashed_pass,
                email=mail,
            )
            new_user.save()

        # Generate random auth string.
        auth = generate_auth()
        # Check that this random string not already used.
        while(Authenticator.objects.filter(authenticator=auth).exists()):
            auth = generate_auth()

        # We now know that string stored in auth is unique, so create new authenticator object.
        new_auth = Authenticator.objects.create(
            user_id=new_user,
            authenticator=auth,
            date_created=datetime.date.today())
        new_auth.save()
        serializer = AuthenticatorSerializer(new_auth)
        return JsonResponse(serializer.data)

    else:
        # We want the API to be called as a POST request with the arguments.
        # >>> 501 Error Code: Not Implemented (i.e. wrong request).
        return HttpResponse(status=501)

@csrf_exempt
def musician_login(request):
    if request.method == 'POST':
        # Decode form-encoded user information from request key-value pairs.
        user_query = request.POST
        # Django gives us a QueryDict for the POST body.
        username = user_query.get('username')
        text_pass = user_query.get('password')

        # Get the user.
        try:
            musician = Musician.objects.get(username=username)
        except Musician.DoesNotExist:
            # Could not find the user.
            return HttpResponse(status=404)

        # Validate the plain-text password against the hash.
        hashed_pass = musician.password
        if not check_password(text_pass, hashed_pass):
            return HttpResponse(status=404)

        # Generate random auth string.
        auth = generate_auth()
        # Check that this random string not already used.
        while(Authenticator.objects.filter(authenticator=auth).exists()):
            auth = generate_auth()

        # We now know that string stored in auth is unique, so create new authenticator object.
        new_auth = Authenticator.objects.create(
            user_id=musician,
            authenticator=auth,
            date_created=datetime.date.today())
        new_auth.save()
        serializer = AuthenticatorSerializer(new_auth)
        return JsonResponse(serializer.data)

    else:
        # We want the API to be called as a POST request with the arguments.
        # >>> 501 Error Code: Not Implemented (i.e. wrong request).
        return HttpResponse(status=501)

@csrf_exempt
def create_listing(request):
    if request.method == 'POST':
        # Get auth token and form data
        query = request.POST
        auth = query.get('authenticator')

        # Check authenticator is valid
        try:
            Authenticator.objects.get(authenticator=auth)
        except Authenticator.DoesNotExist:
            return HttpResponse(status=401)

        # Create a new pack if auth is valid
        new_pack = SamplePack.objects.create(
            name=query.get('name'),
            description=query.get('description'),
            price=query.get('price'))
        new_pack.save()
        serializer = SamplePackSerializer(new_pack)
        return JsonResponse(serializer.data)
    else:
        # We want the API to be called as a POST request with the arguments.
        # >>> 501 Error Code: Not Implemented (i.e. wrong request).
        return HttpResponse(status=501)


@csrf_exempt
def musician_logout(request):
    # Get auth information from request key-value pairs.
    logout_info = request.GET
    auth = logout_info.get('authenticator')

    # Retrieve the authenticator.
    try:
        authenticator = Authenticator.objects.get(authenticator=auth)
    except Authenticator.DoesNotExist:
        # Could not find the authenticator for the user.
        return HttpResponse(status=404)

    # Delete the authenticator.
    authenticator.delete()
    # >>> 205 Error Code: No Content, Refresh.
    return HttpResponse(status=205)


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

    elif request.method == 'DELETE':
        authenticator.delete()
        return HttpResponse(status=204)

@csrf_exempt
def recommendation_list(request):
    if request.method == 'GET':
        recommendations = Recommendation.objects.all()
        serializer = RecommendationSerializer(recommendations, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RecommendationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def recommendation_detail(request, pk):
    """
    CRUD methods for Recommendation model
    """
    try:
        recommendation = Recommendation.objects.get(pk=pk)
    except Recommendation.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RecommendationSerializer(recommendation)
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        recommendation.delete()
        return HttpResponse(status=204)
