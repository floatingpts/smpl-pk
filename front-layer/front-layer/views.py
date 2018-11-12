from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import urllib.request
import urllib.parse
import json

def home(request):
    template = loader.get_template('front-layer/home.html')
    request_top_5 = urllib.request.Request('http://exp-api:8000/home/')
    json_top_5 = urllib.request.urlopen(request_top_5).read().decode('utf-8')
    top_5 = json.loads(json_top_5)
    context = top_5
    return HttpResponse(template.render(context, request))

def pack_detail(request, pk):
    template = loader.get_template('front-layer/pack_detail.html')
    request_pack = urllib.request.Request('http://exp-api:8000/pack_detail/' + str(pk) + '/')
    json_pack = urllib.request.urlopen(request_pack).read().decode('utf-8')
    pack = json.loads(json_pack)
    context = pack
    return HttpResponse(template.render(context, request))

def login(request):
    if request.method == 'GET':
        #display login form
        return render(request, 'login.html')
