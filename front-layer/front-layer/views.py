from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from .forms import *
from django.contrib.auth.hashers import make_password
import urllib.request
import urllib.parse
import json

# ==============
# HELPER METHODS
# ==============
def is_user_logged_in(request):
    authenticator_exists = request.COOKIES.get('authenticator')
    if authenticator_exists:
        return True
    else:
        return False

# ==============
# MAIN METHODS
# ==============
def home(request):
    #Check if user logged in (for login/logout link)
    authenticator = request.COOKIES.get('authenticator')
    if authenticator:
        loggedIn = True
    else:
        loggedIn = False

    template = loader.get_template('front-layer/home.html')
    request_top_5 = urllib.request.Request('http://exp-api:8000/home/')
    json_top_5 = urllib.request.urlopen(request_top_5).read().decode('utf-8')
    top_5 = json.loads(json_top_5)
    context = top_5
    #add logged-in info
    context['loggedIn'] = loggedIn

    return HttpResponse(template.render(context, request))

def pack_detail(request, pk):
    # Check if user logged in (for login/logout link)
    logged_in = is_user_logged_in(request)
    template = loader.get_template('front-layer/pack_detail.html')
    # Send the user_id to the experience layer for logging.
    if logged_in:
        user_id = request.COOKIES.get('user_id')
        request_pack = urllib.request.Request('http://exp-api:8000/pack_detail/' + str(pk) + '/?user_id=' + user_id)
    else:
        request_pack = urllib.request.Request('http://exp-api:8000/pack_detail/' + str(pk) + '/')
    json_pack = urllib.request.urlopen(request_pack).read().decode('utf-8')
    pack = json.loads(json_pack)
    context = pack

    reco_ids = context['recommendations']['recommended']
    if reco_ids:
        countToThree = 0
        for reco in reco_ids:
            if(countToThree > 2):
                break
            else:
                request_recommended_pack = urllib.request.Request('http://exp-api:8000/pack_detail/' + str(reco) + '/')
                json_recommended_pack = urllib.request.urlopen(request_recommended_pack).read().decode('utf-8')
                recommended_pack = json.loads(json_recommended_pack)
                context['recommendations'][reco] = recommended_pack
                countToThree += 1

    # Add logged-in info
    context['loggedIn'] = logged_in
    return JsonResponse(context)

def user_detail(request, pk):
    # Check if user logged in (for login/logout link)
    logged_in = is_user_logged_in(request)
    template = loader.get_template('front-layer/user_profile.html')
    request_musician = urllib.request.Request('http://exp-api:8000/musician_detail/' + str(pk) + '/')
    json_musician = urllib.request.urlopen(request_musician).read().decode('utf-8')
    musician = json.loads(json_musician)
    context = musician
    #add logged-in info
    context['loggedIn'] = logged_in

    return HttpResponse(template.render(context, request))

@csrf_exempt
def login(request):
    # Check if user logged in (for login/logout link)
    logged_in = is_user_logged_in(request)

    # Display login page
    if request.method == 'GET':
        # Get query component from URL.
        query_string = request.META["QUERY_STRING"]
        parsed_queries = urllib.parse.parse_qs(query_string)
        next_from_url = parsed_queries.get('next')
        if next_from_url:
            # Only get the first parameter if it exists
            next_from_url = next_from_url[0]

        # Display login form
        form = LoginForm()
        return render(
            request,
            'front-layer/login.html',
            {
            'form': form,
            'loggedIn': logged_in,
            'next': next_from_url})

    # Create new Login form instance
    form = LoginForm(request.POST)

    # Check if form is valid
    if not form.is_valid():
        # Form error, send back to login page with form errors. Just hope for the best
        # that the next field is incorrect since we set it.
        return render(
            request,
            'front-layer/login.html',
            {
                'form': form,
                'error': 'There was a problem with one of your inputs',
                'loggedIn': logged_in,
                'next': form.cleaned_data['next']
            }
        )

    # Get form data
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    form_data = {'username': username, 'password': password}
    encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')

    # Get next page from query string.
    if form.cleaned_data['next'] == 'None':
        next_page = reverse('home')
    else:
        next_page = form.cleaned_data['next']

    # Send form data to exp layer
    response_request = urllib.request.Request('http://exp-api:8000/login/', data=encoded_data, method='POST')

    # Get response back and convert from JSON.
    json_response = urllib.request.urlopen(response_request).read().decode("utf-8")
    response = json.loads(json_response)

    # Check that exp layer says form data ok
    if not response["success"]:
        error = response["error"]
        return render(request, 'front-layer/login.html', {'form': form, 'error': error, 'loggedIn': logged_in, 'next': next_page})

    # Can now log user in, set login cookie
    authenticator = response["response"]["authenticator"]
    user_id = response["response"]["user_id"]
    response = HttpResponseRedirect(next_page)
    response.set_cookie("authenticator", authenticator)
    response.set_cookie("user_id", user_id)

    return response

