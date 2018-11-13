from django.shortcuts import render, get_object_or_404
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

def login(username, password):
  # Pass info along to model API via a POST request with form data.
  user = {
    "username": username,
    "password": password,
  }
  # Check if info was correct (stored in the database).
  # ...
  # Return a JsonResponse to the front-end specifying whether log-in was successful, with the authenticator included.
  pass

def logout(authenticator):
  # Pass authenticator to model API for verification.
  # ...
  # Return a JsonResponse specifying whether log-out was successful.
  # ...
  pass

def create_account(username, password):
  # Pass info along to model API.
  # ...
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
