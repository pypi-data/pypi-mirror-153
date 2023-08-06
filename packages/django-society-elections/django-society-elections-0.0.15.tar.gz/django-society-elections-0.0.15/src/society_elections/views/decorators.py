import functools

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from ..models import Election
from .helpers import get_latest_election, get_template


def validate_election_period(target_election_period: str):
    """Validates that the target election is currently in the given period

    Args:
        target_election_period (str): Election period the election should be in

    Returns:
        HttpResponse: The expected response if the election is in the target 
            election period, or a page stating it isn't in the target election 
            period otherwise.
    """
    if target_election_period not in Election.ELECTION_PERIODS:
        raise ValueError(
            f'target_election_period must be one of {Election.ELECTION_PERIODS}'
        )
    def validate_election_period_wrapper(func):
        @functools.wraps(func)
        def wrapper(req: HttpRequest, election: int=None, *args, **kwargs):
            if election is None:
                target_election = get_latest_election()
            else:
                target_election = get_object_or_404(Election, pk=election)
            
            if target_election.current_period != target_election_period:
                return render(req, get_template('election_wrong_period'), {
                    'election': target_election,
                    'period': target_election_period
                })
            elif election is None:
                return func(req, *args, **kwargs)
            else:
                return func(req, election, *args, **kwargs)
        return wrapper
    return validate_election_period_wrapper

