from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def index(request):
    template = loader.get_template('isa-app/index.html')
    context = {} # Nothing to substitute in just yet
    return HttpResponse(template.render(context, request))
