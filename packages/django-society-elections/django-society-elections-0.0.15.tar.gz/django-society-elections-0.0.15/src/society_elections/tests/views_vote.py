"""Module to test the views.vote module of society_elections"""
from unittest.mock import Mock, patch

from django.http.response import Http404
from django.test import Client, TestCase
from django.urls.base import reverse
from django.utils import timezone
from datetime import timedelta

from ..models import Vote
from ..views.helpers import get_template
from .helpers import (PASSWORD, create_anon_voter, create_candidate,
                      create_election, create_election_position,
                      create_position, create_voter)


class VoteViewTestCase(TestCase):
    """Tests the views.vote.vote_view function by making client calls"""
    @classmethod
    def setUpTestData(cls) -> None:
        cls.reg_election = create_election(
            anonymous=False,
            nominations_start=timezone.now()-timedelta(days=2),
            nominations_end=timezone.now()-timedelta(days=1),
            voting_start=timezone.now(),
            voting_end=timezone.now()+timedelta(days=1),
        )
        cls.reg_voter = create_voter(cls.reg_election)
        cls.voter_uuid = cls.reg_voter.pk

        cls.anon_election = create_election(
            admin_title='Anonymous Test Election',
            anonymous=True,
            nominations_start=timezone.now()-timedelta(days=2),
            nominations_end=timezone.now()-timedelta(days=1),
            voting_start=timezone.now(),
            voting_end=timezone.now()+timedelta(days=1),
        )
        cls.voter_password = PASSWORD
        cls.anon_voter = create_anon_voter(cls.anon_election)

        cls.position1 = create_position(admin_title='Test Position 1')
        cls.position2 = create_position(admin_title='Test Position 2')
        cls.reg_election_position1 = create_election_position(
            cls.reg_election, cls.position1
        )
        cls.reg_election_position2 = create_election_position(
            cls.reg_election, cls.position2
        )
        cls.anon_election_position1 = create_election_position(
            cls.anon_election, cls.position1
        )
        cls.anon_election_position2 = create_election_position(
            cls.anon_election, cls.position2
        )

        cls.reg_candidate1 = create_candidate(cls.reg_election_position1)
        cls.reg_candidate2 = create_candidate(cls.reg_election_position2)
        cls.anon_candidate1 = create_candidate(cls.anon_election_position1)
        cls.anon_candidate2 = create_candidate(cls.anon_election_position2)


    def setUp(self) -> None:
        self.client = Client()

    #== Regular election
    @patch('society_elections.views.vote.is_request_authenticated', Mock(side_effect=Http404))
    def test_reg_election_no_voter_returns_401(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.get(reverse('society_elections:vote'), {'uuid': self.voter_uuid})
        self.assertEqual(res.status_code, 401)


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=False))
    def test_reg_election_not_authenticated_returns_401(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.get(reverse('society_elections:vote'), {'uuid': self.voter_uuid})
        self.assertEqual(res.status_code, 401)
        self.assertTemplateUsed(res, get_template('voter_not_verified'))


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_reg_election_GET_req_returns_vote_template(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.get(reverse('society_elections:vote'), {'uuid': self.voter_uuid})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, get_template('vote'))


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_reg_election_POST_req_no_submit_returns_vote_template(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.post(reverse('society_elections:vote'), {'uuid': self.voter_uuid})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, get_template('vote'))

    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_reg_election_POST_req_empty_submit_returns_vote_template(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.post(reverse('society_elections:vote'), {'uuid': self.voter_uuid, 'submit': ''}) 
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, get_template('vote'))


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_reg_election_no_votes_returns_vote_template(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.post(reverse('society_elections:vote'), {'uuid': self.voter_uuid, 'submit': True})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, get_template('vote'))


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_reg_election_some_votes_returns_vote_template(self):
        Vote.objects.create(
            registered_voter=self.reg_voter,
            candidate=self.reg_candidate1,
            position=self.reg_election_position1
        )
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.post(reverse('society_elections:vote'), {'uuid': self.voter_uuid, 'submit': True})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, get_template('vote'))


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_reg_election_all_votes_redirects_vote_submitted(self):
        Vote.objects.create(
            registered_voter=self.reg_voter,
            candidate=self.reg_candidate1,
            position=self.reg_election_position1
        )
        Vote.objects.create(
            registered_voter=self.reg_voter,
            candidate=self.reg_candidate2,
            position=self.reg_election_position2
        )
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.post(reverse('society_elections:vote'), {'uuid': self.voter_uuid, 'submit': True})
        self.assertRedirects(res, reverse('society_elections:vote_submitted'))
        

    #== Anonymous Election
    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=False))
    def test_anon_election_not_authenticated_returns_401(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.anon_election)):
            res = self.client.post(reverse('society_elections:vote'), {'password': self.voter_password})
        self.assertEqual(res.status_code, 401)
        self.assertTemplateUsed(res, get_template('password_entry'))


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_anon_election_POST_req_no_submit_returns_vote_template(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.anon_election)):
            res = self.client.post(reverse('society_elections:vote'), {'password': self.voter_password})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(get_template('vote'))


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_anon_election_POST_req_empty_submit_returns_vote_template(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.anon_election)):
            res = self.client.post(reverse('society_elections:vote'), {'password': self.voter_password, 'submit': ''})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(get_template('vote'))


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_anon_election_no_votes_returns_vote_template(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.anon_election)):
            res = self.client.post(reverse('society_elections:vote'), {'password': self.voter_password, 'submit': True})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(get_template('vote'))


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_anon_election_some_votes_returns_vote_template(self):
        Vote.objects.create(
            anonymous_voter=self.anon_voter,
            candidate=self.anon_candidate1,
            position=self.anon_election_position1
        )
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.anon_election)):
            res = self.client.post(reverse('society_elections:vote'), {'password': self.voter_password, 'submit': True})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(get_template('vote'))


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_anon_election_all_votes_redirects_vote_submitted(self):
        Vote.objects.create(
            anonymous_voter=self.anon_voter,
            candidate=self.anon_candidate1,
            position=self.anon_election_position1
        )
        Vote.objects.create(
            anonymous_voter=self.anon_voter,
            candidate=self.anon_candidate2,
            position=self.anon_election_position2
        )
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.anon_election)):
            res = self.client.post(reverse('society_elections:vote'), {'password': self.voter_password, 'submit': True})
        self.assertRedirects(res, reverse('society_elections:vote_submitted'))


