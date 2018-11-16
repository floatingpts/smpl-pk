from django.shortcuts import render, get_object_or_404
import django.contrib.auth.hashers
from django.http import JsonResponse
import urllib.request
import urllib.parse
import json

def samplePack_details(request, pk):
  # Get specified sample pack.
  request_samples = urllib.request.Request('http://models-api:8000/api/samples_in_pack/' + str(pk) + '/')
  request_pack = urllib.request.Request('http://models-api:8000/api/sample_packs/' + str(pk) + '/')
  json_samples = urllib.request.urlopen(request_samples).read().decode('utf-8')
  json_pack = urllib.request.urlopen(request_pack).read().decode('utf-8')

  # Decode individual JSON responses from strings.
  pack = json.loads(json_pack)
  samples = json.loads(json_samples)

  # Put it back into a response.
  data = {
    "pack": pack,
    "samples": samples,
  }

  return JsonResponse(data)


def home(request):
  top_packs = urllib.request.Request('http://models-api:8000/api/top5_sample_packs/')
  json_packs = urllib.request.urlopen(top_packs).read().decode('utf-8')
  packs = json.loads(json_packs)

  data = {
    "packs": packs,
  }

  return JsonResponse(data)

def musician_detail(request, pk):
  musician = urllib.request.Request('http://models-api:8000/api/musicians/' + str(pk) + '/')
  json_musician = urllib.request.urlopen(musician).read().decode('utf-8')
  musician_data = json.loads(json_musician)

  data = {
    "musician": musician_data,
  }
  return JsonResponse(data)

def login(user):
  # Pass info along to model API via a POST request with form data.
  #user = {
  #  "username": username,
  #  "password": password,
  #}
  response = urllib.request.Request('http://models-api:8000/api/musician_login/', data=user)
  json_auth = urllib.request.urlopen(response).read().decode('utf-8')
  auth_data = json.loads(json_auth)

  data = {
    "response": auth_data,
  }

  # Check if info was correct (stored in the database).
  if response.status_code == 404:
    return None
  else:
    return JsonResponse(data)

def logout(authenticator):
  # Pass authenticator to model API for verification.
  # ...
  # Return a JsonResponse specifying whether log-out was successful.
  # ...
  pass

def create_account(username, password):
  # Create hashed version of password
  hashed_password = make_password(password)
  # Pass info along to model API.
  user = {
    "username": username,
    "password": hashed_password,
  }
  response = urllib.request.Request('http://models-api:8000/api/mu', data=user, method='PUT')
  # Check if info does not exist, validate password. Model API will add user to database.
  # ...
  # Return a JsonReponse to the front-end specifying whether account creation was successful, with the new authenticator included.
  pass

def create_listing(authenticator, data):
  # Pass authenticator to model API for verification.
  # ...
  # Pass data along to model API to create a new entry.
  # ...
  # Return a JsonResponse to the front-end specifying whether creation was successful and user was logged-in.
  pass
