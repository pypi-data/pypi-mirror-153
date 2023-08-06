"""General purpose helpers for the views module"""
import logging
from uuid import UUID

from django.http import Http404
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404

from .. import app_settings
from ..models import AnonymousVoter, Election, RegisteredVoter

logger = logging.getLogger(__name__)

def get_template(name: str) -> str:
    """Retrieves the target template with the given name

    Templates are retrieved by prepending the set prefix onto the given name

    Args:
        name (str): Name of the template to retrieve

    Returns:
        str: Full template name to render
    """
    if app_settings.TEMPLATE_PREFIX.endswith('/'):
        return f'{app_settings.TEMPLATE_PREFIX}{name}.html'
    else:
        return f'{app_settings.TEMPLATE_PREFIX}/{name}.html'


def get_latest_election() -> Election:
    """Get the latest election or raise 404
    
    Raises:
        Http404: No election found
    
    Returns:
        Election: The election with the latest nomination start
    """
    try:
        election: Election = Election.objects.latest()
        logger.debug(f'Found latest election "{election}"')
    except Election.DoesNotExist:
        logger.warning('No election found, returning 404')
        raise Http404
    return election


def is_request_authenticated(election: Election, req: HttpRequest) -> bool:
    """Verify that a given request is authenticated to vote in an election

    Args:
        election (Election): Target election
        req (HttpRequest): Request object to verify

    Raises:
        Http404: RegisteredVoter cannot be found in a non-anonymized election

    Returns:
        bool: True if the request is authenticated, False otherwise
    """
    if election.anonymous:
        # Election is anonymous, validate voter or return login
        password = req.POST.get('password')
        if req.method != 'POST' or password is None:
            return False

        password_digest = AnonymousVoter.hash_password(password)
        try:
            get_object_or_404(
                AnonymousVoter, password=password_digest, election=election
            )
        except Http404:
            return False
        return True
    else: # Get voter for non-anonymous election
        if req.method == 'POST':
            uuid = req.POST.get('uuid')
        else:
            uuid = req.GET.get('uuid')

        # No user if uuid is not a UUID - None will work with the query
        if type(uuid) != UUID and uuid is not None:
            try:
                UUID(uuid)
            except ValueError:
                raise Http404
        
        voter = get_object_or_404(
            RegisteredVoter, election=election, pk=uuid
        )

        # Has the voter verified their email?
        return voter.verified
