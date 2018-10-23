from django.shortcuts import render, get_object_or_404
import urllib.request
import urllib.parse
import json
from .models import *

def samplePack_details(request, pk):
  # Get specified sample pack.
  request_samples = urllib.request.Request('db:8001/samples_in_packs', method='GET')
  request_pack = urllib.request.Request('db:8001/sample_packs' + pk)
  json_samples = urllib.request.urlopen(request_samples).read().decode('utf-8')
  json_pack = urllib.request.urlopen(request_pack).read().decode('utf-8')

  data = {
    'pack': pack,
    'samples': samples_ordered
  }

  return render(request, data)


def home(request, template_name='home.html'):
  top_packs = urllib.request.Request('db:8001/top5_packs')
  serializer = SamplePackSerializer(top_packs)
  return JsonResponse(serializer.data)
