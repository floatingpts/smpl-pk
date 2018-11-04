from django.test import TestCase, Client
from django.urls import reverse
from . import models, urls
import json

# ====================
# Musician test cases.
# ====================
# CREATE functionality.
class CreateMusicianTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def setUp(self):
        pass

    def test_create_valid_musician(self):
        # Add a new musician.
        musician_to_create = {
            "username": "john.smith99",
            "follower_count": 1,
            "balance": "20.00",
            "rating": 4,
        }
        self.client.post(
                path=reverse('microservices:musician-list'),
                data=musician_to_create,
                content_type="application/json")

        # Get the newly-created musician.
        response = self.client.get(reverse('microservices:musician-detail', kwargs={"pk":3}))

        # Check that the response HTTP status is 200 OK.
        self.assertEquals(response.status_code, 200)

        # Check that the POSTed musician is the same as before and is assigned an ID.
        json_musician = response.content.decode("utf-8")
        actual_musician = json.loads(json_musician)
        expected_musician = musician_to_create
        expected_musician["id"] = 3
        self.assertEquals(actual_musician, expected_musician)

    def test_create_invalid_musician(self):
        # Try to add a new invalid musician.
        musician_to_create = {
            "non_existing_field": "foo",
        }
        self.client.post(
                path=reverse('microservices:musician-list'),
                data=musician_to_create,
                content_type="application/json")

        # Get the newly-created musician.
        response = self.client.get(reverse('microservices:musician-detail', kwargs={"pk":3}))

        # Check that the musician was not added.
        self.assertEquals(response.status_code, 404)

    def tearDown(self):
        pass

# RETRIEVE functionality.
class GetMusicianDetailsTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    # Setup method is called before each test in this class.
    def setUp(self):
        pass # Nothing to set up.

    def test_get_existing_musician(self):
        # Assumes user with ID 2 is stored in db from fixture.
        response = self.client.get(reverse('microservices:musician-detail', kwargs={"pk":2}))

        # Checks that the HTTP status code is 200.
        self.assertEquals(response.status_code, 200)

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
class CreateSamplePackTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def setUp(self):
        pass

    def test_create_valid_samplePack(self):
        # Add a new sample pack.
        pack_to_create = {
            "name": "Some sounds",
            "description": "What the title says.",
            "purchase_count": 0,
            "price": "5.00",
            "num_samples": 4,
            "current_seller": None,
            "buyers": []
        }
        self.client.post(
                path=reverse('microservices:sample-pack-list'),
                data=pack_to_create,
                content_type="application/json")

        # Get the newly-created musician.
        response = self.client.get(reverse('microservices:sample-pack-detail', kwargs={"pk":6}))

        # Check that the response HTTP status is 200 OK.
        self.assertEquals(response.status_code, 200)

        # Check that the POSTed sample pack is the same as before and is assigned an ID.
        json_pack = response.content.decode("utf-8")
        actual_pack = json.loads(json_pack)
        expected_pack = pack_to_create
        expected_pack["id"] = 6
        self.assertEquals(actual_pack, expected_pack)

    def test_create_invalid_samplePack(self):
        # Try to add a new invalid sample pack.
        pack_to_create = {
            "non_existing_field": "foo",
        }
        self.client.post(
                path=reverse('microservices:sample-pack-list'),
                data=pack_to_create,
                content_type="application/json")

        # Get the newly-created sample pack.
        response = self.client.get(reverse('microservices:sample-pack-detail', kwargs={"pk":6}))

        # Check that the sample pack was not added.
        self.assertEquals(response.status_code, 404)

    def tearDown(self):
        pass

# RETRIEVE functionality.
class GetSamplePackDetailsTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    # Setup method is called before each test in this class.
    def setUp(self):
        pass # Nothing to set up.

    def test_get_existing_samplePack(self):
        # Assumes pack with ID 2 is stored in db from fixture.
        response = self.client.get(reverse('microservices:sample-pack-detail', kwargs={"pk":2}))

        # Checks that the HTTP status code is 200.
        self.assertEquals(response.status_code, 200)

        # Get musician from JSON response.
        # Django returns a byte string for the response content, which
        # needs to be decoded. See https://stackoverflow.com/questions/606191/.
        pack_json = response.content.decode("utf-8")
        pack = json.loads(pack_json)
        self.assertEquals(pack["id"], 2)

    # Non-existing pack ID given in url, so error.
    def test_get_non_existing_samplePack(self):
        # Try to get a pack with an unused ID.
        response = self.client.get(reverse('microservices:sample-pack-detail', kwargs={"pk":9}))

        # Check that no such user exists.
        self.assertEquals(response.status_code, 404)

    def test_get_samplePack_invalid_id(self):
        # Try to get a pack with an invalid ID (a string).
        # Reverse can't be used because the resolver will try to match the url
        # to the urlpattern, which validates whether the argument's type (in
        # this case, the string doesn't match the <int:pk> parameter).
        response = self.client.get('/api/sample_packs/foo/')

        # Check that no such pack exists.
        self.assertEquals(response.status_code, 404)

    # Teardown method is called after each test.
    def tearDown(self):
        pass # Nothing to tear down.

class GetSamplePackListTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    # Setup method is called before each test in this class.
    def setUp(self):
        pass # Nothing to set up.

    def test_get_samplePack_list(self):
        # Assumes user with pack 2 is stored in db from fixture.
        response = self.client.get(reverse('microservices:sample-pack-list'))

        # Checks that the HTTP status code is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Get first element in response.
        pack_list_json = response.content.decode("utf-8")
        pack_list = json.loads(pack_list_json)

        # Check that only 5 packs in list, check that first pack
        # has an ID of 2.
        self.assertEquals(len(pack_list), 5)

    # Teardown method is called after each test.
    def tearDown(self):
        pass # Nothing to tear down.

# ==================
# Sample test cases.
# ==================
# Insert test cases here.
