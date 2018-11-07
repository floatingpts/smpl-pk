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

