from django.test import TestCase, Client
from django.urls import reverse
from . import models, urls
import json

# ====================
# Musician test cases.
# ====================
class GetMusicianDetailsTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    # Setup method is called before each test in this class.
    def setUp(self):
        pass # Nothing to set up.

    def test_get_existing_musician(self):
        # Assumes user with ID 2 is stored in db from fixture.
        response = self.client.get(reverse('microservices:musician-detail', kwargs={"pk":2}))

        # Checks that response contains parameter & implicitly
        # checks that the HTTP status code is 200.
        self.assertContains(response, 'id')

        # Get musician from JSON response.
        # Django returns a byte string for the response content, which
        # needs to be decoded. See https://stackoverflow.com/questions/606191/.
        musician_json = response.content.decode("utf-8")
        musician = json.loads(musician_json)
        self.assertEquals(musician["id"], 2)

    # Non-existing user ID given in url, so error.
    def test_get_non_existing_musician(self):
        # Try to get a user with an unused ID.
        response = self.client.get(reverse('microservices:musician-detail', kwargs={"pk":9}))

        # Check that no such user exists.
        self.assertEquals(response.status_code, 404)

    def test_get_musician_invalid_id(self):
        # Try to get a user with an invalid ID (a string).
        # Reverse can't be used because the resolver will try to match the url
        # to the urlpattern, which validates whether the argument's type (in
        # this case, the string doesn't match the <int:pk> parameter).
        response = self.client.get('/api/musicians/foo/')

        # Check that no such user exists.
        self.assertEquals(response.status_code, 404)

    # Teardown method is called after each test.
    def tearDown(self):
        pass # Nothing to tear down.

class GetMusicianListTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    # Setup method is called before each test in this class.
    def setUp(self):
        pass # Nothing to set up.

    def test_get_musician_list(self):
        # Assumes user with ID 2 is stored in db from fixture.
        response = self.client.get(reverse('microservices:musician-list'))

        # Checks that the HTTP status code is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Get first element in response.
        musician_list_json = response.content.decode("utf-8")
        musician_list = json.loads(musician_list_json)
        musician = musician_list[0]

        # Check that only one musician is inserted, with an ID of 2.
        self.assertEquals(len(musician_list), 1)
        self.assertEquals(musician["id"], 2)

    # Teardown method is called after each test.
    def tearDown(self):
        pass # Nothing to tear down.

# =======================
# Sample pack test cases.
# =======================
# Insert test cases here.

# ==================
# Sample test cases.
# ==================
# Insert test cases here.
