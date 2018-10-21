from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def home(request):
    template = loader.get_template('front-layer/home.html')
    context = {} # Nothing to substitute in just yet
    return HttpResponse(template.render(context, request))

def pack_detail(request):
    template = loader.get_template('front-layer/pack_detail.html')
    context = {}
    return HttpResponse(template.render(context, request))
