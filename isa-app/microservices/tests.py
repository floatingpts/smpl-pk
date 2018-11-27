from django.test import TestCase, Client
from django.urls import reverse
from . import models, urls
import json

# ====================
# Musician test cases.
# ====================
# CREATE/POST functionality.
class CreateMusicianTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

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

# RETRIEVE/GET functionality.
class RetrieveMusicianDetailsTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

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

class RetrieveMusicianListTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

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

# UPDATE/PUT functionality.
class UpdateMusicianTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_update_valid_musician(self):
        # Update the musician with ID 2.
        updated_musician = {
            "username": "john.smith99",
            "follower_count": 1,
            "balance": "20.00",
            "rating": 4,
        }
        self.client.put(
                path=reverse('microservices:musician-detail',
                    kwargs={"pk":2}),
                data=updated_musician,
                content_type="application/json")

        # Get the newly-updated musician.
        response = self.client.get(reverse('microservices:musician-detail', kwargs={"pk":2}))

        # Check that the response HTTP status is 200 OK.
        self.assertEquals(response.status_code, 200)

        # Check that the musician is updated.
        json_musician = response.content.decode("utf-8")
        actual_musician = json.loads(json_musician)
        expected_musician = updated_musician
        expected_musician["id"] = 2
        self.assertEquals(actual_musician, expected_musician)

    def test_update_invalid_musician(self):
        # Get existing musician with ID 2.
        old_musician_response = self.client.get(reverse('microservices:musician-detail', kwargs={"pk":2}))
        old_json_musician = old_musician_response.content.decode("utf-8")
        expected_musician = json.loads(old_json_musician)

        # Try to update the musician with an invalid field.
        invalid_updated_musician = {
            "non_existing_field": "foo",
        }
        self.client.put(
                path=reverse('microservices:musician-detail',
                    kwargs={"pk":2}),
                data=invalid_updated_musician,
                content_type="application/json")

        # Get the musician again.
        new_musician_response = self.client.get(reverse('microservices:musician-detail', kwargs={"pk":2}))
        new_json_musician = new_musician_response.content.decode("utf-8")
        actual_musician = json.loads(new_json_musician)

        # Check that the musician was not updated.
        self.assertEquals(actual_musician, expected_musician)

# DELETE/DEL functionality.
class DeleteMusicianTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_delete_musician(self):
        # Verify musician with ID of 2 exists before continuing.
        verify_exists_response = self.client.get(reverse('microservices:musician-detail', kwargs={"pk":2}))
        self.assertEquals(verify_exists_response.status_code, 200)

        # Delete musician with ID of 2.
        # This returns a 204 No Content response, but there isn't really
        # a consistent standard among RESTful APIs in regards for what to return
        # so there's no need to validate this behavior.
        self.client.delete(reverse('microservices:musician-detail', kwargs={"pk":2}))

        # Check that the musician no longer exists.
        get_response = self.client.get(reverse('microservices:musician-detail', kwargs={"pk":2}))
        self.assertEquals(get_response.status_code, 404)

# =======================
# Sample pack test cases.
# =======================
# CREATE/POST functionality.
class CreateSamplePackTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

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

        # Get the newly-created musician. Assumes there are 5 sample packs in the DB.
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

# RETRIEVE/GET functionality.
class RetrieveSamplePackDetailsTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_get_existing_samplePack(self):
        # Assumes pack with ID 2 is stored in db from fixture.
        response = self.client.get(reverse('microservices:sample-pack-detail', kwargs={"pk":2}))

        # Checks that the HTTP status code is 200.
        self.assertEquals(response.status_code, 200)

        # Get sample pack from JSON response.
        # Django returns a byte string for the response content, which
        # needs to be decoded. See https://stackoverflow.com/questions/606191/.
        pack_json = response.content.decode("utf-8")
        pack = json.loads(pack_json)
        self.assertEquals(pack["id"], 2)

    # Non-existing pack ID given in url, so error.
    def test_get_non_existing_samplePack(self):
        # Try to get a pack with an unused ID.
        response = self.client.get(reverse('microservices:sample-pack-detail', kwargs={"pk":9}))

        # Check that no such pack exists.
        self.assertEquals(response.status_code, 404)

    def test_get_samplePack_invalid_id(self):
        # Try to get a pack with an invalid ID (a string).
        # Reverse can't be used because the resolver will try to match the url
        # to the urlpattern, which validates whether the argument's type (in
        # this case, the string doesn't match the <int:pk> parameter).
        response = self.client.get('/api/sample_packs/foo/')

        # Check that no such pack exists.
        self.assertEquals(response.status_code, 404)

class RetrieveSamplePackListTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_get_samplePack_list(self):
        # Assumes user with pack 2 is stored in db from fixture.
        response = self.client.get(reverse('microservices:sample-pack-list'))

        # Checks that the HTTP status code is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Get list of sample packs in response.
        pack_list_json = response.content.decode("utf-8")
        pack_list = json.loads(pack_list_json)

        # Check that only 5 packs in list.
        self.assertEquals(len(pack_list), 5)

    # Teardown method is called after each test.
    def tearDown(self):
        pass # Nothing to tear down.

# UPDATE/PUT functionality.
class UpdateSamplePackTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_update_valid_samplePack(self):
        # Update the sample pack with ID 5.
        updated_pack = {
            "name": "Some sounds",
            "description": "What the title says.",
            "purchase_count": 0,
            "price": "5.00",
            "num_samples": 4,
            "current_seller": None,
            "buyers": []
        }
        self.client.put(
                path=reverse('microservices:sample-pack-detail',
                    kwargs={"pk":5}),
                data=updated_pack,
                content_type="application/json")

        # Get the newly-updated musician.
        response = self.client.get(reverse('microservices:sample-pack-detail', kwargs={"pk":5}))

        # Check that the response HTTP status is 200 OK.
        self.assertEquals(response.status_code, 200)

        # Check that the sample pack is updated.
        json_pack = response.content.decode("utf-8")
        actual_pack = json.loads(json_pack)
        expected_pack = updated_pack
        expected_pack["id"] = 5
        self.assertEquals(actual_pack, expected_pack)

    def test_update_invalid_samplePack(self):
        # Get existing pack with ID 5.
        old_pack_response = self.client.get(reverse('microservices:sample-pack-detail', kwargs={"pk":5}))
        old_json_pack = old_pack_response.content.decode("utf-8")
        expected_pack = json.loads(old_json_pack)

        # Try to add a new invalid sample pack.
        invalid_updated_pack = {
            "non_existing_field": "foo",
        }
        self.client.put(
                path=reverse('microservices:sample-pack-detail',
                    kwargs={"pk":5}),
                data=invalid_updated_pack,
                content_type="application/json")

        # Get the newly-updated sample pack.
        new_pack_response = self.client.get(reverse('microservices:sample-pack-detail', kwargs={"pk":5}))
        new_json_pack = new_pack_response.content.decode("utf-8")
        actual_pack = json.loads(new_json_pack)

        # Check that the sample pack was not updated.
        self.assertEquals(actual_pack, expected_pack)

# DELETE/DEL functionality.
class DeleteSamplePackTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_delete_samplePack(self):
        # Verify sample pack with ID of 1 exists before continuing.
        verify_exists_response = self.client.get(reverse('microservices:sample-pack-detail', kwargs={"pk":1}))
        self.assertEquals(verify_exists_response.status_code, 200)

        # Delete sample pack with ID of 1.
        self.client.delete(reverse('microservices:sample-pack-detail', kwargs={"pk":1}))

        # Check that the sample pack no longer exists.
        get_response = self.client.get(reverse('microservices:sample-pack-detail', kwargs={"pk":1}))
        self.assertEquals(get_response.status_code, 404)

