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

def login(request):
    if request.method == 'GET':
        #display login form
        return render(request, 'login.html')
    # Create new Musician form instance
    form = MusicianForm(request.POST)
    
    # Check if form is valid
    if not form.is_valid():
        #Form error, send back to login page with an error ADD ERROR
        return render('login.html')

    # Get form data
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    # Get next page. Currently automatically goes to home page
    next = reverse('home')

    # Send form data to exp layer
    # ADD ONCE EXP VIEW DONE!!!
    # ADD CHECKING EXP RESPONSE!!!

    # Can now log user in, set login cookie
    #ADD ONCE EXP VIEW DONE!!
    response = HttpResponseRedirect(next)
    #ADD ONCE EXP VIEW DONE!!
    return response

def logout(request):
    response = HttpResponseRedirect(reverse('home'))
    response.delete_cookie(#'COOKIE NAME HERE')
    return response

def create_listing(request):
    #set cookie assigns a string name, use this name to try to get cookie
    #ADD COOKIE GET
    #ADD CORRECTION FOR NOT LOGGED IN USER
    
    #GET request
    if request.method == 'GET':
        #Display form page
        return render("create_listing.html")

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

    return render("create_listing_success.html")

def create_account(request):
    if request.method == 'GET':
        #display signup form
        return render(request, 'create_account.html')
    # Create new Musician form instance
    form = MusicianForm(request.POST)
    
    # Check if form is valid
    if not form.is_valid():
        #Form error, send back to sign-up page with an error ADD ERROR
        return render('create_account.html')
    # Get form data
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    # Get next page. Currently automatically goes to home page
    next = reverse('home')

    # Send form data to exp layer
    # ADD ONCE EXP VIEW DONE!!!
    # ADD CHECKING EXP RESPONSE!!!

    # Can now log user in, set login cookie
    #ADD ONCE EXP VIEW DONE!!
    response = HttpResponseRedirect(next)
    #ADD ONCE EXP VIEW DONE!!
    return response

    
