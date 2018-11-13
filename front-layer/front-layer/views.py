from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .forms import *
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

def user_detail(request, pk):
    template = loader.get_template('front-layer/musician_detail.html')
    request_musician = urllib.request.Request('http://exp-api:8000/musician_detail/' + str(pk) + '/')
    json_musician = urllib.request.urlopen(request_pack).read().decode('utf-8')
    musician = json.loads(json_musician)
    context = musician
    return HttpResponse(template.render(context, request))

def login(request):
    if request.method == 'GET':
        #display login form
        form = MusicianForm()
        return render(request, 'front-layer/login.html', {'form':form})
    # Create new Musician form instance
    form = MusicianForm(request.POST)
    
    # Check if form is valid
    if not form.is_valid():
        #Form error, send back to login page with an error ADD ERROR
        return render(request, 'front-layer/login.html', {'form':form})

    # Get form data
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    # Get next page. Currently automatically goes to home page
    next = reverse('front-layer/home')

    # Send form data to exp layer
    # ADD ONCE EXP VIEW DONE!!!
    # ADD CHECKING EXP RESPONSE!!!

    # Can now log user in, set login cookie
    #ADD ONCE EXP VIEW DONE!!
    response = HttpResponseRedirect(next)
    #ADD ONCE EXP VIEW DONE!!
    return response

def logout(request):
    response = HttpResponseRedirect(reverse('front-layer/home'))
    response.delete_cookie()#'COOKIE NAME HERE IN ()'
    return response

def create_listing(request):
    #set cookie assigns a string name, use this name to try to get cookie
    #ADD COOKIE GET
    #ADD CORRECTION FOR NOT LOGGED IN USER
    
    #GET request
    if request.method == 'GET':
        #Display form page
        form = ListingForm()
        return render(request, "front-layer/create_listing.html", {'form':form})

    #Otherwise, create new form instance
    form = ListingForm(request.POST)

    #Retrieve form data
    name = form.cleaned_data['name']
    description = form.cleaned_data['description']
    price = form.cleaned_data['price']

    #Send form data to exp layer
    #ADD ONCE EXP DONE!!!

    #Check if exp response says we passed incorrect info
    #ADD ONCE EXP DONE!!!

    return render(request, "front-layer/create_listing_success.html")

def create_account(request):
    if request.method == 'GET':
        #display signup form
        form = MusicianForm()
        return render(request, 'front-layer/create_account.html', {'form':form})
    # Create new Musician form instance
    form = MusicianForm(request.POST)
    
    # Check if form is valid
    if not form.is_valid():
        #Form error, send back to sign-up page with an error ADD ERROR
        return render('front-layer/create_account.html')
    # Get form data
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    # Get next page. Currently automatically goes to home page
    next = reverse('front-layer/home')

    # Send form data to exp layer
    # ADD ONCE EXP VIEW DONE!!!
    # ADD CHECKING EXP RESPONSE!!!

    # Can now log user in, set login cookie
    #ADD ONCE EXP VIEW DONE!!
    response = HttpResponseRedirect(next)
    #ADD ONCE EXP VIEW DONE!!
    return response

    