class CreateVoteAjaxTestCase(TestCase):
    """Tests the views.vote.create_vote_ajax function"""
    @classmethod
    def setUpTestData(cls) -> None:
        cls.reg_election = create_election(
            anonymous=False,
            nominations_start=timezone.now()-timedelta(days=2),
            nominations_end=timezone.now()-timedelta(days=1),
            voting_start=timezone.now(),
            voting_end=timezone.now()+timedelta(days=1),
        )
        cls.reg_voter = create_voter(cls.reg_election)
        cls.voter_uuid = cls.reg_voter.pk

        cls.anon_election = create_election(
            admin_title='Anonymous Test Election',
            anonymous=True,
            nominations_start=timezone.now()-timedelta(days=2),
            nominations_end=timezone.now()-timedelta(days=1),
            voting_start=timezone.now(),
            voting_end=timezone.now()+timedelta(days=1),
        )
        cls.voter_password = PASSWORD
        cls.anon_voter = create_anon_voter(cls.anon_election)

        cls.position1 = create_position(admin_title='Test Position 1')
        cls.position2 = create_position(admin_title='Test Position 2')
        cls.reg_election_single_position = create_election_position(
            cls.reg_election, cls.position1
        )
        cls.reg_election_multiple_position = create_election_position(
            cls.reg_election, cls.position2, positions_available=2, 
    
        )
        cls.anon_election_single_position = create_election_position(
            cls.anon_election, cls.position1
        )
        cls.anon_election_multiple_position = create_election_position(
            cls.anon_election, cls.position2, positions_available=2, 
    
        )

        cls.reg_candidate1 = create_candidate(cls.reg_election_single_position)
        cls.reg_candidate2 = create_candidate(cls.reg_election_multiple_position)
        cls.anon_candidate1 = create_candidate(cls.anon_election_single_position)
        cls.anon_candidate2 = create_candidate(cls.anon_election_multiple_position)


    def setUp(self) -> None:
        self.client = Client()

    def test_get_request_returns_405(self):
        res = self.client.get(reverse('society_elections:vote_create'))
        self.assertEqual(res.status_code, 405)


    @patch('society_elections.views.vote.is_request_authenticated', Mock(side_effect=Http404))
    def test_voter_404_returns_401(self):
        res = self.client.post(reverse('society_elections:vote_create'))
        self.assertEqual(res.json().get('error'), 'Not authorized to vote')


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=False))
    def test_voter_not_authenticated_returns_401(self):
        res = self.client.post(reverse('society_elections:vote_create'))
        self.assertEqual(res.json().get('error'), 'Not authorized to vote')


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_no_position_returns_404(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.post(reverse('society_elections:vote_create'), {'position': 100})
        self.assertEqual(res.json().get('error'), 'Position does not exist')


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_malformed_position_returns_404(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.post(reverse('society_elections:vote_create'), {'position': 'hello'})
        self.assertEqual(res.json().get('error'), 'Position does not exist')


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_no_candidate_returns_404(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.post(reverse('society_elections:vote_create'), {
                'position': self.reg_election_single_position.pk, 'candidate': 100
            })
        self.assertEqual(res.json().get('error'), 'Candidate does not exist')


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_malformed_candidate_returns_404(self):
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.post(reverse('society_elections:vote_create'), {
                'position': self.reg_election_single_position.pk, 'candidate': 'hello'
            })
        self.assertEqual(res.json().get('error'), 'Candidate does not exist')


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_regular_voter_already_voted_updates_existing_vote(self):
        existing_vote = Vote.objects.create(
            registered_voter=self.reg_voter,
            candidate=self.reg_candidate1,
            position=self.reg_election_single_position
        )
        new_candidate = create_candidate(self.reg_election_single_position)
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.post(reverse('society_elections:vote_create'), {
                'position': self.reg_election_single_position.pk, 'uuid': self.reg_voter.pk, 'candidate': new_candidate.pk
            })
        self.assertEqual(res.status_code, 200)
        updated_vote = Vote.objects.get(pk=existing_vote.pk)
        self.assertEqual(updated_vote.candidate, new_candidate)


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_anon_voter_already_voted_updates_existing_vote(self):
        existing_vote = Vote.objects.create(
            anonymous_voter=self.anon_voter,
            candidate=self.anon_candidate1,
            position=self.anon_election_single_position
        )
        new_candidate = create_candidate(self.anon_election_single_position)
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.anon_election)):
            res = self.client.post(reverse('society_elections:vote_create'), {
                'position': self.anon_election_single_position.pk, 'password': self.voter_password, 'candidate': new_candidate.pk
            })
        self.assertEqual(res.status_code, 200)
        updated_vote = Vote.objects.get(pk=existing_vote.pk)
        self.assertEqual(updated_vote.candidate, new_candidate)


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_excessive_votes_multiple_positions_returns_409(self):
        Vote.objects.create(
            registered_voter=self.reg_voter,
            candidate=self.reg_candidate2,
            position=self.reg_election_multiple_position,
        )
        new_candidate_1 = create_candidate(self.reg_election_multiple_position)
        new_candidate_2 = create_candidate(self.reg_election_multiple_position)
        Vote.objects.create(
            registered_voter=self.reg_voter,
            candidate=new_candidate_1,
            position=self.reg_election_multiple_position,
        )
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.post(reverse('society_elections:vote_create'), {
                'position': self.reg_election_multiple_position.pk, 'uuid': self.reg_voter.pk, 'candidate': new_candidate_2.pk
            })
        self.assertEqual(res.json().get('error'), 'Already submitted votes for this position or candidate')


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_double_vote_multiple_positions_returns_409(self):
        Vote.objects.create(
            registered_voter=self.reg_voter,
            candidate=self.reg_candidate2,
            position=self.reg_election_multiple_position,
        )
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.post(reverse('society_elections:vote_create'), {
                'position': self.reg_election_multiple_position.pk,
                'candidate': self.reg_candidate2.pk,
                'uuid': self.reg_voter.pk
            })
        self.assertEqual(res.json().get('error'), 'Already submitted votes for this position or candidate')


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_regular_voter_new_vote_creates_new_vote(self):
        self.assertEqual(Vote.objects.count(), 0)
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.reg_election)):
            res = self.client.post(reverse('society_elections:vote_create'), {
                'position': self.reg_election_single_position.pk,
                'candidate': self.reg_candidate1.pk,
                'uuid': self.reg_voter.pk
            })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Vote.objects.count(), 1)


    @patch('society_elections.views.vote.is_request_authenticated', Mock(return_value=True))
    def test_anon_voter_new_vote_creates_new_vote(self):
        self.assertEqual(Vote.objects.count(), 0)
        with patch('society_elections.views.vote.get_latest_election', Mock(return_value=self.anon_election)):
            res = self.client.post(reverse('society_elections:vote_create'), {
                'position': self.anon_election_multiple_position.pk,
                'candidate': self.anon_candidate1.pk,
                'password': self.voter_password
            })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Vote.objects.count(), 1)