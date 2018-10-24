from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import urllib.request
import urllib.parse
import json

def samplePack_details(request, pk):
  # Get specified sample pack.
  request_samples = urllib.request.Request('http://models-api:8000/samples_in_pack/' + str(pk) + '/')
  request_pack = urllib.request.Request('http://models-api:8000/sample_packs/' + str(pk) + '/')
  json_samples = urllib.request.urlopen(request_samples).read().decode('utf-8')
  json_pack = urllib.request.urlopen(request_pack).read().decode('utf-8')

  # Decode individual JSON responses into strings.
  pack = json.load(json_pack)
  samples = json.load(json_samples)

  # Put it back into a response.
  data = {
    "pack": pack,
    "samples": samples,
  }

  return JsonResponse(data)


def home(request, template_name='home.html'):
  top_packs = urllib.request.Request('http://models-api:8000/top5_sample_packs/')
  serializer = SamplePackSerializer(top_packs, many=True)
  return JsonResponse(serializer.data)
