from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import django.contrib.auth.hashers
from django.http import JsonResponse
from elasticsearch import Elasticsearch
from kafka import KafkaProducer
import urllib.request
import urllib.parse
import urllib.error
import json

def samplePack_details(request, pk):
  # Get specified sample pack.
  request_samples = urllib.request.Request('http://models-api:8000/api/samples_in_pack/' + str(pk) + '/')
  request_pack = urllib.request.Request('http://models-api:8000/api/sample_packs/' + str(pk) + '/')
  json_samples = urllib.request.urlopen(request_samples).read().decode('utf-8')
  json_pack = urllib.request.urlopen(request_pack).read().decode('utf-8')

  # Decode individual JSON responses from strings.
  pack = json.loads(json_pack)
  samples = json.loads(json_samples)

  # Put it back into a response.
  data = {
    "pack": pack,
    "samples": samples,
  }

  return JsonResponse(data)


def home(request):
  top_packs = urllib.request.Request('http://models-api:8000/api/top5_sample_packs/')
  json_packs = urllib.request.urlopen(top_packs).read().decode('utf-8')
  packs = json.loads(json_packs)

  data = {
    "packs": packs,
  }

  return JsonResponse(data)

def musician_detail(request, pk):
  musician = urllib.request.Request('http://models-api:8000/api/musicians/' + str(pk) + '/')
  json_musician = urllib.request.urlopen(musician).read().decode('utf-8')
  musician_data = json.loads(json_musician)

  data = {
    "musician": musician_data,
  }
  return JsonResponse(data)

@csrf_exempt
def login(request):
  # Pass info along to model API via a POST request with form data.
  response_request = urllib.request.Request('http://models-api:8000/api/musician_login/', data=request.body, method='POST')
  try:
    response = urllib.request.urlopen(response_request)
  except urllib.error.HTTPError as e:
    if e.code == 404:
      # This is expected if user is not found, can't return auth.
      data = {
        "success": False,
        "error": "Incorrect username or password.",
      }
      return JsonResponse(data)
    else:
      data = {
        "success": False,
        "error": "Unknown error code %s." % e.code,
      }
      return JsonResponse(data)

  # Decode the response.
  decoded_response = response.read().decode('utf-8')
  auth_data = json.loads(decoded_response)

  # Return the authenticator.
  data = {
    "response": auth_data,
    "success": True,
  }
  return JsonResponse(data)

def logout(request):
    # Get authenticator from front-end.
    logout_info = request.GET
    auth = logout_info['authenticator']
    url = 'http://models-api:8000/api/musician_logout/?authenticator=%s' % auth
    # Pass authenticator to model API for verification.
    response_request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(response_request)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            data = {
              "success": False,
              "error": "User could not be found (is not logged in).",
            }
            return JsonResponse(data)
        else:
            data = {
              "success": False,
              "error": "Unknown error code %s." % e.code,
            }
            return JsonResponse(data)

    # Return a response specifying whether log-out was successful, depending on status code.
    data = {
        "success": True,
    }
    return JsonResponse(data)

@csrf_exempt
def create_account(request):
  # Pass info along to model API via a POST request with form data.
  response_request = urllib.request.Request('http://models-api:8000/api/musician_create_account/', data=request.body, method='POST')
  try:
    response = urllib.request.urlopen(response_request)
  except urllib.error.HTTPError as e:
    #handle error
    data = {
        "success": False,
        "error": "Unknown error code %s." % e.code,
    }
    return JsonResponse(data)

  # Decode the response.
  decoded_response = response.read().decode('utf-8')
  auth_data = json.loads(decoded_response)

  # Return the authenticator.
  data = {
    "response": auth_data,
    "success": True,
  }
  return JsonResponse(data)

@csrf_exempt
def create_listing(request):
  # Pass data along to model API to create a new entry.
  data=request.body
  response_request = urllib.request.Request('http://models-api:8000/api/create_listing/', data, method='POST')
  try:
    # Pass the listing.
    response = urllib.request.urlopen(response_request)
  except urllib.error.HTTPError as e:
    # Handle error
    if e.code == 401:
        data = {
          "success": False,
          "error": "Please log in before creating a listing.",
        }
        return JsonResponse(data)
    else:
        data = {
          "success": False,
          "error": "Unknown error code %s." % e.code,
        }
        return JsonResponse(data)


  # Return a JsonResponse to the front-end specifying whether creation was successful and user was logged-in.

  decoded_response = response.read().decode('utf-8')
  pack_data = json.loads(decoded_response)

  # Insert the listing into the Kafka queue.
  producer = KafkaProducer(bootstrap_servers='kafka:9092')
  producer.send('sample-pack-listings', json.dumps(pack_data).encode('utf-8'))

  data = {
    "response": pack_data,
    "success": True
  }

  return JsonResponse(data)

def search(request):
  # Get query text.
  # Should already be url encoded.
  query = request.GET.get('query_text')

  # Call ElasticSearch to find results based on user's search.
  es = Elasticsearch(['es'])
  # Get the top 10 results.
  results = es.search(index='listing_index', body={'query': {'query_string': {'query': query }}, 'size': 10})

  # Format JSON object:
  # - Elements in a list, ID ordered by highest score
  # - Each element is just the fields of the result (fields of the packs)
  # - Errors field with description of error if present (timeout, failed, etc)
  results_count = results['hits']['total']
  if results_count == 0:
      return JsonResponse({
          'success': False,
          'error': 'No results were found for your search.'
      })

  hits = results['hits']['hits']
  data = {
      'hits': [],
      'success': True,
  }
  for listing in hits:
      data['hits'].append(listing['_source'])

  return JsonResponse(data)
