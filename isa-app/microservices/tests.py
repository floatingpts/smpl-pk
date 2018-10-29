from django.test import TestCase, Client
from django.urls import reverse
from . import models, urls

class GetMusicianDetailsTestCase(TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']

    # setUp method is called before each test in this class.
    def setUp(self):
        pass # Nothing to set up

    def test_get_existing_musician(self):
        # Assumes user with id 2 is stored in db.
        response = self.client.get(reverse('microservices:musician-detail', kwargs={"pk":2}))

        # Checks that response contains parameter & implicitly
        # checks that the HTTP status code is 200.
        self.assertContains(response, 'username')

    # Invalid user_id given in url, so error.
    def test_get_invalid_musician(self):
        response = self.client.get('/api/musicians/9/')
        self.assertEquals(response.status_code, 404)

    # tearDown method is called after each test.
    def tearDown(self):
        pass # Nothing to tear down.
