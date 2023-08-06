"""Module to test the functions in the views.helpers module"""

from uuid import uuid4

from django.http import Http404
from django.http.request import HttpRequest
from django.test import TestCase

from ..models import RegisteredVoter
from ..views.helpers import is_request_authenticated
from .helpers import PASSWORD, create_anon_voter, create_election, create_voter


class IsRequestAuthenticatedTestCase(TestCase):
    """Tests the is_request_authenticated function"""
    @classmethod
    def setUpTestData(cls) -> None:
        cls.anon_election = create_election(
            admin_title='Anonymous Test Election',
            anonymous=True
        )
        cls.reg_election = create_election(anonymous=False)

        cls.voter_password = PASSWORD
        cls.anon_voter = create_anon_voter(cls.anon_election)
        cls.reg_voter = create_voter(cls.reg_election)
        cls.voter_uuid = cls.reg_voter.pk


    def setUp(self) -> None:
        self.request = HttpRequest()


    #== Anonymous Election
    def test_get_req_in_anon_election_returns_false(self):
        self.request.method = 'GET'
        self.request.GET['password'] = self.voter_password
        self.assertFalse(
            is_request_authenticated(self.anon_election, self.request)
        )

    def test_post_req_no_pass_in_anon_election_returns_false(self):
        self.request.method = 'POST'
        self.assertFalse(
            is_request_authenticated(self.anon_election, self.request)
        )

    def test_post_req_none_pass_in_anon_election_returns_false(self):
        self.request.method = 'POST'
        self.request.POST['password'] = None
        self.assertFalse(
            is_request_authenticated(self.anon_election, self.request)
        )

    def test_post_req_empty_pass_in_anon_election_returns_false(self):
        self.request.method = 'POST'
        self.request.POST['password'] = ''
        self.assertFalse(
            is_request_authenticated(self.anon_election, self.request)
        )

    def test_post_req_uuid_in_anon_election_returns_false(self):
        self.request.method = 'POST'
        self.request.POST['uuid'] = self.voter_uuid
        self.assertFalse(
            is_request_authenticated(self.anon_election, self.request)
        )

    def test_post_req_bad_pass_in_anon_election_returns_false(self):
        self.request.method = 'POST'
        self.request.POST['password'] = 'badpass'
        self.assertFalse(
            is_request_authenticated(self.anon_election, self.request)
        )

    def test_post_req_good_pass_wrong_election_in_anon_election_returns_false(self):
        self.request.method = 'POST'
        self.request.POST['password'] = self.voter_password
        fake_anon_election = create_election(
            admin_title='Fake Anonymous Test Election',
            anonymous=True
        )
        self.assertFalse(
            is_request_authenticated(fake_anon_election, self.request)
        )

    def test_post_req_good_pass_in_anon_election_returns_true(self):
        self.request.method = 'POST'
        self.request.POST['password'] = self.voter_password
        self.assertTrue(
            is_request_authenticated(self.anon_election, self.request)
        )

    #== Non-anonymous Election
    #= GET requests
    def test_get_req_no_uuid_returns_false(self):
        self.request.method = 'GET'
        with self.assertRaises(Http404):
            is_request_authenticated(self.reg_election, self.request)

    def test_get_req_pass_returns_false(self):
        self.request.method = 'GET'
        self.request.GET['password'] = self.voter_password
        with self.assertRaises(Http404):
            is_request_authenticated(self.reg_election, self.request)

    def test_get_req_bad_uuid_returns_false(self):
        self.request.method = 'GET'
        self.request.GET['uuid'] = uuid4()
        with self.assertRaises(Http404):
            is_request_authenticated(self.reg_election, self.request)

    def test_get_req_malformed_uuid_returns_false(self):
        self.request.method = 'GET'
        self.request.GET['uuid'] = 'notuuid'
        with self.assertRaises(Http404):
            is_request_authenticated(self.reg_election, self.request)

    def test_get_req_good_uuid_wrong_election_returns_false(self):
        self.request.method = 'GET'
        self.request.GET['uuid'] = self.voter_uuid
        fake_election = create_election(
            admin_title='Fake Test Election',
            anonymous=False
        )
        with self.assertRaises(Http404):
            is_request_authenticated(fake_election, self.request)

    def test_get_req_good_uuid_returns_true(self):
        self.request.method = 'GET'
        self.request.GET['uuid'] = self.voter_uuid
        self.assertTrue(
            is_request_authenticated(self.reg_election, self.request)
        )

    #= POST requests
    def test_post_req_no_uuid_returns_false(self):
        self.request.method = 'POST'
        with self.assertRaises(Http404):
            is_request_authenticated(self.reg_election, self.request)

    def test_post_req_pass_returns_false(self):
        self.request.method = 'POST'
        self.request.POST['password'] = self.voter_password
        with self.assertRaises(Http404):
            is_request_authenticated(self.reg_election, self.request)

    def test_post_req_bad_uuid_returns_false(self):
        self.request.method = 'POST'
        self.request.POST['uuid'] = uuid4()
        with self.assertRaises(Http404):
            is_request_authenticated(self.reg_election, self.request)

    def test_post_req_malformed_uuid_returns_false(self):
        self.request.method = 'POST'
        self.request.POST['uuid'] = 'notuuid'
        with self.assertRaises(Http404):
            is_request_authenticated(self.reg_election, self.request)

    def test_post_req_good_uuid_wrong_election_returns_false(self):
        self.request.method = 'POST'
        self.request.POST['uuid'] = self.voter_uuid
        fake_election = create_election(
            admin_title='Fake Test Election',
            anonymous=False
        )
        with self.assertRaises(Http404):
            is_request_authenticated(fake_election, self.request)

    def test_post_req_good_uuid_returns_true(self):
        self.request.method = 'POST'
        self.request.POST['uuid'] = self.voter_uuid
        self.assertTrue(
            is_request_authenticated(self.reg_election, self.request)
        )

    #== MISC
    def test_unverified_voter_returns_false(self):
        unverified_voter = RegisteredVoter.objects.create(
            election=self.reg_election,
            email='unverified@test.com',
        )
        self.request.method = 'POST'
        self.request.POST['uuid'] = unverified_voter.id
        self.assertFalse(
            is_request_authenticated(self.reg_election, self.request)
        )