def logout(request):
    # Send auth to exp layer for deletion.
    auth = request.COOKIES.get('authenticator')
    url = 'http://exp-api:8000/logout/?authenticator=%s' % auth
    response_request = urllib.request.Request(url)
    urllib.request.urlopen(response_request)
    # Prepare to redirect client back home.
    home = HttpResponseRedirect(reverse('home'))
    # Delete cookie from client if present. We're just going to assume log-out
    # was successful, as otherwise we might have a cookie with no corresponding
    # authenticator. Worst case we have an authenticator in the database with no
    # cookie attached, which will be periodically wiped.
    home.delete_cookie('authenticator')
    return home

@csrf_exempt
def create_listing(request):
    logged_in = is_user_logged_in(request)
    if not logged_in:
        # Remove extra forward slashes.
        return HttpResponseRedirect("%s?next=%s" % (reverse('login'), reverse('create_listing')))

    # GET the form for users
    if request.method == 'GET':
        # Display form page
        form = ListingForm()
        return render(request, "front-layer/create_listing.html", {'form':form, 'loggedIn': logged_in})

    # Otherwise, create new form instance
    form = ListingForm(request.POST)

    # Check if form is valid
    if not form.is_valid():
        # Form error, send back to page with an error
        return render('front-layer/create_listing.html', {'form': form, 'error': 'Form was not valid!', 'loggedIn': logged_in})

    # Retrieve form data
    name = form.cleaned_data['sample_name']
    description = form.cleaned_data['sample_description']
    price = form.cleaned_data['price']
    authenticator = request.COOKIES.get('authenticator')
    form_data = {'name': name, 'description': description, 'price': price, 'authenticator': authenticator}

    # Send form data to exp layer
    data_encoded = urllib.parse.urlencode(form_data).encode('utf-8')
    response_request = urllib.request.Request('http://exp-api:8000/create_listing/', data=data_encoded, method='POST')

    # Get response back and convert from JSON.
    json_response = urllib.request.urlopen(response_request).read().decode("utf-8")
    response = json.loads(json_response)

    # Check if exp response says we passed incorrect info
    # Check that exp layer says form data ok
    if not response["success"]:
        error = response["error"]
        return render(request, 'front-layer/create_listing.html', {'form': form, 'error': error, 'loggedIn': logged_in})

    return render(request, "front-layer/create_listing.html", {'form': form, 'success': 'Your pack was successfully added! (ID=%s)' % response["response"]["id"], 'loggedIn': logged_in})

def create_account(request):
    # A user cannot create a new account while logged in.
    logged_in = is_user_logged_in(request)
    if logged_in:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'GET':
        # Display signup form
        form = MusicianForm()
        return render(request, 'front-layer/create_account.html', {'form':form})

    # Create new Musician form instance
    form = MusicianForm(request.POST)

    # Check if form is valid
    if not form.is_valid():
        # Form error, send back to sign-up page with an error ADD ERROR
        return render('front-layer/create_account.html', {'form': form, 'error': ''})

    # Get form data
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    email = form.cleaned_data['email']
    # Create hashed version of password. By default,
    # make_password salts the password in addition to hashing it.
    hashed_password = make_password(password)

    form_data = {'username': username, 'password': hashed_password, 'email': email}
    encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')

    # Get next page.
    next_page = form.cleaned_data.get('next') or reverse('home')

    # Send form data to exp layer
    response_request = urllib.request.Request('http://exp-api:8000/create_account/', data=encoded_data, method='POST')

    # Get response back and convert from JSON.
    json_response = urllib.request.urlopen(response_request).read().decode("utf-8")
    response = json.loads(json_response)

    # Check that exp layer says form data ok
    if not response["success"]:
        error = response["error"]
        return render(request, 'front-layer/create_account.html', {'form': form, 'error': error})

    # Can now log user in, set login cookie
    authenticator = response["response"]["authenticator"]
    response = HttpResponseRedirect(next_page)
    response.set_cookie("authenticator", authenticator)

    return response

def search_results(request):
    # Get query from GET parameters.
    query_encoded = urllib.parse.urlencode(request.GET)

    # Retrieve search results from exp layer
    search_request = urllib.request.Request('http://exp-api:8000/search?query_text=%s' % query_encoded)
    response = urllib.request.urlopen(search_request)

    # Decode the response from JSON into a dict
    json_response = response.read().decode('utf-8')
    results = json.loads(json_response)

    return render(request, 'front-layer/search_results.html', {'loggedIn': is_user_logged_in(request), 'results': results.get("hits")}
    )
