"""Some helpers for the tests module of society_elections"""
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from ..models import (AnonymousVoter, Candidate, Election, ElectionPosition,
                      Position, RegisteredVoter, Vote)

PASSWORD = 'Test1234!'
USERNAME = 'test_user'
EMAIL = 'test@test.com'
ELECTION_DATA = {
    'title': 'Test Election',
    'description': 'This is a test election',
    'nominations_start': timezone.now() + timedelta(days=1),
    'nominations_end': timezone.now() + timedelta(days=2),
    'voting_start': timezone.now() + timedelta(days=3),
    'voting_end': timezone.now() + timedelta(days=4),
    'candidate_email_domain_whitelist': 'test.com'
}

def create_election(
    created_by: User=None, admin_title: str='Test Election', **kwargs
) -> Election:
    if created_by is None:
        created_by = create_user()
    return Election.objects.create(
        admin_title=admin_title,
        created_by=created_by,
        title=kwargs.pop('title', ELECTION_DATA['title']),
        description=kwargs.pop('description', ELECTION_DATA['description']),
        nominations_start=kwargs.pop('nominations_start', ELECTION_DATA['nominations_start']),
        nominations_end=kwargs.pop('nominations_end', ELECTION_DATA['nominations_end']),
        voting_start=kwargs.pop('voting_start', ELECTION_DATA['voting_start']),
        voting_end=kwargs.pop('voting_end', ELECTION_DATA['voting_end']),
        candidate_email_domain_whitelist=kwargs.pop(
            'candidate_email_domain_whitelist', 
            ELECTION_DATA['candidate_email_domain_whitelist']
        ),
        **kwargs
    )


def create_voter(election: Election) -> RegisteredVoter:
    return RegisteredVoter.objects.create(
        election=election,
        email=EMAIL,
        verified_at=timezone.now()
    )


def create_anon_voter(election: Election) -> AnonymousVoter:
    return AnonymousVoter.objects.create(
        election=election,
        password=AnonymousVoter.hash_password(PASSWORD)
    )


def create_position(**kwargs) -> Position:
    admin_title = kwargs.pop('admin_title', 'Test Position')
    title = kwargs.pop('title', 'Test Position')
    description = kwargs.pop('description', 'Test position for testing')
    return Position.objects.create(
        title=title,
        admin_title=admin_title,
        description=description
    )


def create_election_position(
    election: Election, position: Position, **kwargs
) -> ElectionPosition:
    return ElectionPosition.objects.create(
        position=position,
        election=election,
        **kwargs
    )


def create_candidate(position: ElectionPosition, **kwargs) -> Candidate:
    full_name = kwargs.pop('full_name', 'Test McTestface')
    email = kwargs.pop('email', EMAIL)
    manifesto = kwargs.pop('manifesto', 'Test manifesto')
    email_verified = kwargs.pop('email_verified', True)
    return Candidate.objects.create(
        position=position,
        full_name=full_name,
        email=email,
        manifesto=manifesto,
        email_verified=email_verified
    )


def create_user() -> User:
    user = User(username=f'{uuid.uuid4()}')
    user.set_password('Test1234!')
    user.save()
    return user


def create_all() -> dict:
    pass