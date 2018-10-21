from django.shortcuts import render, get_object_or_404
from .models import *

def samplePack_details(request, pk, template_name='pack_detail.html'):
  # Get specified sample pack.
  pack = get_object_or_404(SamplePack, pk=pk)
  samples = Sample.objects.filter(pack=pk)
  samples_ordered = samples.order_by('name')

  data = {
    'pack': pack,
    'samples': samples_ordered
  }

  return render(request, template_name, data)


def home(request, template_name='home.html'):
  return render(request, template_name)