# ==================
# Sample test cases.
# ==================
# CREATE/POST functionality.
class CreateSampleTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_create_valid_sample(self):
        # Add a new sample.
        sample_to_create = {
            "name": "sound",
            "minute_length": 1,
            "second_length": 20,
            "pack": 2,
        }
        self.client.post(
                path=reverse('microservices:samples-list'),
                data=sample_to_create,
                content_type="application/json")

        # Get the newly-created sample.
        response = self.client.get(reverse('microservices:samples-detail', kwargs={"pk":10}))

        # Check that the response HTTP status is 200 OK.
        self.assertEquals(response.status_code, 200)

        # Check that the POSTed sample is the same as before and is assigned an ID.
        json_sample = response.content.decode("utf-8")
        actual_sample = json.loads(json_sample)
        expected_sample = sample_to_create
        expected_sample["id"] = 10
        self.assertEquals(actual_sample, expected_sample)

    def test_create_invalid_sample(self):
        # Try to add a new invalid sample.
        sample_to_create = {
            "non_existing_field": "foo",
        }
        self.client.post(
                path=reverse('microservices:samples-list'),
                data=sample_to_create,
                content_type="application/json")

        # Get the newly-created sample.
        response = self.client.get(reverse('microservices:samples-detail', kwargs={"pk":10}))

        # Check that the sample was not added.
        self.assertEquals(response.status_code, 404)

# RETRIEVE/GET functionality.
class RetrieveSampleDetailsTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_get_existing_sample(self):
        # Assumes sample with ID 2 is stored in db from fixture.
        response = self.client.get(reverse('microservices:samples-detail', kwargs={"pk":2}))

        # Checks that the HTTP status code is 200.
        self.assertEquals(response.status_code, 200)

        # Get sample from JSON response.
        # Django returns a byte string for the response content, which
        # needs to be decoded. See https://stackoverflow.com/questions/606191/.
        sample_json = response.content.decode("utf-8")
        sample = json.loads(sample_json)
        self.assertEquals(sample["id"], 2)

    # Non-existing sample ID given in url, so error.
    def test_get_non_existing_sample(self):
        # Try to get a sample with an unused ID.
        response = self.client.get(reverse('microservices:samples-detail', kwargs={"pk":25}))

        # Check that no such sample exists.
        self.assertEquals(response.status_code, 404)

    def test_get_sample_invalid_id(self):
        # Try to get a sample with an invalid ID (a string).
        # Reverse can't be used because the resolver will try to match the url
        # to the urlpattern, which validates whether the argument's type (in
        # this case, the string doesn't match the <int:pk> parameter).
        response = self.client.get('/api/samples/foo/')

        # Check that no such sample exists.
        self.assertEquals(response.status_code, 404)

class RetrieveSampleListTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_get_sample_list(self):
        # Assumes sample with ID 1 is stored in db from fixture.
        response = self.client.get(reverse('microservices:samples-list'))

        # Checks that the HTTP status code is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Get first element in response.
        sample_list_json = response.content.decode("utf-8")
        sample_list = json.loads(sample_list_json)
        sample = sample_list[0]

        # Check that 9 samples in list, with first sample having an ID of 1.
        self.assertEquals(len(sample_list), 9)
        self.assertEquals(sample["id"], 1)

