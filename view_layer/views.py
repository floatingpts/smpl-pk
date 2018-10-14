from django.shortcuts import render, get_object_or_404
from .models import *

def samplePack_details(pk, template_name='pack_detail.html')
  #get specified sample pack
  pack = get_object_or_404(SamplePack, pk=pk)
  samples = Sample.objects.filter(pack=pk)
  samples_ordered = samples.order_by('name')
  
  data = {
    'pack': pack,
    'samples': samples_ordered
  }

  return render(request, template_name, data)