# UPDATE/PUT functionality.
class UpdateSampleTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_update_valid_sample(self):
        # Update the sample with ID 2.
        updated_sample = {
            "name": "sound",
            "minute_length": 10,
            "second_length": 0,
            "pack": 2,
        }
        self.client.put(
                path=reverse('microservices:samples-detail',
                    kwargs={"pk":2}),
                data=updated_sample,
                content_type="application/json")

        # Get the newly-updated sample.
        response = self.client.get(reverse('microservices:samples-detail', kwargs={"pk":2}))

        # Check that the response HTTP status is 200 OK.
        self.assertEquals(response.status_code, 200)

        # Check that the sample is updated.
        json_sample = response.content.decode("utf-8")
        actual_sample = json.loads(json_sample)
        expected_sample = updated_sample
        expected_sample["id"] = 2
        self.assertEquals(actual_sample, expected_sample)

    def test_update_invalid_sample(self):
        # Get existing sample with ID 2.
        old_sample_response = self.client.get(reverse('microservices:samples-detail', kwargs={"pk":2}))
        old_json_sample = old_sample_response.content.decode("utf-8")
        expected_sample = json.loads(old_json_sample)

        # Try to update the sample with an invalid field.
        invalid_updated_sample = {
            "non_existing_field": "foo",
        }
        self.client.put(
                path=reverse('microservices:samples-detail',
                    kwargs={"pk":2}),
                data=invalid_updated_sample,
                content_type="application/json")

        # Get the sample again.
        new_sample_response = self.client.get(reverse('microservices:samples-detail', kwargs={"pk":2}))
        new_json_sample = new_sample_response.content.decode("utf-8")
        actual_sample = json.loads(new_json_sample)

        # Check that the sample was not updated.
        self.assertEquals(actual_sample, expected_sample)

# DELETE/DEL functionality.
class DeleteSampleTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_delete_sample(self):
        # Verify sample with ID of 2 exists before continuing.
        verify_exists_response = self.client.get(reverse('microservices:samples-detail', kwargs={"pk":2}))
        self.assertEquals(verify_exists_response.status_code, 200)

        # Delete sample with ID of 2.
        # This returns a 204 No Content response, but there isn't really
        # a consistent standard among RESTful APIs in regards for what to return
        # so there's no need to validate this behavior.
        self.client.delete(reverse('microservices:samples-detail', kwargs={"pk":2}))

        # Check that the sample no longer exists.
        get_response = self.client.get(reverse('microservices:samples-detail', kwargs={"pk":2}))
        self.assertEquals(get_response.status_code, 404)

# ==================
# Authenticator test cases.
# ==================
# CREATE/POST functionality.
class CreateAuthenticatorTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_create_valid_authenticator(self):
        # Add a new authenticator.
        authenticator = {
            "user-id": "tom",
            "authenticator": 30491234,
            "date-created": "1999-02-01"
        }
        self.client.post(
                path=reverse('microservices:authenticator-list'),
                data=authenticator,
                content_type="application/json")

        # Get the newly-created authenticator.
        response = self.client.get(reverse('microservices:authenticator-detail', kwargs={"pk":1}))

        # Check that the response HTTP status is 200 OK.
        self.assertEquals(response.status_code, 200)

        # Check that the POSTed authenticator is the same as before and is assigned an ID.
        actual = json.loads(response.content.decode("utf-8"))
        expected = authenticator
        expected["user-id"] = "tom"
        self.assertEquals(actual, expected)

    def test_create_invalid_authenticator(self):
        # Try to add a new invalid authenticator.
        authenticator = {
            "non_existing_field": "foo",
        }
        self.client.post(
                path=reverse('microservices:authenticator-list'),
                data=authenticator,
                content_type="application/json")

        # Get the newly-created authenticator.
        response = self.client.get(reverse('microservices:authenticator-detail', kwargs={"pk":1}))

        # Check that the authenticator was not added.
        self.assertEquals(response.status_code, 404)

# RETRIEVE/GET functionality.
class RetrieveAuthenticatorDetailsTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_get_existing_authenticator(self):
        # Assumes authenticator with ID 2 is stored in db from fixture.
        response = self.client.get(reverse('microservices:authenticator-detail', kwargs={"pk":2}))

        # Checks that the HTTP status code is 200.
        self.assertEquals(response.status_code, 200)

        # Get authenticator from JSON response.
        # Django returns a byte string for the response content, which
        # needs to be decoded. See https://stackoverflow.com/questions/606191/.
        authenticator_json = response.content.decode("utf-8")
        authenticator = json.loads(authenticator_json)
        self.assertEquals(authenticator["id"], 2)

    # Non-existing authenticator ID given in url, so error.
    def test_get_non_existing_authenticator(self):
        # Try to get a authenticator with an unused ID.
        response = self.client.get(reverse('microservices:authenticator-detail', kwargs={"pk":25}))

        # Check that no such authenticator exists.
        self.assertEquals(response.status_code, 404)

    def test_get_authenticator_invalid_id(self):
        # Try to get a authenticator with an invalid ID (a string).
        # Reverse can't be used because the resolver will try to match the url
        # to the urlpattern, which validates whether the argument's type (in
        # this case, the string doesn't match the <int:pk> parameter).
        response = self.client.get('/api/authenticators/foo/')

        # Check that no such authenticator exists.
        self.assertEquals(response.status_code, 404)

class RetrieveAuthenticatorListTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_get_authenticator_list(self):
        # Assumes authenticator with ID 1 is stored in db from fixture.
        response = self.client.get(reverse('microservices:authenticator-list'))

        # Checks that the HTTP status code is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Get first element in response.
        authenticator_list_json = response.content.decode("utf-8")
        authenticator_list = json.loads(authenticator_list_json)
        authenticator = authenticator_list[0]

        # Check that 9 authenticators in list, with first authenticator having an ID of 1.
        self.assertEquals(len(authenticator_list), 9)
        self.assertEquals(authenticator["id"], 1)

# UPDATE/PUT functionality.
class UpdateAuthenticatorTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_update_valid_authenticator(self):
        # Update the authenticator with ID 2.
        updated_authenticator = {
            "name": "sound",
            "minute_length": 10,
            "second_length": 0,
            "pack": 2,
        }
        self.client.put(
                path=reverse('microservices:authenticator-detail',
                    kwargs={"pk":2}),
                data=updated_authenticator,
                content_type="application/json")

        # Get the newly-updated authenticator.
        response = self.client.get(reverse('microservices:authenticator-detail', kwargs={"pk":2}))

        # Check that the response HTTP status is 200 OK.
        self.assertEquals(response.status_code, 200)

        # Check that the authenticator is updated.
        json_authenticator = response.content.decode("utf-8")
        actual_authenticator = json.loads(json_authenticator)
        expected_authenticator = updated_authenticator
        expected_authenticator["id"] = 2
        self.assertEquals(actual_authenticator, expected_authenticator)

    def test_update_invalid_authenticator(self):
        # Get existing authenticator with ID 2.
        old_authenticator_response = self.client.get(reverse('microservices:authenticator-detail', kwargs={"pk":2}))
        old_json_authenticator = old_authenticator_response.content.decode("utf-8")
        expected_authenticator = json.loads(old_json_authenticator)

        # Try to update the authenticator with an invalid field.
        invalid_updated_authenticator = {
            "non_existing_field": "foo",
        }
        self.client.put(
                path=reverse('microservices:authenticator-detail',
                    kwargs={"pk":2}),
                data=invalid_updated_authenticator,
                content_type="application/json")

        # Get the authenticator again.
        new_authenticator_response = self.client.get(reverse('microservices:authenticator-detail', kwargs={"pk":2}))
        new_json_authenticator = new_authenticator_response.content.decode("utf-8")
        actual_authenticator = json.loads(new_json_authenticator)

        # Check that the authenticator was not updated.
        self.assertEquals(actual_authenticator, expected_authenticator)

# DELETE/DEL functionality.
class DeleteAuthenticatorTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    def test_delete_authenticator(self):
        # Verify authenticator with ID of 2 exists before continuing.
        verify_exists_response = self.client.get(reverse('microservices:authenticator-detail', kwargs={"pk":2}))
        self.assertEquals(verify_exists_response.status_code, 200)

        # Delete authenticator with ID of 2.
        # This returns a 204 No Content response, but there isn't really
        # a consistent standard among RESTful APIs in regards for what to return
        # so there's no need to validate this behavior.
        self.client.delete(reverse('microservices:authenticator-detail', kwargs={"pk":2}))

        # Check that the authenticator no longer exists.
        get_response = self.client.get(reverse('microservices:authenticator-detail', kwargs={"pk":2}))
        self.assertEquals(get_response.status_code, 404)
